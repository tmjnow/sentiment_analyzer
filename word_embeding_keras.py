################################################################
# Data for News corpus(Bellow link might help)
# http://mpqa.cs.pitt.edu/
# http://www.anc.org/data/oanc/download/


from keras.preprocessing import sequence
from keras.models import Sequential
from keras.layers import Dense, Embedding, Masking, LSTM, Conv1D, MaxPooling1D, Flatten, Dropout, TimeDistributed, Lambda
from keras.datasets import imdb
import numpy as np
from nltk.tokenize import word_tokenize
import tensorflow as tf
from keras import backend as K

import pickle
import os
import time


print('Loading data...')
# (x_train, y_train), (x_test, y_test) = imdb.load_data(num_words=max_features)
with open('/home/john/sentiment_files/data/twitter_vocab.pkl', 'rb') as f:
    data = pickle.load(f)
print(len(data['vocab_to_index']))
vocab_to_index = data['vocab_to_index']
index_to_vocab = data['index_to_vocab']
vocab_frequency_tuple = data['vocab_frequency_tuple']
vocab_len = len(data['vocab_to_index'])
print('Vocab len: ', vocab_len)
# del data
#
# # Convert data into word vector
# max_word = 200
# train_pos_sample_dir = '/home/janmejaya/sentiment_analyzer/aclImdb/train/pos'
# train_neg_sample_dir = '/home/janmejaya/sentiment_analyzer/aclImdb/train/neg'
# test_neg_sample_dir = '/home/janmejaya/sentiment_analyzer/aclImdb/test/neg'
# test_pos_sample_dir = '/home/janmejaya/sentiment_analyzer/aclImdb/test/pos'
#
# file_list_pos = [each_file for each_file in os.listdir(train_pos_sample_dir) if os.path.isfile(os.path.join(train_pos_sample_dir, each_file))]
# file_list_neg = [each_file for each_file in os.listdir(train_neg_sample_dir) if os.path.isfile(os.path.join(train_neg_sample_dir, each_file))]
# file_list = file_list_neg + file_list_pos
#
# file_pointer = 0
# max_features = 20000
# def next_batch(batch_size, test=False):
#     # This function reads equal amount of positive and negative review depending on batch size.
#     # returns input_data of size [batch_size, max_chars]
#     #     and target_data of size [batch_size, 1]
#
#     global file_pointer, file_list_pos, file_list_neg
#     if batch_size % 2 != 0:
#         print("[ERROR]Please provide batch_size divisible by 2")
#     if test:
#         file_list_pos = [each_file for each_file in os.listdir(test_pos_sample_dir) if
#                          os.path.isfile(os.path.join(test_pos_sample_dir, each_file))]
#         file_list_neg = [each_file for each_file in os.listdir(test_neg_sample_dir) if
#                          os.path.isfile(os.path.join(test_neg_sample_dir, each_file))]
#     else:
#         file_list_pos = [each_file for each_file in os.listdir(train_pos_sample_dir) if
#                          os.path.isfile(os.path.join(train_pos_sample_dir, each_file))]
#         file_list_neg = [each_file for each_file in os.listdir(train_neg_sample_dir) if
#                          os.path.isfile(os.path.join(train_neg_sample_dir, each_file))]
#
#     pos_file_to_read = file_list_pos[file_pointer:(file_pointer + (batch_size // 2))]
#     neg_file_to_read = file_list_neg[file_pointer:(file_pointer + (batch_size // 2))]
#
#     if (file_pointer+(batch_size//2)) > len(file_list_pos):
#         file_pointer = 0
#     else:
#         file_pointer += batch_size//2
#
#     data_len_list, data_list = [], []
#     target_data = np.zeros([batch_size], dtype=np.int32)
#     input_data = np.zeros([batch_size, max_word], dtype=np.int32)
#
#     # Keep maximum frequent occurring words
#     frequent_words_tuple = sorted(vocab_frequency.items(), key=lambda x: x[1], reverse=True)[:max_features]
#     frequent_words = [val for val, freq in frequent_words_tuple]
#     print('Length of frequent words: ', frequent_words)
#
#     for index, each_file in enumerate(pos_file_to_read+neg_file_to_read):
#         print(index)
#         if test:
#             pos_dir = test_pos_sample_dir
#             neg_dir = test_neg_sample_dir
#         else:
#             pos_dir = train_pos_sample_dir
#             neg_dir = train_neg_sample_dir
#
#         try:
#             with open(os.path.join(pos_dir, each_file), 'r') as f:
#                 data = f.read()
#                 target_data[index] = 1
#         except:
#             with open(os.path.join(neg_dir, each_file), 'r') as f:
#                 data = f.read()
#         # Tokenize the data
#         tokenized_word = word_tokenize(data)
#         truncated_review = []
#         for each_word in tokenized_word:
#             # Go through each word and discard words which are not present in dictionary
#             each_word = each_word.lower()
#             # Take words which are frequent
#             if each_word in frequent_words:
#                 try:
#                     truncated_review.append(vocab_to_index[each_word])
#                     if len(truncated_review) >= max_word:
#                         break
#                 except Exception as exc:
#                     print('[Exception] if Key word not present in vocab dict but present in frequent words its a bug: {0}'.format(exc))
#         # Pad appropriately if less words are present
#         word_len = len(truncated_review)
#         if word_len < max_word:
#             truncated_review += [vocab_len] * (max_word - word_len)
#         input_data[index] = truncated_review
#
#     return dict(input_data=input_data, target_data=target_data)


max_word = 15
max_features = 25000
batch_size = 30
state_size = 25
n_classes = 2

def td_sum(x):
    return K.sum(x, axis=1)

print('Build model...')
model = Sequential()
model.add(Masking(mask_value=0, input_shape=(max_word, )))
print('MAsking Model input shape {0} output shape {1}'.format(model.input_shape, model.output_shape))
model.add(Embedding(max_features, 1000))
print('EMBEDING Model input shape {0} output shape {1}'.format(model.input_shape, model.output_shape))
model.add(LSTM(state_size, dropout=0.5, recurrent_dropout=0.5, return_sequences=True))
print('Model input shape {0} output shape {1}'.format(model.input_shape, model.output_shape))
model.add(Lambda(td_sum))
print('Model input shape {0} output shape {1}'.format(model.input_shape, model.output_shape))
time.sleep(100)
model.add(Dense(2, activation='softmax'))
# model.add(Dense(1, activation='sigmoid'))

# try using different optimizers and different optimizer configs
model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
# model.compile(loss='binary_crossentropy', optimizer='adam', metrics=['accuracy'])

print('Train...')
with open('/home/john/sentiment_files/data/train.pkl', 'rb') as f:
    data = pickle.load(f)
perm = np.arange(len(data['input']))
np.random.shuffle(perm)
print(data['input'].max(1).max())
print(len(data['input']))
# stri = ''
# ind = 160000
# print('Data\n', data['input'][ind])
# for indx in data['input'][ind]:
#     stri += ' ' + index_to_vocab[indx]
# print(stri)
# time.sleep(100)

print("Data Loaded")
sess = tf.Session()
target = sess.run(tf.one_hot(data['target'][perm], n_classes))
# input_data = sess.run(tf.one_hot(data['input'][perm], max_features))
model.fit(data['input'][perm], target, batch_size=batch_size, epochs=5, validation_split=0.3)

print('Test...')
with open('/home/john/sentiment_files/data/test.pkl', 'rb') as f:
    data = pickle.load(f)
perm = np.arange(len(data['input']))
np.random.shuffle(perm)
target = sess.run(tf.one_hot(data['target'][perm], n_classes))
score, acc = model.evaluate(data['input'][perm], target, batch_size=batch_size)


print('Score {0} acc {1}'.format(score, acc))
prediction = model.predict(data['input'][perm], batch_size=batch_size)
# print(prediction)
sess = tf.Session()
prediction = sess.run(tf.nn.softmax(prediction))
# print(np.argmax(prediction))
# print(data['target_data'])
acc = np.sum(np.equal(np.argmax(prediction), data['target'][perm])) / len(data['target'])
print(acc)

# serialize model to JSON
model_json = model.to_json()
with open('/home/john/sentiment_files/model/complete_sentiment_15_word.json', "w") as json_file:
    json_file.write(model_json)
# serialize weights to HDF5
model.save_weights("/home/john/sentiment_files/model/complete_sentiment_15_word.h5")
print("Saved model to disk")