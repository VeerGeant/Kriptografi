
def extended_vigenere(data, key, mode):
    key_bytes = key.encode()
    key_len = len(key_bytes)
    result = bytearray()
    for i in range(len(data)):
        k = key_bytes[i % key_len]
        if mode == 'encrypt':
            result.append((data[i] + k) % 256)
        else:
            result.append((data[i] - k + 256) % 256)
    return bytes(result)
