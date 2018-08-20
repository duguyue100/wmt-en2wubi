"""Some investigation on Chinese Wubi Dictionary.

Author: Yuhuang Hu
Email : duguyue100@gmail.com
"""

import os

import en2pinyin as e2p
from en2pinyin import utils


def is_ascii(s):
    return all(ord(c) < 128 for c in s)

ch2wubi_dict = utils.load_ch_wubi_dict(
                    os.path.join(e2p.E2P_PACKAGE_DICT_PATH,
                                 "chinese_to_wubi_unique.pkl"))

wubi2ch_dict = utils.load_wubi_ch_dict(
                    os.path.join(e2p.E2P_PACKAGE_DICT_PATH,
                                 "wubi_to_chinese_unique.pkl"))

# checking chinese to wubi
print ("Checking Chinese to Wubi")
for key, value in ch2wubi_dict.iteritems():
    if is_ascii(value) is False:
        print key, value

# checking wubi to chinese
print ("Checking Wubi to Chinese")
for key, value in wubi2ch_dict.iteritems():
    if is_ascii(key) is False:
        print key, value
