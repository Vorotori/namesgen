
import numpy as np
import pandas as pd
import streamlit as st
from PIL import Image
from namesgen import generator, utils, ua_name_converter


st.sidebar.markdown(f"""
    # Name Generator
    """)

st.subheader('Generating real sounding names with the help of deep learning models')

direction = st.sidebar.radio('What would you like to create?', 
                            ('A Ukrainian Identity', 'An Indian Deity', 'A Eurorack Manufacturer'))

st.write(f"""# {direction}""")

my_slot1 = st.empty()

if direction == 'A Ukrainian Identity':
    my_slot1.write('Ready to create...')
    filename = 'uanames.txt'
elif direction == 'An Indian Deity':
    my_slot1.write('Not available yet')
elif direction == 'A Eurorack Manufacturer':
    my_slot1.write('Not available yet')
else:
    st.write('First select what would you like to generate')

if st.sidebar.button('Generate'):
    # print is visible in server output, not in the page
    print('Generating name...')
    my_slot1.write("Generating name...")
    generated_name = generator.predict_name(filename)

    # Taks-specific processing section
    if direction == 'A Ukrainian Identity':
        gender = ua_name_converter.check_gender(generated_name)
        first_name, gender, ua_gender = ua_name_converter.match_first_name(gender)
        my_slot1.write("Generation successful!")
        col1, col2 = st.beta_columns(2)
        
        col1.subheader(f'{first_name.capitalize()} {generated_name.capitalize()} ({ua_gender})')
        col1.subheader(f'{ua_name_converter.convert_to_latin(first_name).capitalize()} {ua_name_converter.convert_to_latin(generated_name).capitalize()} ({gender})')
        
        if gender == 'M':
            image = Image.open('namesgen/data/ups.jpg')
        else:
            image = Image.open('namesgen/data/upsf.jpg')    
        col2.image(image, caption='Ukrainian Passport Example', use_column_width=True)
    else:
        st.text('Something went wrong...')
    
    real = utils.is_real(generated_name,filename)
    if real:
        st.success(f'This name is real.')
    else:
        st.warning(f'This name is not real.')     
else:
    st.sidebar.write('Click this button to generate a new name')


