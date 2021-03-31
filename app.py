
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
from namesgen import generator, utils, ua_name_converter, indian, eurorack, confs

stop_chars = ['-', ' ', 'ь', '`']

st.sidebar.title(f"""
    Name Generator
    """)

direction = st.sidebar.radio('What would you like to create?', 
                            ('A Ukrainian Identity', 'An Indian Deity', 'A Eurorack Manufacturer'),
                            index=0)

regenerate = True

st.markdown("""# Name Generator""")
st.text('   Generating real sounding names with the help of deep learning models')
my_slot0 = st.empty()

my_slot1 = st.empty()
my_slot2 = st.empty()

if direction == 'A Ukrainian Identity':
    my_slot0.write(f"""## {direction}""")
    my_slot1.write('Ready to create...')
    filename = 'uanames.txt'
    special = ' '
elif direction == 'An Indian Deity':
    my_slot0.write(f"""## {direction}""")
    my_slot1.write('Ready to create...')
    filename = 'indian_gods.txt'
    special = ' '
elif direction == 'A Eurorack Manufacturer':
    my_slot0.write(f"""## {direction}""")
    my_slot1.write('Ready to create...')
    filename = 'eurorack_manufacturers.txt'
    special = '>'
else:
    st.write('First select what would you like to generate')

dont_show_real = st.sidebar.checkbox('Do not show existing names', value=False)

if st.sidebar.button('Generate'):
    # print is visible in server output, not in the page
    print('Generating name...')
    my_slot1.write("Generating name...")
    
    while regenerate:
        model = generator.load_that_model(filename)
        max_length = model.output_shape[1]
        chars, names, char_to_ix, ix_to_char, max_char, min_char = generator.parse_text(filename)
        generated_name = generator.predict_name(model, filename, special, max_length, chars, names, char_to_ix, ix_to_char, max_char, min_char)
        
        real = utils.is_real(generated_name,filename)
        
        if (real and dont_show_real) or (len(generated_name) < 2) or (generated_name[0] in stop_chars):
            regenerate = True
            if dont_show_real:
                my_slot1.write(f"Got real name ({generated_name.capitalize()}). Regenerating...")
            else:
                my_slot1.write(f"Bad name ({generated_name.capitalize()}). Regenerating...")
            print('Had to regenerate.')
        else: regenerate = False

    # Taks-specific processing section
    if direction == 'A Ukrainian Identity':
        gender = ua_name_converter.check_gender(generated_name)
        first_name, gender, ua_gender = ua_name_converter.match_first_name(gender)
        my_slot1.write("Generation successful!")
        col1, col2 = st.beta_columns(2)
        
        col1.subheader(f'{first_name.capitalize()} {generated_name.capitalize()} ({ua_gender})'
                       f'\n{ua_name_converter.convert_to_latin(first_name).capitalize()} {ua_name_converter.convert_to_latin(generated_name).capitalize()} ({gender})')
        
        if gender == 'M':
            image = Image.open('namesgen/data/ups.jpg')
        else:
            image = Image.open('namesgen/data/upsf.jpg')    
        col2.image(image, caption='Ukrainian Passport Example', use_column_width=True)
    # Taks-specific processing section
    elif direction == 'An Indian Deity':
        my_slot1.write("Generation successful!")
        col1, col2 = st.beta_columns(2)
        indic = indian.translit(generated_name)
        col1.subheader(f'{generated_name.capitalize()} / {indic["Devanagari"]}')
        del indic['Devanagari']
        for key, value in indic.items():
            col2.write(f'{key} version: {value}\n')

        thumbnails = utils.search_images(generated_name)
        st.write('What could this name possibly mean?')
        
        if thumbnails == []:
            st.write(f'No images found for {generated_name.capitalize()}.')
        else:
            col3, col4, col5 = st.beta_columns(3)
        for t in range(len(thumbnails)):
            eval('col'+str(t+3)).image(thumbnails[t], use_column_width=True, clamp=False, channels='RGB', output_format='auto')
    # Taks-specific processing section
    elif direction == 'A Eurorack Manufacturer':
        ending = eurorack.get_eurorack_styling()
        my_slot1.write("Generation successful!")
        col1, col2 = st.beta_columns(2)
        final_name = generated_name + ending        
        col1.subheader(f'{final_name.title()}')

        
        style = eurorack.random_style()
        st.markdown(style, unsafe_allow_html=True)
        col2.markdown(f'<p class="random-font">{final_name.title()}</p>', unsafe_allow_html=True)
                       
        
                

    else:
        st.text('Something went wrong...')
    
    if real and not dont_show_real:
        col1.success(f'\nThis name is real.')
    else:
        col1.warning(f'\nThis name is not real.')
        

st.sidebar.write('Click this button to generate a new name')

st.sidebar.text('\n\n\n\n\n\n')
if st.sidebar.button('Project Info'):
    my_slot0.markdown("""## PROJECT DESCRIPTION""")
    my_slot1.markdown("""
This project explores the possibilities of Deep Learning approach in generating similar-sounding but not necessarily existing names based on a given set of real names. The solution in this particular case is a character-based sequential prediction algorithm. The prediction model is a recurrent neural network that uses LSTM and GRU layers with various hyperparameters.
## THE MODEL
The model is a simple combination of LSTM, GRU and Dropout layers. Input sequences are single names as lists of characters shifted one character forward for prediction purposes. A large number of nodes shows better results. Other hyperparameters such as batch size, dropout, learning rate, and number of epochs contribute to the ability of the model to produce appropriate results.\n
The model generalizes well on larger sets (Ukrainian surnames) but tends to overfit with smaller datasets (Eurorack manufacturers).\n
    model = Sequential()
    model.add(LSTM(256, input_shape=(max_char, alphabet_size), recurrent_dropout=0.5, return_sequences=True, activation='tanh'))
    model.add(GRU(128, recurrent_dropout=0.5, return_sequences=True))
    model.add(Dropout(0.5))
    model.add(Dense(alphabet_size, activation='softmax'))
    model.compile(loss='categorical_crossentropy', optimizer='adam')
Here *max_char* is the maximum length of a name and *alphabet_size* is the number of unique characters in the training dataset.
### 1. UKRAINIAN NAMES
The model was trained on a publicly available set of 10 000 Ukrainian surnames. Output is randomized but takes into account probabilities assigned by the model to each character. Resulting predictions sometimes coincide with real names, and in rare cases fail to resemble possible surnames. The user interface provides an option to hide real-world examples, bad results are filtered out.
#### UKRAINIAN SURNAMES SPECIFIC FEATURES
To accompany the model and make it more real sounding the following features were added:\n
-	Sex identification based on the ending of the generated surname or randomly picked up first name
-	First name suggestion based on sex and real-world name frequency. In case the surname is unisex, male/female is chosen as a coin toss.
-	Official transliteration of the name into Latin alphabet according to the Resolution of the Cabinet of Ministers of Ukraine from January 27, 2010 N 55. This transliteration is officially used in travel documents.
-	Specimens of real Ukrainian identification documents for visualization purposes.
#### NOTES
Some generated names are labeled as not existing, but do actually exist. This is because the algorithm only checks the names in the dataset it was trained on and doesn’t do any online search or web-scrapping to identify whether the name actually exists or not. 
Sometimes the names sound perfectly right, but are still marked as non-existing. It may also be due to the fact that many names would resemble Russian-style spelling but should be actually written differently according to the Ukrainian spelling rules.
### 2. INDIAN DEITIES
This model was trained on a small set of about 600 Indian gods and goddesses whose names are freely available via online resources such as Wikipedia. Output is randomized but takes into account probabilities assigned by the model to each character. Resulting predictions sometimes coincide with real names, and in rare cases fail to resemble real-like names. The user interface provides an option to hide real-world examples, bad results are filtered out.
#### INDIAN DEITIES SPECIFIC FEATURES
To accompany the model the following features were added:\n
-	Transliteration of the Latin version into several Indian scripts according to ITRANS rules. The languages are Devanagari, Telugu, Tamil, Gujarati, Bengali, Kannada, Malayalam, and Oriya. Transliteration are done with the help of indic_transliteration module for Python.
-	Automatic image search using Bing Image Search API that returns 3 first images found with the generated word as a query. This allows to check what the word could possibly mean in the real world.
### 3. EURORACK MANUFACTURERS
This model was trained on a small set of 439 names of Eurorack manufacturers listed on modulargrid.net. Output is randomized but takes into account probabilities assigned by the model to each character. Resulting predictions sometimes coincide with real names, and in rare cases fail to resemble real-like names. The user interface provides an option to hide real-world examples, bad results are filtered out.
#### EURORACK MANUFACTURERS SPECIFIC FEATURES
To accompany the model the following features were added:\n
-	Real-world name extensions. Eurorack manufacturers often pair up their brand names with words like “Electronics”, “Modular”, “Music” etc. The list of most frequent extensions was created to be randomly added to a generated word making the names sound more realistic.
-	Logo-like text display. The algorithm randomizes a set of basic font types and sizes to display generated names in more appealing way.
\n\n
This project on GitHub: https://github.com/Vorotori/namesgen
\n\n
2021 ©
""")

st.sidebar.write('Click for detailed description of the project')
