#!/usr/bin/python3  
# -*- coding: utf-8 -*-
# @Time    : 2021-05-06 13:18
# @Author  : Jiaxiang.Dong
# @Site    : 
# @File    : main.py
# @Email   : dongjx@nbjl.nankai.edu.cn


import numpy as np
from nltk import word_tokenize
import heapq
# from flask import Flask, jsonify, request, Response
# from app import app
from conceptnet.data_load import word2vec
import conceptnet.text_to_uri as text_to_uri

Conceptnet_match_thresholds=80

def cos_sim(vector_a, vector_b):
    """
    计算两个向量之间的余弦相似度
    :param vector_a: 向量 a
    :param vector_b: 向量 b
    :return: sim
    """

    vector_a = np.mat(vector_a)
    vector_b = np.mat(vector_b)
    num = float(vector_a * vector_b.T)
    denom = np.linalg.norm(vector_a) * np.linalg.norm(vector_b)
    sim = num / denom
    return sim


def find_top_similar_words(word2vec, words, top_num=50):

    result_dic = {}

    for wd in words:
        concept = text_to_uri.standardized_uri("en", wd)

        # emb = word2vec.get(concept, np.zeros(300))
        if concept in word2vec:
            emb = word2vec.get(concept, np.zeros(300))
        else:
            # print("{} not found in ConceptNet".format(wd))
            result_dic[wd] = None
            continue

        result_lst = []

        for k, v in word2vec.items():
            score = cos_sim(emb, v)
            tmp_dict = {'word': k, 'score': score, 'vec': v}
            result_lst.append(tmp_dict)

        candidate_word = heapq.nlargest(top_num, result_lst, key=lambda s: s['score'])

        result_dic[wd] = candidate_word

    return result_dic


def match_table_column(word2vec, top_similar_words, table_columns):

    result = {}

    for real_wd, similar_wd in top_similar_words.items():

        if similar_wd is None:
            result[real_wd] = None
            continue

        every_wd_lst = []
        for real_column_name in table_columns:
            real2concept = text_to_uri.standardized_uri("en", real_column_name)

            top_score = -1000
            top_candidate2concept = None

            for candidate2concept in similar_wd:

                real2concept_vec = word2vec.get(real2concept, np.zeros(300))
                candidate2concept_vec = candidate2concept['vec']
                score = cos_sim(candidate2concept_vec, real2concept_vec)

                if score > top_score:
                    top_score = score
                    top_candidate2concept = candidate2concept['word']

            tmp_itm = {'column': real_column_name, 'score': top_score, 'candidate_concept': top_candidate2concept}
            every_wd_lst.append(tmp_itm)

        every_wd_lst = sorted(every_wd_lst, key=lambda x: x['score'], reverse=True)

        result[real_wd] = every_wd_lst

    return result

# @app.route('/v1.0/word2column', methods=['GET', 'POST'], strict_slashes=False)
def word2column(words,table_columns):
    attributes=[]
    top_similar_words = find_top_similar_words(word2vec, words)
    result = match_table_column(word2vec, top_similar_words, table_columns)
    for col in words:
        if not result[col] is None:
             for item in result[col]:
                 if item['score']>Conceptnet_match_thresholds:
                     attributes.append(item['column']) 
    return attributes


# if __name__ == '__main__':
    # app.run(port=5001, host='0.0.0.0', threaded=True)
    
# words=["year","age","year_age"]
# table_columns=["years","birth"]
# print(word2column(words, table_columns))