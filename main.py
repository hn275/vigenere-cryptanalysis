import enum
from re import split


CIPHERTEXT = "COTKXNHWJGXABFZPKGJCWGHMYQGEBJYBGQXJIRDCVLVPPWNKSIPXAMTKUQFHQJDKVBGAETTEOGFTSTJVKHKITSLOZYYBANBZALLPIMTKHCMBCTYHPQZNQUPKJFYPPEXDXFGUQMYWEEDXFMOQRECYQVSHDNBMCAXNRZWNTNTJQKEHEXFCKMYSVFHRZVWUSIJOVCOUSKPBKFPRRQKPFNZCRXNTTWKGSEUBMZXURCQEEPPOKWNSHGEPLFKQLATMWMKQBPKSELDVYVPFAWZSMDBMEFNERSXWRGGMBEXDSFDIQRPIGNZTPTZACHHQDTTASREJDLTFLSJLGKJPJKUXIAGNMIAEUFNKVOGVPBXUOHFBIYQLMRZEJOGHQFSYOUUXBWVCBLFLUDGXJCEXEWQZOHZMLAK";
ALPHABET_LEN = 26
ENGLISH_IOC = 0.067

def decode(c: str) -> int:
    return ord(c) - ord('A')

def encode(c: int) -> str:
    return chr(c + ord('A'))

def decrypt(ciphertext: int, key: int, block_index: int) -> int:
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
        decrypted_char = ord(char) - ord('A')
        decrypted_char = decrypt(decrypted_char, 0, block)
        decrypted_char += ord('A')
        decrypted_char = chr(decrypted_char)
        letter_freq[decrypted_char] = letter_freq.get(decrypted_char, 0) + 1

    return letter_freq


def decrypt_ciphertext(ciphertext: str, keys: list[int]) -> str:
    plaintext = ""

    block_size = len(keys)
    block_index = -1

    for i, char in enumerate(ciphertext):
        if i % block_size == 0:
            block_index += 1

        p = decrypt(decode(char), keys[i % block_size], block_size)
        plaintext += encode(p)

    return plaintext

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

    # brute force the key for each stream
    streams = make_streams(CIPHERTEXT, key_len)
    keys = [0]*key_len

    assert len(streams) == key_len

    for i in range(key_len):
        letter_freq = stream_letter_freq(streams[i])
        max_key: str = max(letter_freq, key=letter_freq.get)
        keys[i] = decode(max_key) % ALPHABET_LEN

    print(f"key {keys} - {"".join([encode(i) for i in keys])}")
    pt = decrypt_ciphertext(CIPHERTEXT, keys)
    print(pt)
