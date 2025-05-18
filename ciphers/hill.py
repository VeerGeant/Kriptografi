import numpy as np
from math import gcd

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
    det = int(round(np.linalg.det(matrix))) % modulus
    if gcd(det, modulus) != 1:
        raise ValueError(f"Tidak ada invers modulo untuk determinan {det} mod {modulus}")

    det_inv = pow(det, -1, modulus)
    adjugate = np.round(np.linalg.det(matrix) * np.linalg.inv(matrix)).astype(int)
    return (det_inv * adjugate) % modulus

def hill_cipher(text, key, mode):
    text = clean_text(text)
    key_clean = clean_text(key)
    key_len = len(key_clean)

    # Tentukan ukuran matriks: 2x2 untuk 4 huruf, 3x3 untuk 9 huruf
    if key_len == 4:
        size = 2
    elif key_len == 9:
        size = 3
    else:
        raise ValueError("Key harus terdiri dari 4 (untuk 2x2) atau 9 (untuk 3x3) huruf.")

    key_nums = [ord(k) - ord('A') for k in key_clean]
    key_matrix = np.array(key_nums).reshape(size, size)
    text_matrix = text_to_matrix(text, size)

    if mode == 'encrypt':
        result = (np.dot(text_matrix, key_matrix) % 26)
    else:
        key_matrix_inv = mod_inverse_matrix(key_matrix, 26)
        result = (np.dot(text_matrix, key_matrix_inv) % 26)

    return matrix_to_text(result)