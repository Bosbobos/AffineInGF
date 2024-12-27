def string_to_binary(text):
    return ''.join(bin(ord(i))[2:].rjust(8, '0') for i in text)


def binary_to_string(binary):
    return ''.join(chr(int(binary[i:i + 8], 2)) for i in range(0, len(binary), 8))
