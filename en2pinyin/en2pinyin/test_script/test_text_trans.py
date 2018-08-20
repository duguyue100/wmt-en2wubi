"""Test text translation.

Chinese To English.

Author: Yuhuang Hu
Email : duguyue100@gmail.com
"""
from __future__ import print_function
import os
import cPickle as pickle

import numpy as np
from keras.models import Sequential
from keras.layers import Activation
from keras.callbacks import EarlyStopping, ModelCheckpoint
import seq2seq
from seq2seq.models import Seq2Seq

import en2pinyin as e2p

# prepare English and Chinese texts
eng_text = open(os.path.join(e2p.E2P_EN_DATA_PATH,
                             "en_news_mag.en")).read().lower()

print ("[MESSAGE] English Text Length: ", len(eng_text))

wb_text = open(os.path.join(e2p.E2P_PY_DATA_PATH,
                            "wb_news_mag.wb")).read().lower()

print ("[MESSAGE] Encoding Text Length: ", len(wb_text))

eng_chars = sorted(list(set(eng_text)))
print ("[MESSAGE] Total English chars: ", len(eng_chars))

wb_chars = sorted(list(set(wb_text)))
print ("[MESSAGE] Total Chinese chars: ", len(wb_chars))

input_dim = len(eng_chars)  # WB encoding as input
output_dim = len(wb_chars)  # ENG as output

# Char index
eng_char_idx = dict((c, i) for i, c in enumerate(eng_chars))
eng_idx_char = dict((i, c) for i, c in enumerate(eng_chars))

wb_char_idx = dict((c, i) for i, c in enumerate(wb_chars))
wb_idx_char = dict((i, c) for i, c in enumerate(wb_chars))

# Sentences

eng_sen = eng_text.split("\n")
wb_sen = wb_text.split("\n")

eng_sen = eng_sen[:-1]
wb_sen = wb_sen[:-1]

# select only 200 and lower sentences because of dimensionality
# based on input sequences
MAX_CHAR = 250

eng_sen_selected = []
wb_sen_selected = []
max_len_eng = 0
max_len_wb = 0

for i in xrange(len(eng_sen)):
    if len(eng_sen[i]) < MAX_CHAR and len(wb_sen[i]) < MAX_CHAR:
        eng_sen_selected.append(eng_sen[i])
        wb_sen_selected.append(wb_sen[i])

        if len(eng_sen[i]) > max_len_eng:
            max_len_eng = len(eng_sen[i])
        if len(wb_sen[i]) > max_len_wb:
            max_len_wb = len(wb_sen[i])

# construct vector representation
X = np.zeros((len(eng_sen_selected), MAX_CHAR, len(eng_chars)), dtype=np.bool)
y = np.zeros((len(wb_sen_selected), MAX_CHAR, len(wb_chars)), dtype=np.bool)

for i, sen in enumerate(eng_sen_selected):
    for t, char in enumerate(sen):
        X[i, t, eng_char_idx[char]] = 1
    X[i, len(sen), eng_char_idx["\n"]] = 1

for i, sen in enumerate(wb_sen_selected):
    for t, char in enumerate(sen):
        y[i, t, wb_char_idx[char]] = 1
    y[i, len(sen), wb_char_idx["\n"]] = 1

train_idx = int(len(eng_sen_selected)*0.7)

# Split data
X_train = X[:train_idx]
y_train = y[:train_idx]
X_test = X[train_idx:]
y_test = y[train_idx:]

print ("[MESSAGE] Vectorization completed")

print ("[MESSAGE] Build Model...")
BATCH_SIZE = 128

model = Sequential()

model.add(Seq2Seq(input_dim=input_dim, input_length=MAX_CHAR,
                  hidden_dim=100, output_length=MAX_CHAR,
                  output_dim=output_dim, depth=4))
model.add(Activation("softmax"))

model.compile(loss="categorical_crossentropy", optimizer="rmsprop",
              metrics=["accuracy"])

model.summary()

print ("[MESSAGE] The model is built.")

early_stopping = EarlyStopping(monitor='val_loss', patience=3)
model_name = os.path.join(e2p.E2P_PATH, "trans_test")
model_name += "-{epoch:02d}-{val_acc:.2f}.hdf5"
checkpoint = ModelCheckpoint(model_name,
                             monitor='val_acc',
                             verbose=1,
                             save_best_only=True,
                             mode='max')
callbacks_list = [early_stopping, checkpoint]
history = model.fit(X_train, y_train, batch_size=BATCH_SIZE,
                    nb_epoch=200, verbose=1,
                    validation_data=(X_test, y_test),
                    callbacks=callbacks_list)
score = model.evaluate(X_test, y_test, verbose=0)
print ("[MESSAGE] The training has completed.")
print ("[MESSAGE] Test Score: %.2f" % (score[0]))
print ("[MESSAGE] Test Accuracy: %.2f" % (score[1]))
history_name = os.path.join(e2p.E2P_PATH, "trans-test.pkl")
with open(history_name, "wb") as f:
    pickle.dump(history, f, protocol=pickle.HIGHEST_PROTOCOL)
    f.close()
print ("[MESSAGE] Save training history at %s" % (history_name))
