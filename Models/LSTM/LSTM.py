from google.colab import drive
drive.mount('/content/drive')


import pickle
with open("/content/drive/MyDrive/Design_Project_Verselet/pre_processing+vectoristation/word_embedding/word_vectors_test_set_100_iterations",'rb') as f:
  glove = pickle.load(f)

with open("/content/drive/MyDrive/Design_Project_Verselet/pre_processing+vectoristation/tf-idf/test_data_btf",'rb') as f:
  testData = pickle.load(f)

with open("/content/drive/MyDrive/Design_Project_Verselet/pre_processing+vectoristation/tf-idf/train_data_btf",'rb') as f:
  trainData = pickle.load(f)

totalLen = len(trainData)
validationStart = (int) (90*totalLen/100)

validationData = trainData[validationStart:]
trainData = trainData[0:validationStart]



poets = []
eras = []

for i in range(len(trainData)):
  if trainData[i][3] == '':
    continue
  if trainData[i][3] not in eras:
    eras.append(trainData[i][3])
  if trainData[i][0] not in poets:
    poets.append(trainData[i][0])

numEras = len(eras)
numPoets = len(poets)
print(numEras)
print(numPoets)

from sklearn.feature_extraction.text import TfidfVectorizer
train_poems = []
for elem in trainData:
	train_poems.append(elem[4])
def identity_func(doc):
	return doc
btf = TfidfVectorizer(binary=True,
	norm=None,
	use_idf=False,
	smooth_idf=False,
	lowercase=False,
	tokenizer=identity_func,
	preprocessor=identity_func,
  min_df = 500,
	max_df = 0.8,
	token_pattern=None)
# Fit the model
btf.fit(train_poems)

len(btf.vocabulary_)




# Keras
import keras
from keras.preprocessing.text import Tokenizer
from keras.preprocessing.sequence import pad_sequences
from keras.models import Sequential
from keras.layers import Dense, Flatten, LSTM, Bidirectional,Conv1D, MaxPooling1D, Dropout, Activation
from keras.layers.embeddings import Embedding

# Other
import re
import string
import numpy as np
import pandas as pd

embeddings_index = dict()
for tok in btf.vocabulary_.keys():
  embeddings_index[tok] = np.asarray(glove[tok],dtype='float32')

all_vocab_words = list(embeddings_index.keys())

vocabulary_size = len(all_vocab_words)
tokenizer = Tokenizer() #num_words= vocabulary_size
tokenizer.fit_on_texts(all_vocab_words)

embedding_matrix = np.zeros((vocabulary_size, 100)) 
for word, index in tokenizer.word_index.items():
    if index > vocabulary_size - 1:
        break
    else:
        embedding_vector = embeddings_index.get(word)
        if embedding_vector is not None:
            embedding_matrix[index] = embedding_vector

print(embedding_matrix.shape)

def removeToksNotInVocab(Data):
  for i in range(len(Data)):
    inp = []
    for tok in Data[i][4]:
      if tok in all_vocab_words:
        inp.append(tok)
    Data[i][4] = inp

removeToksNotInVocab(trainData)
removeToksNotInVocab(testData)
removeToksNotInVocab(validationData)

maxLen = 500
maxC = 0
count = 0

for i in range(len(testData)):
  if len(testData[i][4]) > maxLen:
    count = count +1
  maxC = max(len(testData[i][4]),maxC)

print(len(testData))
print(count)
print(maxLen)

import numpy as np
import tensorflow as tf
def getXandY(Data):
  X = []

  for i in range(len(Data)):
    if i % 1000 == 0:
      print(i)
    if Data[i][3] == '':
      continue
    if Data[i][0] not in poets:
      continue
    if len(trainData[i][4]) > maxLen:
      trainData[i][4] = trainData[i][4][0:maxLen]
    strVar = ' '.join(trainData[i][4])
    X.append(strVar)

  Y_poets = np.zeros((len(X),numPoets))
  Y_eras = np.zeros((len(X),numEras))
  count = 0
  for i in range(len(Data)):
    if i % 1000 == 0:
      print(i)
    if Data[i][3] == '':
      continue
    if Data[i][0] not in poets:
      continue
    Y_poets[count][poets.index(Data[i][0])] = 1.0
    Y_eras[count][eras.index(Data[i][3])] = 1.0
    count = count + 1

  
  print("Start Conversion")
  sequences = tokenizer.texts_to_sequences(X)
  data = pad_sequences(sequences, maxlen=maxLen)
  return [data,Y_poets,Y_eras]

[X_test, Y_test_poets, Y_test_eras] = getXandY(testData)
[X_train, Y_train_poets, Y_train_eras] = getXandY(trainData)
[X_validation, Y_validation_poets, Y_validation_eras] = getXandY(validationData)



"""### Model Poets"""

from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Masking, Embedding


model = Sequential()

model.add(Embedding(vocabulary_size, output_dim=100, input_length=maxLen, weights=[embedding_matrix], trainable=False))
# Recurrent layer
model.add(LSTM(100, return_sequences=False, dropout=0.1, recurrent_dropout=0.1, input_shape=(None, 100)))

# Fully connected layer
model.add(Dense(100, activation='relu'))

# Fully connected layer
model.add(Dense(100, activation='relu'))

# Output layer
model.add(Dense(numPoets, activation='softmax'))

# Compile the model
model.compile(
    optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.summary()

from keras.callbacks import EarlyStopping, ModelCheckpoint

callbacks = [EarlyStopping(monitor='val_loss', patience=5000),
             ModelCheckpoint('/content/drive/MyDrive/Design_Project_Verselet/LSTM+GloVe/LstmModel.h5', save_best_only=False, 
             save_weights_only=False)]

history = model.fit(X_train,  Y_train_poets, 
                    batch_size=256, epochs=10,
                    callbacks=callbacks,
                    validation_data=(X_validation, Y_validation_poets))

from keras.models import load_model
# Load in model and evaluate on validation data
model = load_model('/content/drive/MyDrive/Design_Project_Verselet/LSTM+GloVe/LstmModel.h5')
# model.evaluate(X_valid, Y_valid)

model.evaluate(X_test, Y_test_poets)

model.evaluate(X_train, Y_train_poets)


"""###Model Eras"""

from keras.models import Sequential
from keras.layers import LSTM, Dense, Dropout, Masking, Embedding


model = Sequential()

model.add(Embedding(vocabulary_size, output_dim=100, input_length=maxLen, weights=[embedding_matrix], trainable=False))
# Recurrent layer
model.add(LSTM(100, return_sequences=False, dropout=0.1, recurrent_dropout=0.1, input_shape=(None, 100)))

# Fully connected layer
model.add(Dense(100, activation='relu'))

# Fully connected layer
model.add(Dense(100, activation='relu'))

# Output layer
model.add(Dense(numEras, activation='softmax'))

# Compile the model
model.compile(
    optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])

model.summary()

from keras.callbacks import EarlyStopping, ModelCheckpoint

callbacks = [EarlyStopping(monitor='val_loss', patience=30),
             ModelCheckpoint('/content/drive/MyDrive/Design_Project_Verselet/LSTM+GloVe/LstmModel.h5', save_best_only=False, 
             save_weights_only=False)]

history = model.fit(X_train,  Y_train_eras, 
                    batch_size=256, epochs=10,
                    callbacks=callbacks,
                    validation_data=(X_validation, Y_validation_eras))

from keras.models import load_model
# Load in model and evaluate on validation data
model = load_model('/content/drive/MyDrive/Design_Project_Verselet/LSTM+GloVe/LstmModel.h5')
# model.evaluate(X_valid, Y_valid)

model.evaluate(X_test, Y_test_eras)

model.evaluate(X_train, Y_train_eras)