import math

CIPHERTEXT = "COTKXNHWJGXABFZPKGJCWGHMYQGEBJYBGQXJIRDCVLVPPWNKSIPXAMTKUQFHQJDKVBGAETTEOGFTSTJVKHKITSLOZYYBANBZALLPIMTKHCMBCTYHPQZNQUPKJFYPPEXDXFGUQMYWEEDXFMOQRECYQVSHDNBMCAXNRZWNTNTJQKEHEXFCKMYSVFHRZVWUSIJOVCOUSKPBKFPRRQKPFNZCRXNTTWKGSEUBMZXURCQEEPPOKWNSHGEPLFKQLATMWMKQBPKSELDVYVPFAWZSMDBMEFNERSXWRGGMBEXDSFDIQRPIGNZTPTZACHHQDTTASREJDLTFLSJLGKJPJKUXIAGNMIAEUFNKVOGVPBXUOHFBIYQLMRZEJOGHQFSYOUUXBWVCBLFLUDGXJCEXEWQZOHZMLAK";
ALPHABET_LEN = 26
ENGLISH_IOC = 0.067

def decode(c: str) -> int:
    return ord(c) - ord('A')

def encode(c: int) -> str:
    return chr(c + ord('A'))

def decrypt(ciphertext: int, key: int, block_index: int) -> int:
    # pt = (ciphertext - key - block_index + ALPHABET_LEN) % ALPHABET_LEN
    pt = ciphertext - (key + block_index)
    return pt % ALPHABET_LEN

def make_streams(text: str, block_size: int) -> list[str]:
    streams = [""] * block_size
    for i, c in enumerate(text):
        streams[i%block_size] += c
    return streams

def calc_stream_ioc(stream: str, key: int = 0) -> float:
    N = len(stream)
    if N == 1:
        return 0 # the stub

    freq_list = [0]*ALPHABET_LEN
    for block, char in enumerate(stream):
        char = ord(char) - ord('A')
        decrypted_char = decrypt(char, key, block)
        freq_list[decrypted_char] += 1

    ioc = 0.0
    for ctr in freq_list:
        ioc += (ctr * (ctr - 1))

    return ioc / (N * (N - 1))


def stream_letter_freq(stream: str) -> dict[str, int]:
    letter_freq = {}

    for block, char in enumerate(stream):
        decrypted_char = decode(char)
        decrypted_char = decrypt(decrypted_char, 0, block)
        decrypted_char = encode(decrypted_char)
        letter_freq[decrypted_char] = letter_freq.get(decrypted_char, 0) + 1

    return letter_freq


def decrypt_ciphertext(ciphertext: str, keys: list[int]) -> str:
    plaintext = ""
    block_count = math.ceil(len(ciphertext) / len(keys))
    block_size = len(keys)

    for block_index in range(block_count):
        start = block_index * block_size
        end = start + block_size
        block = ciphertext[start:end]

        for k, char in enumerate(block):
            c = decode(char)
            pt_char = decrypt(c, keys[k], block_index)
            plaintext += encode(pt_char)

    return plaintext

def recover_key(ciphertext: str, key_len: int) -> list[int]:
    streams = make_streams(ciphertext, key_len)
    key = [0]*key_len

    for i, stream in enumerate(streams):
        freq = stream_letter_freq(stream)
        
        print(i, freq)
        max_freq = 0
        stream_key = ''
        for l, f in freq.items():
            if f > max_freq:
                max_freq = f
                stream_key = l

        key[i] = (ord(stream_key) - ord('E')) % ALPHABET_LEN

    return key

if __name__ == "__main__":
    ioc_min = float('inf')
    key_len = 2

    for stream_size in range(2, len(CIPHERTEXT)):
        streams = make_streams(CIPHERTEXT, stream_size)

        ioc_sum = 0.0
        for stream in streams:
            ioc_sum += calc_stream_ioc(stream)

        ioc_avg = ioc_sum / stream_size
        ioc_diff = abs(ioc_avg - ENGLISH_IOC)

        if ioc_diff < ioc_min:
            ioc_min = ioc_diff
            key_len = stream_size

    print(f"Key length {key_len}")

    # keys = recover_key(CIPHERTEXT, key_len)
    keys = [decode(i) for i in "CIPHER"]
    print(decrypt_ciphertext(CIPHERTEXT, keys))
