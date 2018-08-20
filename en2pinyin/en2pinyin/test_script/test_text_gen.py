"""Text Generation Test.


The example is taken from mineshmathew's char_rnn_karpathy_keras

Author: Yuhuang Hu
Email : duguyue100@gmail.com
"""
from __future__ import print_function
from time import sleep
import sys
import os

from keras.models import Sequential
from keras.layers import Dense, Activation, Dropout
from keras.layers import LSTM, TimeDistributed
import numpy as np

import en2pinyin as e2p

text = open(os.path.join(e2p.E2P_DATA_PATH, "py",
                         "wb_poem.wb")).read().lower()
print ('corpus length:', len(text))

chars = sorted(list(set(text)))
print('total chars:', len(chars))
char_indices = dict((c, i) for i, c in enumerate(chars))
indices_char = dict((i, c) for i, c in enumerate(chars))

maxlen = 150
step = 1
sentences = []
next_chars = []
for i in range(0, len(text) - maxlen+1, step):
    sentences.append(text[i: i + maxlen])
    next_chars.append(text[i+1:i+1+maxlen])
print('nb sequences:', len(sentences))

print('Vectorization...')
X = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)
y = np.zeros((len(sentences), maxlen, len(chars)), dtype=np.bool)

for i, sentence in enumerate(sentences):
    for t, char in enumerate(sentence):
        X[i, t, char_indices[char]] = 1

for i, sentence in enumerate(next_chars):
    for t, char in enumerate(sentence):
        y[i, t, char_indices[char]] = 1

print ('vetorization completed')

print('Build model...')
model = Sequential()
# model.add(LSTM(512, return_sequences=True,
#                input_shape=(maxlen, len(chars))))
# original one
# minesh witout specifying the input_length
model.add(LSTM(512, input_dim=len(chars), return_sequences=True))
model.add(LSTM(512, return_sequences=True))
model.add(LSTM(512, return_sequences=True))
model.add(Dropout(0.2))
model.add(TimeDistributed(Dense(len(chars))))
model.add(Activation('softmax'))

model.compile(loss='categorical_crossentropy', optimizer='rmsprop')

print ('model is made')

# train the model, output generated text after each iteration

print (model.summary())

for iteration in range(1, 30):
    print()
    print('-' * 50)
    print('Iteration', iteration)
    history = model.fit(X, y, batch_size=128, nb_epoch=1, verbose=0)
    sleep(0.1)
    print ('loss is')
    print (history.history['loss'][0])
    print (history)

out_doc = open(os.path.join(e2p.E2P_DATA_PATH, "py", "gen_test_2.wb"), "wb")
seed_string = "mq"
print ("seed string -->", seed_string)
print ('The generated text is')
sys.stdout.write(seed_string)
out_doc.write(seed_string)
#  x=np.zeros((1, len(seed_string), len(chars)))
num_sec = 0
while num_sec < 40:
    x = np.zeros((1, len(seed_string), len(chars)))
    for t, char in enumerate(seed_string):
        x[0, t, char_indices[char]] = 1.
    preds = model.predict(x, verbose=0)[0]
    #  print (np.argmax(preds[7]))
    next_index = np.argmax(preds[len(seed_string)-1])

    #  next_index=np.argmax(preds[len(seed_string)-11])
    #  print (preds.shape)
    #  print (preds)
    #  next_index = sample(preds, 1) #diversity is 1
    next_char = indices_char[next_index]
    if len(seed_string) > 100:
        seed_string = seed_string[1:]+next_char
    else:
        seed_string = seed_string+next_char

    if next_char == ".":
        num_sec += 1

    #  print (seed_string)
    #  print ('##############')
    #  if i==40:
    #      print ('####')
    sys.stdout.write(next_char)
    out_doc.write(next_char)

sys.stdout.flush()
out_doc.flush()

out_doc.close()
