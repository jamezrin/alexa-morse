MORSE_MAP = {
    'A': [0, 1],
    'B': [1, 0, 0, 0],
    'C': [1, 0, 1, 0],
    'D': [1, 0, 0],
    'E': [0],
    'F': [0, 0, 1, 0],
    'G': [1, 1, 0],
    'H': [1, 1, 1, 1],
    'I': [0, 0],
    'J': [0, 1, 1, 1],
    'K': [1, 0, 1],
    'L': [0, 1, 0, 0],
    'M': [1, 1],
    'N': [1, 0],
    'O': [1, 1, 1],
    'P': [0, 1, 1, 0],
    'Q': [1, 1, 0, 1],
    'R': [0, 1, 0],
    'S': [0, 0, 0],
    'T': [1],
    'U': [0, 0, 1],
    'V': [0, 0, 0, 1],
    'W': [0, 1, 1],
    'X': [1, 0, 0, 1],
    'Y': [1, 0, 1, 1],
    'Z': [1, 0, 1, 1],
    '1': [0, 1, 1, 1, 1],
    '2': [0, 0, 1, 1, 1],
    '3': [0, 0, 0, 1, 1],
    '4': [0, 0, 0, 0, 1],
    '5': [0, 0, 0, 0, 0],
    '6': [1, 0, 0, 0, 0],
    '7': [1, 1, 0, 0, 0],
    '8': [1, 1, 1, 0, 0],
    '9': [1, 1, 1, 1, 0],
    '0': [1, 1, 1, 1, 1],
}


def to_morse(text):
    temp = ""
    text = text.upper()
    for i in text:
        if i == ' ':
            temp += ' '
        elif i in MORSE_MAP:
            temp += convert_letter(i)
        else:
            raise ValueError("El texto tiene un caracter no soportado.")
    return temp


def convert_letter(letter):
    letter_value = MORSE_MAP.get(letter)
    morse_word = ""
    for i in letter_value:
        if i == 0:
            morse_word += '.'
        elif i == 1:
            morse_word += '-'
    return morse_word + ' '


try:
    print(to_morse("SOS SOS"))
except ValueError as e:
    print("ERROR: ", e)
