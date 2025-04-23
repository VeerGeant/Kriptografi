
import string

def clean_text(text):
    return ''.join(filter(str.isalpha, text)).upper().replace('J', 'I')

def generate_matrix(key):
    key = clean_text(key)
    seen = set()
    matrix = []
    for char in key + string.ascii_uppercase:
        if char not in seen and char != 'J':
            seen.add(char)
            matrix.append(char)
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_position(matrix, char):
    for i, row in enumerate(matrix):
        if char in row:
            return i, row.index(char)

def playfair_cipher(text, key, mode):
    text = clean_text(text)
    text = text.replace('J', 'I')
    i = 0
    pairs = []
    while i < len(text):
        a = text[i]
        b = text[i + 1] if i + 1 < len(text) and text[i + 1] != a else 'X'
        pairs.append((a, b))
        i += 2 if b != 'X' else 1

    matrix = generate_matrix(key)
    result = ''
    for a, b in pairs:
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)
        if r1 == r2:
            if mode == 'encrypt':
                result += matrix[r1][(c1 + 1) % 5] + matrix[r2][(c2 + 1) % 5]
            else:
                result += matrix[r1][(c1 - 1) % 5] + matrix[r2][(c2 - 1) % 5]
        elif c1 == c2:
            if mode == 'encrypt':
                result += matrix[(r1 + 1) % 5][c1] + matrix[(r2 + 1) % 5][c2]
            else:
                result += matrix[(r1 - 1) % 5][c1] + matrix[(r2 - 1) % 5][c2]
        else:
            result += matrix[r1][c2] + matrix[r2][c1]
    return result
