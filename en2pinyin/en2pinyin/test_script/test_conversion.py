"""Try out Chinese - Wubi Conversion.

Author: Yuhuang Hu
Email : duguyue100@gmail.com
"""

import os

import en2pinyin as e2p
from en2pinyin import utils

in_doc = utils.read_doc(os.path.join(e2p.E2P_CN_DATA_PATH, "cn_shiji2.cn"))
out_doc = utils.write_doc(os.path.join(e2p.E2P_DATA_PATH,
                                       "py", "wb_shiji2.wb"))

ch2wubi_dict = utils.load_ch_wubi_dict(
                    os.path.join(e2p.E2P_PACKAGE_DICT_PATH,
                                 "chinese_to_wubi_unique.pkl"))

wubi2ch_dict = utils.load_wubi_ch_dict(
                    os.path.join(e2p.E2P_PACKAGE_DICT_PATH,
                                 "wubi_to_chinese_unique.pkl"))

# Convert from Chinese to Wubi

utils.chinese_wubi(in_doc, out_doc, ch2wubi_dict)

in_doc = utils.read_doc(os.path.join(e2p.E2P_DATA_PATH, "py", "gen_test_2.wb"))
out_doc = utils.write_doc(os.path.join(e2p.E2P_DATA_PATH,
                                       "py", "gen_test_2.cn"))

# convert from Wubi to Chinese

utils.wubi_chinese(in_doc, out_doc, wubi2ch_dict)
