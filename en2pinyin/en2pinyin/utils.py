# -*- encoding: utf-8 -*-
"""Handing data preprocessing and IO pipeline.

Covers

+   Dictionary Preprocessing
+   Get a statistics for dictionary
+   Data formatting
+   General IO functions

Author: Yuhuang Hu
Email : duguyue100@gmail.com
"""

from __future__ import print_function
import os
import cPickle as pickle
from future.utils import iteritems

import en2pinyin as e2p


def load_dict(dict_path):
    """Load a dictionary.

    Currently only support Wubi typing method.

    Parameters
    ----------
    dict_path : str
        the absolute path to the dictionary

    Returns
    -------
    dict : Dictonary
        a mapping between one code to another
    """
    if not os.path.isfile(dict_path):
        raise ValueError("The target dictionary is not available at %s"
                         % (dict_path))

    return pickle.load(open(dict_path, "r"))


def save_dict(target_dict, filename, save_path=e2p.E2P_PACKAGE_DICT_PATH):
    """Save a Dictionary to some path.

    Parameters
    ---------
    target_dict : Dictionary
        A dictionary that is about to dump.
    filename : str
        the name of the dictionary.
    save_path : str
        the destination of the saving path.
    """
    file_path = os.path.join(save_path, filename)
    pickle.dump(target_dict, open(file_path, "wb"))
    print ("[MESSAGE] The target dictionary is saved at %s" % (file_path))


def load_ch_wubi_dict(dict_path=e2p.E2P_CH_WUBI_PATH):
    """Load Chinese to Wubi Dictionary.

    Parameters
    ---------
    dict_path : str
        the absolute path to chinese2wubi dictionary.
        In default, it's E2P_CH_WUBI_PATH.

    Returns
    -------
    dict : Dictionary
        a mapping between Chinese to Wubi Code
    """
    return load_dict(dict_path)


def load_wubi_ch_dict(dict_path=e2p.E2P_WUBI_CH_PATH):
    """Load Wubi to Chinese Dictionary.

    Parameters
    ---------
    dict_path : str
        the absolute path to chinese2wubi dictionary.
        In default, it's E2P_WUBI_CH_PATH.

    Returns
    -------
    dict : Dictionary
        a mapping between Wubi to Chinese Code
    """
    return load_dict(dict_path)


def reverse_dict(ori_dict):
    """Reverse dictionary mapping.

    Parameters
    ----------
    ori_dict : Dictionary
        original given dictionary

    Returns
    -------
    res_dict : Dictionary
        The result dictionary with the mapping of one-to-many
    """
    res_dict = {}
    for key in ori_dict:
        if ori_dict[key] not in res_dict:
            res_dict[ori_dict[key]] = [key]
        else:
            res_dict[ori_dict[key]].append(key)

    return res_dict


def reduce_dict(ori_dict):
    """Reduce one-to-many dictionary to one-to-one dictionary.

    The scenario here is the value is a list of Chinese characters, and
    the key is the wubi code. So the ideal processing is the Chinese
    character is mapping to some wubi code + order number.

    Parameters
    ---------
    ori_dict : Dictionary
        one-to-many dictionary.

    Returns
    -------
    res_dict : Dictionary
        result one-to-one dictionary.
    """
    res_dict = {}

    for key in ori_dict:
        if len(ori_dict[key]) > 1:
            for i in xrange(len(ori_dict[key])):
                res_dict[ori_dict[key][i]] = key+str(i)
        else:
            res_dict[ori_dict[key][0]] = key

    return res_dict


def build_chinese_wubi_dict(ch2wubi_dict):
    """Build a Chinese-Wubi one-to-one mapping.

    Parameters
    ----------
    ch2wubi_dict : Dictionary
        A Chinese to Wubi Dictionary

    Returns
    -------
    ch2wubi_res : Dictionary
        Chinese to Wubi code one-to-one mapping.
    wubi2ch_res : Dictionary
        Wubi to Chinese one-to-one mapping.
    """
    reverse_map = reverse_dict(ch2wubi_dict)
    ch2wubi_res = reduce_dict(reverse_map)
    wubi2ch_res = {v: k for k, v in iteritems(ch2wubi_res)}

    return ch2wubi_res, wubi2ch_res


# The following conversion scheme is roughly following chinese_wubi
# which is originally written by arcsecw.
# And you can find the code here:
# https://github.com/arcsecw/chinese_wubi


def read_doc(file_name):
    """Read a document.

    Parameters
    ----------
    file_name : str
        The path to the document that is ready to be translate.

    Returns
    -------
    in_doc : file
        A file object that allow reading of document.
    """
    if not os.path.isfile(file_name):
        raise ValueError("The document is not available at %s" % (file_name))

    return open(file_name, "r")


def write_doc(file_name):
    """Write a converted document.

    Parameters
    ----------
    file_name : str
        The converted document.

    Returns
    -------
    out_doc : file
        A file object that allows writing of document.
    """
    return open(file_name, "wb")


def convert_line(in_line, map_dict, line_type):
    """Convert line based on a given dictionary.

    Parameters
    ----------
    in_line : str
        The line that is subject to convert.
    map_dict : Dictionary
        Dictionary that translates from one index to another.
    line_type : str
        The string type of the line.
        "ch" : Chinese
        "wb" : Wubi

    Returns
    -------
    out_line : str
        The output line.
    """
    if line_type == "ch":
        in_line = in_line.translate(e2p.CH2EN_PUNC)

        out_line = ""
        for ch_char in in_line:
            if ch_char in map_dict:
                out_line += map_dict[ch_char]
            else:
                if ch_char in u'0123456789':
                    out_line += " "
                out_line += ch_char
        return out_line
    elif line_type == "wb":
        # remove any chance there is a Chinese punctuation in there.
        in_line = in_line.translate(e2p.CH2EN_PUNC)
        out_line = ""

        for wb_word in in_line.split(" "):
            if len(wb_word) > 0:
                char_idx = 0
                for char in wb_word:
                    if (not char.isalpha()) and (not char.isnumeric()):
                        break
                    char_idx += 1
                punc = wb_word[char_idx:]
                wb_word = wb_word[:char_idx]
            else:
                punc = ""

            if u" "+wb_word in map_dict:
                out_line += map_dict[u" "+wb_word]+punc
            else:
                out_line += wb_word+punc

        return out_line.translate(e2p.EN2CH_PUNC)


def convert_doc(in_doc, out_doc, map_dict, doc_type):
    """Convert a document.

    Parameters
    ----------
    in_doc : file
        The input document
    out_doc : file
        The output document
    map_dict : Dictionary
        Dictionary that translates from one index to another.
    doc_type : str
        The string type of the document.
        "ch" : Chinese
        "wb" : Wubi
    """
    num_line = 1
    for line in in_doc.readlines():
        num_line += 1
        line = line.decode("utf-8")
        line = convert_line(line, map_dict, doc_type)
        out_doc.write(line.encode("utf-8"))
        if num_line % 1000 == 0:
            out_doc.flush()

    out_doc.close()
    in_doc.close()

    print ("[MESSAGE] The converted file is saved at "+out_doc.name)


def chinese_wubi(in_doc, out_doc, ch2wubi_dict):
    """Chinese to Wubi Conversion.

    Parameters
    ----------
    in_doc : str
        The document that is subject to convert.
    ch2wubi_dict : Dictionary
        Chinese to Wubi Dictionary.

    Returns
    -------
    out_doc : string
        The output document.
    """
    convert_doc(in_doc, out_doc, ch2wubi_dict, "ch")


def wubi_chinese(in_doc, out_doc, wubi2ch_dict):
    """Wubi to Chinese Conversion.

    Parameters
    ----------
    in_doc : str
        The document that is subject to convert.
    wubi2ch_dict : Dictionary
        Wubi to Chinese Dictionary.

    Returns
    -------
    out_doc : string
        The output document.
    """
    convert_doc(in_doc, out_doc, wubi2ch_dict, "wb")
