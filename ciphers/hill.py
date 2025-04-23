
import numpy as np

def clean_text(text):
    return ''.join(filter(str.isalpha, text)).upper()

def text_to_matrix(text, size):
    text = clean_text(text)
    while len(text) % size != 0:
        text += 'X'
    matrix = [ord(c) - ord('A') for c in text]
    return np.array(matrix).reshape(-1, size)

def matrix_to_text(matrix):
    return ''.join(chr(int(round(num)) % 26 + ord('A')) for num in matrix.flatten())

def mod_inverse_matrix(matrix, modulus):
    det = int(round(np.linalg.det(matrix)))
    det_inv = pow(det, -1, modulus)
    matrix_mod_inv = (
        det_inv * np.round(det * np.linalg.inv(matrix)).astype(int) % modulus
    )
    return matrix_mod_inv

def hill_cipher(text, key, mode, size=3):
    text = clean_text(text)
    key_nums = [ord(k) - ord('A') for k in clean_text(key)]
    key_matrix = np.array(key_nums).reshape(size, size)
    text_matrix = text_to_matrix(text, size)

    if mode == 'encrypt':
        result = (np.dot(text_matrix, key_matrix) % 26)
    else:
        key_matrix_inv = mod_inverse_matrix(key_matrix, 26)
        result = (np.dot(text_matrix, key_matrix_inv) % 26)
    return matrix_to_text(result)
