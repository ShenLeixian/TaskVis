import tensorflow as tf
from tensorflow import keras
import numpy as np
import random
import pandas as pd
from keras import losses
import pickle
import nltk
from nltk.stem import WordNetLemmatizer 
from nltk.corpus import stopwords 
import json
import random
from sklearn.feature_extraction.text import TfidfVectorizer

language="cn"
if language=="en":
    task_json="./model/task_en.json"
    stop_words = set(stopwords.words('english'))
elif language=="cn":
    task_json="./model/task_cn.json"
    stop_words = set([line.strip() for line in open('./model/stopwords_zn/cn_stopwords.txt',encoding='UTF-8').readlines()])

lemmatizer = WordNetLemmatizer() 
NGRAM_RANGE = (1, 2)
TOP_K = 20000
TOKEN_MODE = 'word'
kwargs = {
        'ngram_range': NGRAM_RANGE,  # Use 1-grams + 2-grams.
        'dtype': 'int32',
        'strip_accents': 'unicode',
        'decode_error': 'replace',
        'analyzer': TOKEN_MODE,  # Split text into word tokens.
}

vectorizer = TfidfVectorizer(**kwargs)


def preprocess_data():
    with open(task_json,encoding='UTF-8') as file:
        data = json.load(file)

    labels = []
    patterns_text = []
    patterns_label = []

    for intent in data["intents"]:
        for pattern in intent["patterns"]:
            lemmatized = [ lemmatizer.lemmatize(w.lower()) for w in  nltk.word_tokenize(pattern) if (w != "?" and w not in stop_words)]
            patterns_text.append(' '.join(lemmatized))
            patterns_label.append(intent["tag"])
        
        if intent["tag"] not in labels:
            labels.append(intent["tag"])

    training = vectorizer.fit_transform(patterns_text).toarray()
    labels = sorted(labels)
    output = []
    out_empty = [0 for _ in range(len(labels))]

    for x, patter in enumerate(patterns_text):
        output_row = out_empty[:]
        output_row[labels.index(patterns_label[x])] = 1

        output.append(output_row)

    return training, output, labels, data


training, output, labels, data = preprocess_data()
print(labels)
training = np.array(training)
output = np.array(output)
model = keras.Sequential([
    keras.layers.Dense(len(output[1]), input_shape=(len(training[1]),)),
    keras.layers.Dense((2/3 * (len(training[1]))) + len(output[1]), activation='relu'),
    keras.layers.Dense(len(output[1]), activation="softmax")
])

# model.compile(optimizer="adam", loss=losses.CategoricalCrossentropy(from_logits=True), metrics=["accuracy"])
# # model.compile(optimizer="adam", loss=tf.losses.softmax_cross_entropy, metrics=["accuracy"])
# model.fit(training, output, epochs=500)

# model.save("./model/task_model_cn.h5")
# pickle.dump(vectorizer, open("./model/feature_cn.pickle", "wb"))


















# tag = ""
# while tag != "###":
#     user_input = input("User: ")
#     transformed, lemmatized_user_input = data_handler.handle_predict_data(user_input)
#     results = model.predict(transformed)
#     results_index = np.argmax(results)
#     tag = labels[results_index]
#     print(tag)
#     temp_products = []

    # if tag == "price" or tag == "images":
    #     for index, row in products.iterrows():
    #         if str(row["brand"]).lower() in str(lemmatized_user_input[0]):
    #             temp_products.append(row["name"])
    #     print("Robot: We have these available options, please select one:\n")
    #     for idx, product in enumerate(temp_products):
    #         print(str(idx) + ": " + product)
    #     product = products[products.name == temp_products[int(input("Choose a number: "))]]
    #     if tag == "price":
    #         print(str(product["prices.amountMin"].values[0]) + str(product["prices.currency"].values[0]) + " - " + str(product["prices.amountMax"].values[0]) + str(product["prices.currency"].values[0]))
    #     else:
    #         print("Image URL:" + str(product["imageURLs"].values[0]))
    #     print("You can find them here: " + str(product["prices.sourceURLs"].values[0]))
    # else:
    #     for intent in data["intents"]:
    #         if intent["tag"] == tag:
    #             print("Robot: " + random.choice(intent['responses']))
        
