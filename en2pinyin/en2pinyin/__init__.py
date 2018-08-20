# -*- encoding: utf-8 -*-
"""Initialization file for en2pinyin package.

Author: Yuhuang Hu
Email : duguyue100@gmail.com
"""

import os
from os.path import join

E2P_PATH = os.environ["EN2PINYIN_PATH"]
E2P_DATA_PATH = join(E2P_PATH, "data")
E2P_EN_DATA_PATH = join(E2P_DATA_PATH, "en")  # English data
E2P_CN_DATA_PATH = join(E2P_DATA_PATH, "cn")  # Chinese character data
E2P_PY_DATA_PATH = join(E2P_DATA_PATH, "py")  # Chinese character encodings

E2P_PACKAGE_PATH = os.path.dirname(os.path.abspath(__file__))
E2P_PACKAGE_DATA_PATH = join(E2P_PACKAGE_PATH, "e2p_data")
E2P_PACKAGE_DICT_PATH = join(E2P_PACKAGE_DATA_PATH, "dict")
E2P_CH_WUBI_PATH = join(E2P_PACKAGE_DICT_PATH, "chinese_wubi")
E2P_WUBI_CH_PATH = join(E2P_PACKAGE_DICT_PATH, "wubi_chinese")

# Create necessary folder structure

if not os.path.isdir(E2P_PATH):
    os.makedirs(E2P_PATH)

if not os.path.isdir(E2P_DATA_PATH):
    os.makedirs(E2P_DATA_PATH)

if not os.path.isdir(E2P_CN_DATA_PATH):
    os.makedirs(E2P_CN_DATA_PATH)

if not os.path.isdir(E2P_EN_DATA_PATH):
    os.makedirs(E2P_EN_DATA_PATH)

if not os.path.isdir(E2P_PY_DATA_PATH):
    os.makedirs(E2P_PY_DATA_PATH)

# Dictionary of Chinese punctuation to English one

CH2EN_PUNC = {ord(f): ord(t)
              for f, t in zip(
                  u'，。！？【】（）％＃＠＆１２３４５６７８９０；：',
                  u',.!?[]()%#@&1234567890;:')}
EN2CH_PUNC = {ord(f): ord(t)
              for f, t in zip(
                  u',.!?[]()%#@&1234567890;:',
                  u'，。！？【】（）％＃＠＆１２３４５６７８９０；：')}
