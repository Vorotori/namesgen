import pandas as pd
import numpy as np
import streamlit as st

def convert_to_latin(name):

    FIRST_LETTERS = {'а':'a','б':'b','в':'v','г':'h','ґ':'g','д':'d','е':'e','є':'ye','-':'-',
                    'ж':'zh','з':'z','и':'y','і':'i','ї':'yi','й':'y','к':'k','л':'l',
                    'м':'m','н':'n','о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f',
                    'х':'kh','ц':'ts','ч':'ch','ш':'sh','щ':'shch','ю':'yu','я':'ya','ь':'','`':''}

    LETTERS = {'а':'a','б':'b','в':'v','г':'h','ґ':'g','д':'d','е':'e','є':'ie','-':'-',
                    'ж':'zh','з':'z','и':'y','і':'i','ї':'i','й':'i','к':'k','л':'l',
                    'м':'m','н':'n','о':'o','п':'p','р':'r','с':'s','т':'t','у':'u','ф':'f',
                    'х':'kh','ц':'ts','ч':'ch','ш':'sh','щ':'shch','ю':'iu','я':'ia','ь':'','`':''}

    # Примітка: 1. Буквосполучення "зг" відтворюється латиницею як "zgh" 
    #          (наприклад,  Згорани - Zghorany, Розгон - Rozghon) на 
    #          відміну від "zh" -  відповідника  української  літери 
    #          "ж". 

    name = name.lower()

    latin_name = []
    latin_name.append(FIRST_LETTERS[name[0]])
    for i in range(1,len(name)):
        if (name[i] == 'г') and (name[i-1] == 'з'):
            latin_name.append('gh')
        else:
            latin_name.append(LETTERS[name[i]])
    
    return ''.join(latin_name)

def check_gender(final_name):
    # Male or Female?
    female_endings = ['ва', 'ка']
    male_endings = ['ов', 'ий', 'єв']

    if final_name[-2:] in female_endings:
        gender = 'F'        
    elif final_name[-2:] in male_endings:
        gender = 'M'        
    else: 
        gender = 'N'
        

    return gender

@st.cache(show_spinner=False)
def read_first_names():
    males = pd.read_csv("namesgen/data/ua_male_first_names.csv",header=None)
    females = pd.read_csv("namesgen/data/ua_female_first_names.csv",header=None)

    return males, females

def match_first_name(gender):
    # Select an appropriate first name based on the sex and with real-life probabilities
    males, females = read_first_names()

    if gender == 'N':
        sex = np.random.choice(['M', 'F'])
    else: sex = gender

    if sex == 'M':
        index = np.random.choice(range(len(males)), p=males[1])
        first = males[0][index]
        final_ua_sex = 'Ч'
    if sex == 'F':
        index = np.random.choice(range(len(females)), p=females[1])
        first = females[0][index]
        final_ua_sex = 'Ж'

    return first, sex, final_ua_sex
