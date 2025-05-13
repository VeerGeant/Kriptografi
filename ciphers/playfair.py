import string

def create_playfair_matrix(key: str):
    key = ''.join(sorted(set(key), key=lambda x: key.index(x)))  # Hilangkan duplikasi
    alphabet = string.ascii_uppercase.replace('J', '')  # Menghilangkan 'J' untuk menggantinya dengan 'I'
    
    matrix = []
    for char in key:
        if char not in matrix:
            matrix.append(char)
    
    for char in alphabet:
        if char not in matrix:
            matrix.append(char)
    
    # Membuat matriks 5x5
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def playfair_cipher(text: str, key: str, mode: str):
    key = key.upper().replace(" ", "")
    text = text.upper().replace("J", "I").replace(" ", "")  # Gantikan J dengan I

    # Membuat Playfair Matrix 5x5
    matrix = create_playfair_matrix(key)

    # Fungsi untuk menemukan posisi karakter di matriks
    def find_position(char):
        for i, row in enumerate(matrix):
            if char in row:
                return i, row.index(char)
        return None  # Jika tidak ditemukan

    # Encrypt atau Decrypt tergantung mode
    def process_pair(a, b):
        row_a, col_a = find_position(a)
        row_b, col_b = find_position(b)
        
        if row_a == row_b:
            return matrix[row_a][(col_a + 1) % 5] + matrix[row_b][(col_b + 1) % 5]
        elif col_a == col_b:
            return matrix[(row_a + 1) % 5][col_a] + matrix[(row_b + 1) % 5][col_b]
        else:
            return matrix[row_a][col_b] + matrix[row_b][col_a]

    # Membagi teks menjadi pasangan dua karakter
    pairs = []
    i = 0
    while i < len(text):
        if i + 1 < len(text) and text[i] != text[i + 1]:
            pairs.append((text[i], text[i + 1]))
            i += 2
        else:
            pairs.append((text[i], 'X'))  # Jika ada duplikasi, tambahkan 'X'
            i += 1

    result = ""
    for pair in pairs:
        a, b = pair
        if mode == "encrypt":
            result += process_pair(a, b)
        elif mode == "decrypt":
            result += process_pair(a, b)

    return result, matrix  # Kembalikan hasil dan matrix untuk preview
