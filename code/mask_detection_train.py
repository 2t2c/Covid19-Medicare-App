import numpy as np
import matplotlib.pyplot as plt
import cv2
import random
import pandas as pd
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
# config = tf.ConfigProto()
# config.gpu_options.allow_growth = True
# sess = tf.Session(config=config)
from tensorflow.keras.applications import InceptionResNetV2, Xception, DenseNet201
from tensorflow.keras.layers import Dense, GlobalAveragePooling2D, Flatten
from tensorflow.keras import optimizers, Sequential
from tensorflow.keras.callbacks import LearningRateScheduler
from tensorflow.keras.optimizers import Adam
import efficientnet.tfkeras as efn
from tqdm import tqdm
import tensorflow.keras.backend as K
from sklearn.model_selection import cross_val_score, KFold
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image
import math
AUTO = tf.data.experimental.AUTOTUNE
k_fold = KFold(n_splits=10, shuffle=False)


os.chdir('./mask_detection')
TRAIN_DIR = 'train/'
CATEGORIES = ["mask","no_mask"] # 1 : mask , 0 : no_mask
image_id = []
label = []

CFG = dict(
    rot=180.0,
    shr=2.0,
    hzoom=8.0,
    wzoom=8.0,
    hshift=8.0,
    wshift=8.0,
)

def train_csv():
    for image in os.listdir(TRAIN_DIR):
        image_name = image.split('.')[0]
        image_label = image.split('_')[0]
        image_id.append(image_name)

        if image_label == 'mask':
            label.append(1)
        else:
            label.append(0)

    train = pd.DataFrame({'image_id':image_id,'label':label})
    train.to_csv('mask_train.csv',index=False)

# train_csv()

train = pd.read_csv('mask_train.csv')
labels = train['label'].values
# labels = labels.tolist()
labels = tf.keras.utils.to_categorical(labels) # [0,0,1,1,1] to [[1,0][1,0][0,1][0,1][0,1]]

train_paths = train.image_id.apply(lambda x: TRAIN_DIR + x + '.jpg').values
# print(train_paths)

IMG_SIZE = 256
BATCH_SIZE = 8
strategy = tf.distribute.get_strategy()

# learning rate schedule
LR_START = 0.00001
LR_MAX = 0.0008 * strategy.num_replicas_in_sync
LR_MIN = 0.00001
LR_RAMPUP_EPOCHS = 15
LR_SUSTAIN_EPOCHS = 3
LR_EXP_DECAY = .8

def lrfn(epoch):
    if epoch < LR_RAMPUP_EPOCHS:
        lr = (LR_MAX - LR_START) / LR_RAMPUP_EPOCHS * epoch + LR_START
    elif epoch < LR_RAMPUP_EPOCHS + LR_SUSTAIN_EPOCHS:
        lr = LR_MAX
    else:
        lr = (LR_MAX - LR_MIN) * LR_EXP_DECAY**(epoch - LR_RAMPUP_EPOCHS - LR_SUSTAIN_EPOCHS) + LR_MIN
    return lr

lr_callback = LearningRateScheduler(lrfn, verbose=True)

# y = [lrfn(x) for x in range(40)]
# plt.plot(y)
# plt.show()

def get_mat(rotation, shear, height_zoom, width_zoom, height_shift, width_shift):
    # returns 3x3 transformmatrix which transforms indicies
    # CONVERT DEGREES TO RADIANS
    rotation = math.pi * rotation / 180.
    shear = math.pi * shear / 180.

    def get_3x3_mat(lst):
        return tf.reshape(tf.concat([lst], axis=0), [3, 3])

    # ROTATION MATRIX
    c1 = tf.math.cos(rotation)
    s1 = tf.math.sin(rotation)
    one = tf.constant([1], dtype='float32')
    zero = tf.constant([0], dtype='float32')

    rotation_matrix = get_3x3_mat([c1, s1, zero,
                                   -s1, c1, zero,
                                   zero, zero, one])
    # SHEAR MATRIX
    c2 = tf.math.cos(shear)
    s2 = tf.math.sin(shear)

    shear_matrix = get_3x3_mat([one, s2, zero,
                                zero, c2, zero,
                                zero, zero, one])
    # ZOOM MATRIX
    zoom_matrix = get_3x3_mat([one / height_zoom, zero, zero,
                               zero, one / width_zoom, zero,
                               zero, zero, one])
    # SHIFT MATRIX
    shift_matrix = get_3x3_mat([one, zero, height_shift,
                                zero, one, width_shift,
                                zero, zero, one])

    return K.dot(K.dot(rotation_matrix, shear_matrix),
                 K.dot(zoom_matrix, shift_matrix))


def transform(image, cfg):
    # input image - is one image of size [dim,dim,3] not a batch of [b,dim,dim,3]
    # output - image randomly rotated, sheared, zoomed, and shifted
    DIM = IMG_SIZE
    XDIM = DIM % 2  # fix for size 331

    rot = cfg['rot'] * tf.random.normal([1], dtype='float32')
    shr = cfg['shr'] * tf.random.normal([1], dtype='float32')
    h_zoom = 1.0 + tf.random.normal([1], dtype='float32') / cfg['hzoom']
    w_zoom = 1.0 + tf.random.normal([1], dtype='float32') / cfg['wzoom']
    h_shift = cfg['hshift'] * tf.random.normal([1], dtype='float32')
    w_shift = cfg['wshift'] * tf.random.normal([1], dtype='float32')

    # GET TRANSFORMATION MATRIX
    m = get_mat(rot, shr, h_zoom, w_zoom, h_shift, w_shift)

    # LIST DESTINATION PIXEL INDICES
    x = tf.repeat(tf.range(DIM // 2, -DIM // 2, -1), DIM)
    y = tf.tile(tf.range(-DIM // 2, DIM // 2), [DIM])
    z = tf.ones([DIM * DIM], dtype='int32')
    idx = tf.stack([x, y, z])

    # ROTATE DESTINATION PIXELS ONTO ORIGIN PIXELS
    idx2 = K.dot(m, tf.cast(idx, dtype='float32'))
    idx2 = K.cast(idx2, dtype='int32')
    idx2 = K.clip(idx2, -DIM // 2 + XDIM + 1, DIM // 2)

    # FIND ORIGIN PIXEL VALUES
    idx3 = tf.stack([DIM // 2 - idx2[0,], DIM // 2 - 1 + idx2[1,]])
    d = tf.gather_nd(image, tf.transpose(idx3))

    return tf.reshape(d, [DIM, DIM, 3])

def decode_image(filename, label=None, image_size=(IMG_SIZE, IMG_SIZE)):
    bits = tf.io.read_file(filename)
    image = tf.image.decode_jpeg(bits, channels=3)
    image = tf.cast(image, tf.float32) / 255.0
    image = tf.image.resize(image, image_size)
    if label is None:
        return image
    else:
        return image, label


def data_augment(image, label=None):
    image = transform(image, CFG)
    image = tf.image.random_flip_left_right(image)
    image = tf.image.random_hue(image, 0.1)
    image = tf.image.random_brightness(image, 0.2)
    image = tf.image.random_contrast(image, 0.8, 1.2)
    image = tf.image.random_saturation(image, 0.7, 1.3)

    if label is None:
        return image
    else:
        return image, label


def get_training_dataset():
    dataset = tf.data.Dataset.from_tensor_slices((train_paths, labels))
    dataset = dataset.map(decode_image, num_parallel_calls=AUTO)
    dataset = dataset.map(data_augment, num_parallel_calls=AUTO)
    dataset = dataset.repeat()
    dataset = dataset.shuffle(512)
    dataset = dataset.batch(BATCH_SIZE)
    dataset = dataset.prefetch(AUTO)
    return dataset

training_dataset = get_training_dataset()

def create_model():
    pretrained_model = efn.EfficientNetB3(weights='imagenet', pooling="avg", include_top=False,
                                          input_shape=(IMG_SIZE, IMG_SIZE, 3))
    pretrained_model.trainable = True
    model = tf.keras.Sequential([
        pretrained_model,
        tf.keras.layers.Dense(512, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(128, activation='relu'),
        tf.keras.layers.BatchNormalization(),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(2, activation='softmax')
    ])
    return model

model = create_model()

model.compile(optimizer="adam", loss='binary_crossentropy', metrics=['accuracy'])

print('\nTraining')
model.fit(training_dataset,
          steps_per_epoch=labels.shape[0] // BATCH_SIZE,
          epochs=10, verbose=1, callbacks=[lr_callback]
          )

model.save("EfnB3.h5")


model = load_model("EfnB3.h5")
model.compile(optimizer="adam", loss='categorical_crossentropy', metrics=['accuracy'])

test = ['train/mask_90.jpg', 'train/mask_91.jpg',
       'train/mask_92.jpg', 'train/mask_93.jpg', 'train/mask_94.jpg',
       'train/mask_95.jpg', 'train/mask_96.jpg', 'train/mask_97.jpg',
       'train/mask_98.jpg', 'train/mask_99.jpg', 'train/no_mask_1.jpg',
       'train/no_mask_10.jpg', 'train/no_mask_100.jpg',
       'train/no_mask_101.jpg', 'train/no_mask_102.jpg',
       'train/no_mask_103.jpg', 'train/no_mask_104.jpg',
       'train/no_mask_105.jpg', 'train/no_mask_106.jpg']

print('\nPredicting')
def predict():
    for id in test:
        # img = image.load_img(id, target_size=(IMG_SIZE, IMG_SIZE))
        img = cv2.imread(id)
        img = cv2.resize(img,(IMG_SIZE,IMG_SIZE))
        img = img / 255.0
        # print(type(img))
        # print(img)
        # img = np.array(img)
        # img = np.expand_dims(img, axis=0)
        # x = image.img_to_array(img)
        # x = np.expand_dims(x, axis=0)
        img = np.reshape(img,(1,IMG_SIZE,IMG_SIZE,3))
        # prob = model.predict(img)
        # prob = (model.predict(img) > 0.5).astype("int32")
        prob = np.argmax(model.predict(img),axis=1)[0]
        print(prob)

predict()



