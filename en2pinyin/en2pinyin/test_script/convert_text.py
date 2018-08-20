"""Try out Chinese - Wubi Conversion.

Author: Yuhuang Hu
Email : duguyue100@gmail.com
"""

import os
import argparse

import en2pinyin as e2p
from en2pinyin import utils


def convert_doc(input_doc, output_doc, convert_type="ch2wb"):
    """Convert a given document by given convert type.

    Assume all the data is located at e2p.E2P_DATA_PATH

    Parameters
    ----------
    input_doc : str
        the path of the input doc
    output_doc : str
        the path of the output doc
    convert_type : str
        Chinese to Wubi: ch2wb
        Wubi to Chinese: wb2ch
    """
    # setup input and output document stream
    in_doc = utils.read_doc(os.path.join(e2p.E2P_DATA_PATH, input_doc))
    out_doc = utils.write_doc(os.path.join(e2p.E2P_DATA_PATH, output_doc))

    if convert_type == "ch2wb":
        ch2wubi_dict = utils.load_ch_wubi_dict(
            os.path.join(e2p.E2P_PACKAGE_DICT_PATH,
                         "chinese_to_wubi_unique.pkl"))
        utils.chinese_wubi(in_doc, out_doc, ch2wubi_dict)
    elif convert_type == "wb2ch":
        wubi2ch_dict = utils.load_wubi_ch_dict(
            os.path.join(e2p.E2P_PACKAGE_DICT_PATH,
                         "wubi_to_chinese_unique.pkl"))
        utils.wubi_chinese(in_doc, out_doc, wubi2ch_dict)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Convert given text from \
                                        Chinese to Wubi encoding or \
                                        Wubi to Chinese. by Yuhuang Hu")
    parser.add_argument("--input-doc", type=str,
                        help="Input document, assume data at default \
                            data folder.")
    parser.add_argument("--output-doc", type=str,
                        help="Output document, assume data at default \
                            data folder.")
    parser.add_argument("--convert-type", type=str, help="ch2wb or wb2ch")

    args = parser.parse_args()
    convert_doc(**vars(args))
