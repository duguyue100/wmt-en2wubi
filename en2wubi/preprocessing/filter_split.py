# -*- coding: utf-8 -*-
"""
Filter, shuffle and display statistics about data.
Split into train/valid/test.
"""

import importlib
import linecache
import logging
import pickle
import re
import subprocess
import sys

importlib.reload(sys)
# sys.setdefaultencoding('utf8')

import numpy as np

logging.basicConfig(format='%(asctime)s : %(levelname)s : %(message)s', level=logging.INFO)

REGEX_DICT = {
    "([a-zA-Z0-9])([\\\,\:`\?!\/\'\‘\’\"\-])(\s|$)": r"\1 \2 \3",  # handle i.e.: "text,"
    ";s ": r"; ",
    "&[#\da-zA-Z]*;": "",  # Remove stuff like &apos;
    " ([\.\,\:\-\?!\\\/`\'\‘\’\"])([a-zA-Z0-9]+) ": r" \2 ",  # handle ".text"
    "\d": r"#",  # Replace all digits with #
    "[ \t\r\f]{1,}": r" "  # replace all spaces and tabs with a single space
}

# Split size of train/valid/test
TRAIN_SIZE = 0.95
VALID_SIZE = 0.025
TEST_SIZE = 0.025

## Length restrictions
MIN_SOURCE_LEN = 5
MAX_SOURCE_LEN = 50
MIN_TARGET_LEN = 5
MAX_TARGET_LEN = 50


def file_len(fname):
    p = subprocess.Popen(['wc', '-l', fname], stdout=subprocess.PIPE,
                         stderr=subprocess.PIPE)
    result, err = p.communicate()
    if p.returncode != 0:
        raise IOError(err)
    return int(result.strip().split()[0])


def wc(f):
    if type(f) is list:
        return tuple([file_len(subf) for subf in f])
    elif type(f) is str:
        return file_len(f)
    else:
        raise Exception


def final_filtering(txt):
    for match, replace in REGEX_DICT.items():
        txt = re.sub(re.compile(match), replace, txt)
        re.purge()
    txt = txt.strip(' \t\n\r')
    return txt + "\n"


def check_size(text, target="source"):
    word_len = len(text.split(" "))
    if target == "source":
        if not MIN_SOURCE_LEN < word_len < MAX_SOURCE_LEN:
            return False
    elif target == "target":
        if not MIN_TARGET_LEN < word_len < MAX_TARGET_LEN:
            return False
    return True


class DataStat:
    def __init__(self):
        self.target_word_counts = []
        self.source_word_counts = []
        self.outside_limits = 0


if __name__ == '__main__':
    source_file_path = sys.argv[1]
    target_file_path = sys.argv[2]

    logging.info("Filtering files: " + source_file_path + " " + target_file_path)
    source_linecount, target_linecount = wc([source_file_path, target_file_path])

    try:
        assert source_linecount == target_linecount
        logging.info("{} files in total.".format(source_linecount))
    except AssertionError:
        logging.error("Files don't have the same lengths. \n" + source_file_path + ": " + str(
            source_linecount) + "\n" + target_file_path + ": " + str(target_linecount))
        raise AssertionError

    train_limit = round(TRAIN_SIZE * source_linecount)
    val_limit = round(VALID_SIZE * source_linecount) + train_limit
    test_limit = source_linecount
    # Shuffle files
    line_sequence = np.arange(start=1, stop=source_linecount)
    shuffled_sequence = np.copy(line_sequence)
    np.random.shuffle(shuffled_sequence)
    assert len(np.unique(line_sequence)) == len(np.unique(shuffled_sequence))
    # Open output files
    article_tok_filter_train = open(source_file_path + ".train.txt", "w")
    title_tok_filter_train = open(target_file_path + ".train.txt", "w")
    article_tok_filter_val = open(source_file_path + ".valid.txt", "w")
    title_tok_filter_val = open(target_file_path + ".valid.txt", "w")
    article_tok_filter_test = open(source_file_path + ".test.txt", "w")
    title_tok_filter_test = open(target_file_path + ".test.txt", "w")

    # Store some statistics about dataset
    data_stat = DataStat()
    max_article_length = 0
    # Total number of files written so far
    total_pairs_written = 0

    ind = 0
    tra_ids = shuffled_sequence[0:train_limit - 1]
    val_ids = shuffled_sequence[train_limit:val_limit - 1]
    tes_ids = shuffled_sequence[val_limit:]

    for ind, line_number in enumerate(shuffled_sequence):
        article_text = linecache.getline(source_file_path, line_number)
        title_text = linecache.getline(target_file_path, line_number)
        if ind % int(float(source_linecount) / 100) == 0:
            logging.info("Filtered {}% of lines...".format(np.round((float(ind) * 100.) / source_linecount, 2)))

        # Compute statistics
        data_stat.target_word_counts.append(len(title_text.split()))
        data_stat.source_word_counts.append(len(article_text.split()))

        if not check_size(article_text) or not check_size(title_text, target="target"):
            data_stat.outside_limits += 1
        else:  # Include data point in final dataset
            article_text_f = final_filtering(article_text)
            title_text_f = final_filtering(title_text)
            total_pairs_written += 1
            # Figure out to which dataset the data point belongs to
            if ind in tra_ids:
                article_tok_filter_train.write(article_text_f)
                title_tok_filter_train.write(title_text_f)
                continue
            elif ind in val_ids:
                article_tok_filter_val.write(article_text_f)
                title_tok_filter_val.write(title_text_f)
                continue
            elif ind in tes_ids:
                article_tok_filter_test.write(article_text_f)
                title_tok_filter_test.write(title_text_f)
                continue

    article_tok_filter_train.close()
    title_tok_filter_train.close()
    article_tok_filter_val.close()
    title_tok_filter_val.close()
    article_tok_filter_test.close()
    title_tok_filter_test.close()
    pickle.dump(data_stat, open("stat.p", "wb"))

    if not total_pairs_written == source_linecount - data_stat.outside_limits:
        logging.error("Numbers don't add...\nOriginal:\t{}\tWritten:\t{}\tExcluded:\t{}\n".format(source_linecount,
                                                                                                  total_pairs_written,
                                                                                                  data_stat.outside_limits))
    # Check if final line numbers add up
    train_source_linecount, train_target_linecount = wc([source_file_path + ".train.txt",
                                                         target_file_path + ".train.txt"])

    if not train_source_linecount == train_target_linecount:
        logging.error("Mismatch between line counts. \n"
                      "article: {}\ttitle: {}".format(train_source_linecount, train_target_linecount))

    ### Print statistics about dataset
    logging.info("-" * 40)
    logging.info("Total number of sentences excluded: {}".format(data_stat.outside_limits))
    logging.info("Final num of lines: " + str(total_pairs_written))
    logging.info(
        "Source (abstract) stat: Min length: {}\t Max: {}\t Avg: {}".format(np.min(data_stat.source_word_counts),
                                                                            np.max(data_stat.source_word_counts),
                                                                            np.average(data_stat.source_word_counts)))
    logging.info("Target (title) stat: Min length: {}\t Max: {}\t Avg: {}".format(np.min(data_stat.target_word_counts),
                                                                                  np.max(data_stat.target_word_counts),
                                                                                  np.average(
                                                                                      data_stat.target_word_counts)))
    logging.info("-" * 40)
