# ### Dataset and Preprocessing (CLEAN)

import numpy as np
import requests

def get_names(filename):
    # Reads the file == should be a simple text file with one name per line
    data = open(f'{filename}', 'r').read()
    data = data.lower() # dataset of single lower-case characters
    names = data.split('\n') # list of parsed names
    names = [s+' ' for s in names] # all names end with an extra space to signify end of word
    chars = list(set(data)) # list of unique characters (usually results in alphabet + couple of special symbols)
    chars.remove('\n')
    if ' ' not in chars:
        chars.append(' ')
    total_chars, alphabet_size, how_many_names = len(data), len(chars), len(names)
    
    return chars, names

def create_indexes(alphabet):
    # Create two mutual indexes
    char_to_ix = { ch:i for i,ch in enumerate(sorted(alphabet)) }
    ix_to_char = { i:ch for i,ch in enumerate(sorted(alphabet)) }
    
    return char_to_ix, ix_to_char

def get_minmax(names):
    # Get maximal and minimal names length
    max_char = len(max(names, key=len))
    min_char = len(min(names, key=len))

    return max_char, min_char

def create_xy(chars,names,max_char,char_to_ix):
    # Returns X and Y 3D arrays

    X = np.zeros((len(names), max_char, len(chars)))
    Y = np.zeros((len(names), max_char, len(chars)))

    for i in range(len(names)):
        name = list(names[i])
        for j in range(len(name)):
            X[i, j, char_to_ix[name[j]]] = 1
            if j < len(name)-1:
                Y[i, j, char_to_ix[name[j+1]]] = 1
    
    return X,Y

# Callback providing useful information every 25 epochs

def make_name(model,max_char,chars,ix_to_char,special):
    name = []
    i = 0
    character = ''
    x = np.zeros((1, max_char, len(chars)))
    special = special
        
    while (character != special) and (i < max_char-1 ):
      probs = list(model.predict(x)[0,i])
      probs = probs / np.sum(probs)
      index = np.random.choice(range(len(chars)), p=probs)
      character = ix_to_char[index]
      name.append(character)
      x[0, i+1, index] = 1
      i += 1
        
    final_name = ''.join(name[:-1])
    
    return final_name

def is_real(final_name,filename):
    # Name exists?
    data = open(f'namesgen/data/{filename}', 'r').read()
    data = data.lower() # dataset of single lower-case characters
    names = data.split() # list of parsed names
    exists = final_name in names

    return exists

def search_images(final_name):

    subscription_key = "baf7067e328d40a789e9c3d076f3c898"
    assert subscription_key
    search_url = "https://api.bing.microsoft.com/v7.0/images/search"
    search_term = final_name

    headers = {"Ocp-Apim-Subscription-Key": subscription_key}
    params = {"q": search_term, "count":3, "mkt":"en-IN"}
    response = requests.get(search_url, headers=headers, params=params)
    response.raise_for_status()
    search_results = response.json()
    thumbnail_urls = [img["thumbnailUrl"] for img in search_results["value"][:16]]
    
    return thumbnail_urls


     


