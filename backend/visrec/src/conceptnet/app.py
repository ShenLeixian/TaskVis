#!/usr/bin/python3  
# -*- coding: utf-8 -*-
# @Time    : 2021-05-06 13:51
# @Author  : Jiaxiang.Dong
# @Site    : 
# @File    : app.py
# @Email   : dongjx@nbjl.nankai.edu.cn

from flask import Flask
from flask_cors import *  #导入模块

app = Flask(__name__)
CORS(app, supports_credentials=True)  # 设置允许跨域
app.config['DEBUG'] = True