# Input Based Names Generator v1
# This algorithm generates new words that sound like the words in the input dataset
# This could be anything
# In our examples we used Ukrainian surnames, names of Indian gods, names of Eurorack modules

# In ML articles this is notmally called ##Character level language model##

from namesgen.utils import get_names, create_indexes, get_minmax, create_xy, make_name
from namesgen.namesgen_model import compile_lstm_gru
from tensorflow import keras
import streamlit as st

# Load model and store it in streamlit cache
# @st.cache == do not know how to pass hash_funcs
def load_that_model(filename):
    model = keras.models.load_model(f'namesgen/models/{filename[:-4]}')

    return model

# 1. Standard text preprocessing steps
def predict_name(model, filename, special,max_length):
    chars, names = get_names(f'namesgen/data/{filename}')
    char_to_ix, ix_to_char = create_indexes(chars)
    max_char, min_char = get_minmax(names)

    # 2. Preparation of data for deep learning
    X, Y = create_xy(chars,names,max_char,char_to_ix)

    # Load trained model
    generated_name = make_name(model,max_length,chars,ix_to_char,special)
    
    return generated_name