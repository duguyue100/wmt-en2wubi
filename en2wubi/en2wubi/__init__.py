# -*- encoding: utf-8 -*-
"""Initialization file for en2wubi package.

Author: Yuhuang Hu
Email : duguyue100@gmail.com
"""

import os
from os.path import join

E2W_PATH = os.environ["EN2WUBI_PATH"]
E2W_DATA_PATH = join(E2W_PATH, "data")
E2W_EN_DATA_PATH = join(E2W_DATA_PATH, "en")  # English data
E2W_CN_DATA_PATH = join(E2W_DATA_PATH, "cn")  # Chinese character data
E2W_PY_DATA_PATH = join(E2W_DATA_PATH, "wb")  # Chinese character encodings

E2W_PACKAGE_PATH = os.path.dirname(os.path.abspath(__file__))
E2W_PACKAGE_DATA_PATH = join(E2W_PACKAGE_PATH, "e2w_data")
E2W_PACKAGE_DICT_PATH = join(E2W_PACKAGE_DATA_PATH, "dict")
E2W_CH_WUBI_PATH = join(E2W_PACKAGE_DICT_PATH, "chinese_wubi")
E2W_WUBI_CH_PATH = join(E2W_PACKAGE_DICT_PATH, "wubi_chinese")

# Create necessary folder structure

if not os.path.isdir(E2W_PATH):
    os.makedirs(E2W_PATH)

if not os.path.isdir(E2W_DATA_PATH):
    os.makedirs(E2W_DATA_PATH)

if not os.path.isdir(E2W_CN_DATA_PATH):
    os.makedirs(E2W_CN_DATA_PATH)

if not os.path.isdir(E2W_EN_DATA_PATH):
    os.makedirs(E2W_EN_DATA_PATH)

if not os.path.isdir(E2W_PY_DATA_PATH):
    os.makedirs(E2W_PY_DATA_PATH)

# Dictionary of Chinese punctuation to English one

CH2EN_PUNC = {ord(f): ord(t)
              for f, t in zip(
                  u'，。！？【】（）％＃＠＆１２３４５６７８９０；：',
                  u',.!?[]()%#@&1234567890;:')}
EN2CH_PUNC = {ord(f): ord(t)
              for f, t in zip(
                  u',.!?[]()%#@&1234567890;:',
                  u'，。！？【】（）％＃＠＆１２３４５６７８９０；：')}
