import numpy as np
import matplotlib.pyplot as plt
import cv2
import random
import pandas as pd
import os
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import tensorflow as tf
# config = tf.ConfigProto()
# oconfig.gpu_options.allow_growth = True
# sess = tf.Sessin(config=config)
import efficientnet.tfkeras as efn
AUTO = tf.data.experimental.AUTOTUNE
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.image import img_to_array
from tensorflow.keras.applications.efficientnet import preprocess_input
import imutils

os.chdir('Y:/Data Science/mask_detection')
model = load_model("EfnB3.h5")
model.compile(optimizer="adam", loss='binary_crossentropy', metrics=['accuracy'])

cap = cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
frame_width = int(cap.get(3))
frame_height = int(cap.get(4))

size = (frame_width, frame_height)
out = cv2.VideoWriter('C:/Users/Udit/Desktop/md.avi',
                         cv2.VideoWriter_fourcc(*'MJPG'),
                         15, size)

DNN = "CAFFE"
if DNN == "CAFFE":
    modelFile = "res10_300x300_ssd_iter_140000.caffemodel"
    configFile = "deploy.prototxt"
    net = cv2.dnn.readNetFromCaffe(configFile, modelFile)
else:
    modelFile = "opencv_face_detector_uint8.pb"
    configFile = "opencv_face_detector.pbtxt"
    net = cv2.dnn.readNetFromTensorflow(modelFile, configFile)

labels_dict = {1:'  MASK',0:'NO MASK'}
colors_dict = {1:(0,255,0),0:(0,0,255)}

IMG_SIZE = 256
writer = None

def detect_and_predict_mask(frame, net, model):
    (h, w) = frame.shape[:2]
    blob = cv2.dnn.blobFromImage(frame, 1.0, (256, 256),
        (104.0, 177.0, 123.0))
    net.setInput(blob)
    detections = net.forward()
    # print(detections.shape)
    faces = []
    locs = []
    preds = []
    for i in range(0, detections.shape[2]):
        confidence = detections[0, 0, i, 2]
        if confidence > 0.5:
            box = detections[0, 0, i, 3:7] * np.array([w, h, w, h])
            (startX, startY, endX, endY) = box.astype("int")
            (startX, startY) = (max(0, startX), max(0, startY))
            (endX, endY) = (min(w - 1, endX), min(h - 1, endY))

            face = frame[startY:endY, startX:endX]

            face = cv2.cvtColor(face, cv2.COLOR_BGR2RGB)
            face = cv2.resize(face,(IMG_SIZE,IMG_SIZE))
            # face = np.reshape(face, (1, IMG_SIZE, IMG_SIZE, 3))
            face = img_to_array(face)
            face = preprocess_input(face)
            face = face / 255.0

            faces.append(face)
            locs.append((startX, startY, endX, endY))

    if len(faces) > 0:
        faces = np.array(faces, dtype="float32")
        preds = model.predict(faces)

    return (locs, preds)

while(True):
    ret, img = cap.read()
    img = cv2.flip(img,1)

    x,y,w,h = 20,40,20,20
    # (locs, preds) = detect_and_predict_mask(img, net, model)
    (locs, preds) = detect_and_predict_mask(img, net, model)

    for (box, pred) in zip(locs, preds):
        (startX, startY, endX, endY) = box
        (mask, withoutMask) = pred

        label = "Mask" if mask < withoutMask else "No Mask"
        color = (0, 255, 0) if label == "Mask" else (0, 0, 255)

        label = "{}: {:.2f}%".format(label, max(mask, withoutMask) * 100)

        cv2.rectangle(img, (startX-5, startY), (endX+5, endY), color, 2)
        cv2.rectangle(img, (startX-5, startY), (endX+5, startY+25), color, -1)
        cv2.putText(img, label, (startX+5, startY+20), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)

    # if result == 1:
    #     mask_prob = round(100*prob[0][1], 2)
    #     text1 = f'MASK: {mask_prob}'
    #     # print(text1)
    #     cv2.rectangle(img, (x, y), (x + w, y + h), (0,255,0), -1)
    #     cv2.putText(img, text1, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)
    # elif result == 0:
    #     nomask_prob = round(100*prob[0][0], 2)
    #     text2 = f'NO MASK: {nomask_prob}'
    #     # print(text2)
    #     cv2.rectangle(img, (x, y), (x + w, y + h), (0, 0, 255), -1)
    #     cv2.putText(img, text2, (x, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

    # haar
    # for (x, y, w, h) in faces:
    #     face_img = img_gray[y:y + w, x:x + w]
    #     resized = cv2.resize(face_img, (100, 100))
    #     cv2.rectangle(img, (x, y), (x + w, y + h), colors_dict[result], 2)
    #     cv2.rectangle(img, (x, y - 40), (x + w, y), colors_dict[result], -1)
    #     cv2.putText(img, labels_dict[result], (x+30, y - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    # opencv dnn
    # blob = cv2.dnn.blobFromImage(img, 1.0, (256, 256), [104, 117, 123], False, False)
    #
    # net.setInput(blob)
    # detections = net.forward()
    # bboxes = []
    # for i in range(detections.shape[2]):
    #     confidence = detections[0, 0, i, 2]
    #     if confidence > 0.5:
    #         x1 = int(detections[0, 0, i, 3] * frame_width)
    #         y1 = int(detections[0, 0, i, 4] * frame_height)
    #         x2 = int(detections[0, 0, i, 5] * frame_width)
    #         y2 = int(detections[0, 0, i, 6] * frame_height)
    #         cv2.rectangle(img, (x1, y1), (x2, y2), colors_dict[result], 2)
    #         cv2.rectangle(img, (x1, y1), (x2, y1+25), colors_dict[result], -1)
    #         cv2.putText(img, labels_dict[result], (x1+30,y1+20), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

    cv2.imshow("MaskDetection", img)
    if cv2.waitKey(1) % 0xFF == ord("q"):
        break

    # frame = imutils.resize(img, width=700)
    # fourcc = cv2.VideoWriter_fourcc(*"MJPG")
    # writer = cv2.VideoWriter('C:/Users/Udit/Desktop/md.avi', fourcc, 30,
    #                          (frame.shape[1], frame.shape[0]), True)
    # if writer is not None:
    #     writer.write(frame)
    out.write(img)

cap.release()
cv2.destroyAllWindows()