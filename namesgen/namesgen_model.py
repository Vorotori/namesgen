# The training code for the model
# Accepts X and Y created with create_xy() from 'utils'

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, GRU, Dropout

# Building actual model

def compile_lstm_gru(max_char, chars):
    model = Sequential()
    model.add(LSTM(256, input_shape=(max_char, len(chars)), recurrent_dropout=0.2, return_sequences=True, activation='tanh'))
    model.add(GRU(128, recurrent_dropout=0.2, return_sequences=True))
    model.add(Dropout(0.4))
    model.add(Dense(len(chars), activation='softmax'))

    model.compile(loss='categorical_crossentropy', optimizer='adam')

    return model

