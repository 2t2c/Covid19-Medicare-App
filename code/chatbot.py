"""
Covid ChatBot Module
"""

# imports
import os

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
import nltk
from nltk.stem import WordNetLemmatizer

# nltk.download('punkt')
# nltk.download('wordnet')

lemmatizer = WordNetLemmatizer()
import pickle
import numpy as np
import tensorflow as tf

model = tf.keras.models.load_model('CovidChatBot.h5')
import json
import random
# Creating GUI with tkinter
from tkinter import *

intents = json.loads(open('../data/covid_intents.json').read())
words = pickle.load(open('../data/words.pkl', 'rb'))
classes = pickle.load(open('../data/classes.pkl', 'rb'))


def clean_up_sentence(sentence):
    # tokenize the pattern - split words into array
    sentence_words = nltk.word_tokenize(sentence)
    # stem each word - create short form for word
    sentence_words = [lemmatizer.lemmatize(word.lower()) for word in sentence_words]
    return sentence_words


# return bag of words array: 0 or 1 for each word in the bag that exists in the sentence

def bow(sentence, words, show_details=True):
    # tokenize the pattern
    sentence_words = clean_up_sentence(sentence)
    # bag of words - matrix of N words, vocabulary matrix
    bag = [0] * len(words)
    for s in sentence_words:
        for i, w in enumerate(words):
            if w == s:
                # assign 1 if current word is in the vocabulary position
                bag[i] = 1
                if show_details:
                    print("found in bag: %s" % w)
    return (np.array(bag))


def predict_class(sentence, model):
    # filter out predictions below a threshold
    p = bow(sentence, words, show_details=False)
    res = model.predict(np.array([p]))[0]
    ERROR_THRESHOLD = 0.25
    results = [[i, r] for i, r in enumerate(res) if r > ERROR_THRESHOLD]
    # sort by strength of probability
    results.sort(key=lambda x: x[1], reverse=True)
    return_list = []
    for r in results:
        return_list.append({"intent": classes[r[0]], "probability": str(r[1])})
    return return_list


def getResponse(ints, intents_json):
    tag = ints[0]['intent']
    list_of_intents = intents_json['intents']
    for i in list_of_intents:
        if (i['tag'] == tag):
            result = random.choice(i['responses'])
            break
    return result


def chatbot_response(msg):
    ints = predict_class(msg, model)
    res = getResponse(ints, intents)
    return res


def send():
    msg = EntryBox.get("1.0", 'end-1c').strip()
    EntryBox.delete("0.0", END)

    # if msg == '':
    #     ChatLog.config(state=NORMAL)
    #
    #     # res = chatbot_response(msg)
    #     ChatLog.insert(END, "Bot: " + 'dfgdfgdfgdf' + '\n\n')
    #
    #     ChatLog.config(state=DISABLED)
    #     ChatLog.yview(END)

    if msg != '':
        ChatLog.config(state=NORMAL)
        ChatLog.insert(END, "You: " + msg + '\n\n')
        ChatLog.config(foreground="#442265", font=("Verdana", 12))

        res = chatbot_response(msg)
        ChatLog.insert(END, "Bot: " + res + '\n\n')

        ChatLog.config(state=DISABLED)
        ChatLog.yview(END)


base = Tk()
base.title("Bot")
base.geometry("450x550")
base.resizable(width=FALSE, height=FALSE)

# Create Chat window
ChatLog = Text(base, bd=0, bg="white", height="8", width="50", font="Arial", wrap=WORD)
ChatLog.config(state=NORMAL)
ChatLog.config(foreground="#442265", font=("Verdana", 12))
ChatLog.insert(END, 'Bot: Hi, I’m Covid Medicare Virtual Assistant.How can I help you today?' + '\n\n')
ChatLog.config(state=DISABLED)

# Bind scrollbar to Chat window
scrollbar = Scrollbar(base, command=ChatLog.yview, cursor="heart")
ChatLog['yscrollcommand'] = scrollbar.set

# Create Button to send message
SendButton = Button(base, font=("Arial", 12, 'bold'), text="Send", width="10", height=3,
                    bd=0, bg="#32de97", activebackground="#3c9d9b", fg='#ffffff',
                    command=send)

# Create the box to enter message
EntryBox = Text(base, bd=0, bg="white", width="29", height="3", font="Arial")
# EntryBox.bind("<Return>", send)

# Place all components on the screen
scrollbar.place(x=425, y=6, height=386)
ChatLog.place(x=6, y=10, height=450, width=420)
EntryBox.place(x=6, y=470, height=70, width=300)
SendButton.place(x=320, y=470, height=70)

base.mainloop()
