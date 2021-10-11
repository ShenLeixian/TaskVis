#!/usr/bin/python3  
# -*- coding: utf-8 -*-
# @Time    : 2021-05-06 13:14
# @Author  : Jiaxiang.Dong
# @Site    : 
# @File    : data_load.py
# @Email   : dongjx@nbjl.nankai.edu.cn

from itertools import islice
from numpy import asarray


def load_word2vec(pkl_path):

    word2vec = dict()

    f = open(pkl_path,encoding='utf-8')

    for line in islice(f, 1, None):

        if '/' in line and line.split('/')[2] != 'en':
            continue

        values = line.split()
        word = values[0]
        coefs = asarray(values[1:], dtype='float32')
        word2vec[word] = coefs
    f.close()

    return word2vec


word2vec = load_word2vec("../jars/numberbatch.txt")