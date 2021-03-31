# Input Based Names Generator v1
# This algorithm generates new words that sound like the words in the input dataset
# This could be anything
# In our examples we used Ukrainian surnames, names of Indian gods, names of Eurorack modules

# In ML articles this is notmally called ##Character level language model##

from namesgen.utils import get_names, create_indexes, get_minmax, make_name
from tensorflow import keras
import streamlit as st

# Load model and store it in streamlit cache
@st.cache(allow_output_mutation=True, show_spinner=False)
def load_that_model(filename):
    model = keras.models.load_model(f'namesgen/models/{filename[:-4]}')

    return model

# 1. Standard text preprocessing steps
@st.cache(show_spinner=False)
def parse_text(filename):
    chars, names = get_names(f'namesgen/data/{filename}')
    char_to_ix, ix_to_char = create_indexes(chars)
    max_char, min_char = get_minmax(names)

    return chars, names, char_to_ix, ix_to_char, max_char, min_char

def predict_name(model, filename, special, max_length, chars, names, char_to_ix, ix_to_char, max_char, min_char):
    # Make prediction with loaded trained model
    generated_name = make_name(model,max_length,chars,ix_to_char,special)
    
    return generated_name