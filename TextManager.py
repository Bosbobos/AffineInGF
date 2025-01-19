from math import log, ceil, floor

def string_to_binary(text):
    return ''.join(bin(ord(i))[2:].rjust(8, '0') for i in text)


def binary_to_string(binary):
    return ''.join(chr(int(binary[i:i + 8], 2)) for i in range(0, len(binary), 8))

def string_to_base_p(text, p):
    res = ''
    max_unicode_num = 155063
    block_len = len(str(p)) * ceil(log(max_unicode_num, p))

    for symbol in text:
        sym_res = ''
        x = ord(symbol)
        while x:
            sym_res += str(x % p).ljust(len(str(p)), '0')
            x //= p

        sym_res = sym_res[::-1]
        res += sym_res.rjust(block_len, '0')

    return res

def base_p_to_string(encoded_text, p):
    res = ''
    max_unicode_num = 155063
    block_len = len(str(p)) * ceil(log(max_unicode_num, p))
    for i in range(0, len(encoded_text), block_len):
        sym_res = 0
        block = encoded_text[i:i + block_len].rjust(block_len, '0')
        for j in range(0, block_len, len(str(p))):
            x = int(block[j : j + len(str(p))])
            sym_res += x * p ** (block_len//len(str(p)) - j - 1)

        res += chr(int(sym_res))

    return res
