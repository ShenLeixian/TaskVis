import tensorflow as tf
import numpy as np
import nltk
from nltk.stem import WordNetLemmatizer 
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from nltk.corpus import stopwords 
import pickle

stop_words_en = set(stopwords.words('english'))
stop_words_cn = set([line.strip() for line in open('./NLI/model/stopwords_zn/cn_stopwords.txt',encoding='UTF-8').readlines()])
stop_words=stop_words_cn|stop_words_en

lemmatizer = WordNetLemmatizer() 

def handle_predict_data(user_input): 
    print("user input:",user_input)
    lemmatized_user_input = [' '.join([ lemmatizer.lemmatize(w.lower()) for w in nltk.word_tokenize(user_input) if (w != "?" and w not in stop_words)])]
    print("lemmatized_user_input:",lemmatized_user_input)
    # if language=="en":
    #     vectorizer_model='./NLI/model/feature_en.pickle'
    # elif language=="cn":
    #     vectorizer_model='./NLI/model/feature_cn.pickle'
    vectorizer_model='./NLI/model/feature_mix.pickle'
    vectorizer = pickle.load(open(vectorizer_model, "rb"))
    transformed = vectorizer.transform(lemmatized_user_input).toarray()
    return transformed

def DecideTask(query):
    labels=['change_over_time', 'characterize_distribution', 'cluster', 'comparison', 'compute_derived_value', 'correlate', 'determine_range', 'deviation', 'error_range', 'find_anomalies', 'find_extremum', 'magnitude', 'part_to_whole', 'retrieve_value', 'sort', 'spatial', 'trend']
    # if language=="en":
    #     labels=['change_over_time', 'characterize_distribution', 'cluster', 'comparison', 'compute_derived_value', 'correlate', 'determine_range', 'deviation', 'error_range', 'find_anomalies', 'find_extremum', 'magnitude', 'part_to_whole', 'retrieve_value', 'sort', 'spatial', 'trend']
    #     task_model="./NLI/model/task_model_en.h5"
    # elif language=="cn":
    #     labels=['偏差', '关系', '分布', '取值', '取值范围', '大小', '对比', '异常值', '排序', '推导值', '时序变化', '极值', '空间', '聚类', '误差', '趋势', '部分与整体']
    #     task_model="./NLI/model/task_model_cn.h5"
    task_model="./NLI/model/task_model_mix.h5"
    model=tf.keras.models.load_model(task_model)
    transformed = handle_predict_data(query)
    results = model.predict(transformed)
    results_index = np.argmax(results)
    task = labels[results_index]
    return task
