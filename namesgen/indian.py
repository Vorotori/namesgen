# Funstions to accompany Indian Deities creation process

# Indian transliteration
from indic_transliteration import sanscript
from indic_transliteration.sanscript import SchemeMap, SCHEMES, transliterate

def translit(final_name):

    indic = {
    'Devanagari':transliterate(final_name, sanscript.ITRANS, sanscript.DEVANAGARI),
    'Telugu': transliterate(final_name, sanscript.HK, sanscript.TELUGU),
    'Tamil': transliterate(final_name, sanscript.ITRANS, sanscript.TAMIL),
    'Gujarati': transliterate(final_name, sanscript.ITRANS, sanscript.GUJARATI),
    'Bengali': transliterate(final_name, sanscript.ITRANS, sanscript.BENGALI),
    'Kannada': transliterate(final_name, sanscript.ITRANS, sanscript.KANNADA),
    'Malayalam': transliterate(final_name, sanscript.ITRANS, sanscript.MALAYALAM),
    'Oriya': transliterate(final_name, sanscript.ITRANS, sanscript.ORIYA)
    }
    
    return indic