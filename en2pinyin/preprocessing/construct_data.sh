#!/usr/bin/env bash
# How to use: run "bash construct_data.sh source_file target_file"
# Will generate 6 files, 2 each for train/valid/test

export PR_ROOT=`cd "$(dirname "$0")" && pwd`

# MOSES settings
# Need the contents of https://github.com/moses-smt/mosesdecoder/tree/master/scripts/tokenizer to a local folder
tokenizer_home=$PR_ROOT/tokenizer
t_dir=$OUT_DIR
punctuation=$tokenizer_home/normalize-punctuation.perl
tokenizer=$tokenizer_home/tokenizer.perl
lowercase=$tokenizer_home/lowercase.perl

echo " ---> Running MOSES scripts..."
for target in $1 $2
do
    echo "Normalize punctuation of $target..."
    perl $punctuation -l en < $target > $target.tok
    echo "Tokenize $target.tok..."
    perl $tokenizer -l en < $target.tok > $target.tmp
    echo "Lowercase $target.tmp..."
    perl $lowercase -l en < $target.tmp > $target.tok
    rm $target.tmp
done

### Final filtering of data, and split into train/valid/test
echo ' ---> Filter and split into train/valid/test...'
python $PR_ROOT/filter_split.py $1.tok $2.tok

echo ' ---> Finished!'