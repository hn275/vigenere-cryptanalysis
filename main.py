from re import split


CIPHERTEXT = "COTKXNHWJGXABFZPKGJCWGHMYQGEBJYBGQXJIRDCVLVPPWNKSIPXAMTKUQFHQJDKVBGAETTEOGFTSTJVKHKITSLOZYYBANBZALLPIMTKHCMBCTYHPQZNQUPKJFYPPEXDXFGUQMYWEEDXFMOQRECYQVSHDNBMCAXNRZWNTNTJQKEHEXFCKMYSVFHRZVWUSIJOVCOUSKPBKFPRRQKPFNZCRXNTTWKGSEUBMZXURCQEEPPOKWNSHGEPLFKQLATMWMKQBPKSELDVYVPFAWZSMDBMEFNERSXWRGGMBEXDSFDIQRPIGNZTPTZACHHQDTTASREJDLTFLSJLGKJPJKUXIAGNMIAEUFNKVOGVPBXUOHFBIYQLMRZEJOGHQFSYOUUXBWVCBLFLUDGXJCEXEWQZOHZMLAK";
ALPHABET_LEN = 26
ENGLISH_IOC = 0.067

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
