"""Some testing script for utils module.

Author: Yuhuang Hu
Email : duguyue100@gmail.com
"""

from __future__ import print_function
import en2pinyin.utils as utils

print ("[MESSAGE] Loading dictionary")
ch2wubi_dict = utils.load_ch_wubi_dict()
ch2wubi_res, wubi2ch_res = utils.build_chinese_wubi_dict(ch2wubi_dict)
print ("[MESSAGE] The dictionaries are converted. Start saving...")

# save the dictionary.
utils.save_dict(ch2wubi_res, "chinese_to_wubi_unique.pkl")
utils.save_dict(wubi2ch_res, "wubi_to_chinese_unique.pkl")

print ("[MESSAGE] The translated dictionary is saved.")
