# wmt-en2wubi
Code and data for [Character-level Chinese-English Translation through ASCII Encoding](https://arxiv.org/abs/1805.03330). 

# Cite the paper

```
@inproceedings{en2wubi,
    author = {{Nikolov}, N.~I. and {Hu}, Y. and {Xue Tan}, M. and {Hahnloser}, R.~H.~R.},
    title = {{Character-level Chinese-English Translation through ASCII Encoding}},
    booktitle = {Third Conference on Machine Translation (WMT18)},
    year = {2018},
    address = {Brussels, Belgium}
}
```

## Training/Evaluation Data and Results

The data used to produce the paper and model results is available [here](https://drive.google.com/open?id=12BJ2oKPxO7PBUW6qjJFhQ6447ghwmU9H).

## Converting Chinese to Wubi 

To convert your data from Chinese to Wubi, follow the instructions in the [en2wubi](./en2wubi) package.

## Instructions for reproducing the results

### Word- and subword- level 

Follow the instructions in the [Fairseq library](https://github.com/pytorch/fairseq) for preprocessing, training and evaluation. To train the same LSTM model that we use the paper, pass `--arch lstm` to `train.py`; for the FConv model pass `--arch fconv_iwslt_de_en`. 

On the subword-level, you need to additionally learn and apply subword segmentation rules on the dataset. We use the [subword-nmt](https://github.com/rsennrich/subword-nmt) library for subword segmentation. 

### Character-level 

Follow the instructions in [this repository](https://github.com/nyu-dl/dl4mt-c2c) for preprocessing and train a bilingual char2char model using `char2char/train_bi_char2char.py`. 

### Evaluation 

To compute BLEU, download and run [multi-bleu.perl](https://github.com/moses-smt/mosesdecoder/blob/master/scripts/generic/multi-bleu.perl) as: 

```
perl multi-bleu.perl reference.txt < model_output.txt
```

When evaluating *en2wb* vs. *en2cn*, you can use our scripts to convert the Chinese results to Wubi before computing BLEU, to make the scores more comparable.  

## Contacts

Nikola I. Nikolov and Yuhuang Hu
