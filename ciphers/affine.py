
def mod_inverse(a, m):
    for x in range(1, m):
        if (a * x) % m == 1:
            return x
    raise ValueError('No mod inverse exists.')

def clean_text(text):
    return ''.join(filter(str.isalpha, text)).upper()

def affine_cipher(text, a, b, mode):
    text = clean_text(text)
    m = 26
    result = ''
    if mode == 'decrypt':
        a_inv = mod_inverse(a, m)
    for char in text:
        x = ord(char) - ord('A')
        if mode == 'encrypt':
            y = (a * x + b) % m
        else:
            y = (a_inv * (x - b)) % m
        result += chr(y + ord('A'))
    return result
