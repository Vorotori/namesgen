import numpy as np

eurorack_endings = {'modular':0.2,'audio':0.13,'electronics':0.1,'instruments':0.09,'music':0.08,'systems':0.07,'sound':0.06,'labs':0.06,
                    'circuits':0.04,'devices':0.04,'technologies':0.03,'synthesis':0.03,'analog':0.02, 'modules':0.03,
                    'technology':0,'design':0.01,'synthesizer':0,'tools':0.01}

def get_eurorack_styling():
    ending = ''
    with_ending = np.random.choice([True, False])
    if with_ending:
        index = np.random.choice(range(len(list(eurorack_endings.values()))), p=list(eurorack_endings.values()))
        ending = ' '+list(eurorack_endings.keys())[index]
    
    return ending

def random_style():
    # Generate random display style for the name
    size = str(np.random.choice([30,35,40,45,50,55,60]))
    fonts = ['Arial','Helvetica','Palatino','Verdana','Trebuchet MS','Calisto MT',
            'Didot','Perpetua','Consolas','Optima','Century Gothic','Andale Mono',
            'Copperplate Gothic','Bodoni','Impact','Lucida Console','Comic Sans MS']
    font = str(np.random.choice(fonts))
    style = """
            <style>
            .random-font {
                font-size:""" + size + """px !important;
                font-family:""" + font + """;
            \}
            </style>
            """
    return style