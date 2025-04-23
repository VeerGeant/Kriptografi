
def clean_text(text):
    return ''.join(filter(str.isalpha, text)).upper()

def auto_key_vigenere(text, key, mode):
    text = clean_text(text)
    key = clean_text(key)
    if mode == 'encrypt':
        full_key = key + text
    else:
        full_key = key
    result = ''
    for i in range(len(text)):
        k = full_key[i] if i < len(full_key) else result[i - len(key)]
        shift = ord(k) - ord('A')
        if mode == 'encrypt':
            result += chr((ord(text[i]) - ord('A') + shift) % 26 + ord('A'))
        else:
            result += chr((ord(text[i]) - ord('A') - shift + 26) % 26 + ord('A'))
            full_key += result[-1]
    return result
