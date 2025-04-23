
def clean_text(text):
    return ''.join(filter(str.isalpha, text)).upper()

def vigenere_cipher(text, key, mode):
    text = clean_text(text)
    key = clean_text(key)
    result = ''
    key_length = len(key)
    for i, char in enumerate(text):
        key_char = key[i % key_length]
        shift = ord(key_char) - ord('A')
        if mode == 'encrypt':
            result += chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
        else:
            result += chr((ord(char) - ord('A') - shift + 26) % 26 + ord('A'))
    return result
