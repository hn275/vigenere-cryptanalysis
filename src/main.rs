use core::f64;

const INPUT: &'static str = "COTKXNHWJGXABFZPKGJCWGHMYQGEBJYBGQXJIRDCVLVPPWNKSIPXAMTKUQFHQJDKVBGAETTEOGFTSTJVKHKITSLOZYYBANBZALLPIMTKHCMBCTYHPQZNQUPKJFYPPEXDXFGUQMYWEEDXFMOQRECYQVSHDNBMCAXNRZWNTNTJQKEHEXFCKMYSVFHRZVWUSIJOVCOUSKPBKFPRRQKPFNZCRXNTTWKGSEUBMZXURCQEEPPOKWNSHGEPLFKQLATMWMKQBPKSELDVYVPFAWZSMDBMEFNERSXWRGGMBEXDSFDIQRPIGNZTPTZACHHQDTTASREJDLTFLSJLGKJPJKUXIAGNMIAEUFNKVOGVPBXUOHFBIYQLMRZEJOGHQFSYOUUXBWVCBLFLUDGXJCEXEWQZOHZMLAK";
const IOC: f64 = 0.065;
const ALPHABET_LEN: usize = 26;

mod vigenere {
    pub const ALPHABET_LEN: usize = 26;

    pub fn encrypt(plaintext: char, key: usize, block_index: usize) -> u8 {
        let mut plaintext: i8 = plaintext as i8 - 'A' as i8;
        plaintext += block_index as i8;
        plaintext += key as i8;
        let plaintext: u8 = (plaintext % (ALPHABET_LEN as i8)) as u8;
        plaintext
    }

    pub fn decrypt(ciphertext: char, key: usize, block_index: usize) -> u8 {
        let mut plaintext: i32 = ciphertext as i32 - 'A' as i32;
        plaintext -= block_index as i32;
        plaintext -= key as i32;
        let plaintext =
            ((plaintext % (ALPHABET_LEN as i32)) + (ALPHABET_LEN as i32)) % (ALPHABET_LEN as i32);
        plaintext as u8
    }
}

#[derive(Debug)]
struct CryptoSystem {
    input_string: String,
}

impl CryptoSystem {
    fn new() -> Self {
        let input_string = String::from(INPUT);
        let mut char_count = [0_usize; ALPHABET_LEN];
        for c in input_string.chars() {
            let n = c as usize - 'A' as usize;
            char_count[n] += 1;
        }
        Self { input_string }
    }

    fn input_partition(&self, key_len: usize) -> Vec<String> {
        let mut buf = Vec::new();
        let block_ctr = (self.input_string.len() as f64 / key_len as f64).ceil() as usize;

        for block in 0..block_ctr {
            let mut block_string = String::new();
            let index = block * key_len;
            for i in 0..key_len {
                let sub_index = index + i;
                if sub_index >= self.input_string.len() {
                    break;
                }
                block_string.push(self.input_string.chars().collect::<Vec<char>>()[sub_index]);
            }
            buf.push(block_string);
        }

        buf
    }
}

fn main() {
    let v = CryptoSystem::new();

    // finding key length
    let mut key_len = 1;
    let mut min_ioc = (IOC - calc_ioc(&v.input_partition(key_len))).ceil();

    for block_size in 2..26 {
        let parts = v.input_partition(block_size);
        let ioc = calc_ioc(&parts);
        let diff = 0.065 - ioc;
        if diff < min_ioc {
            min_ioc = diff;
            key_len = block_size;
        }
    }

    println!("key length: {}", key_len);
    // brute forcing key
    let mut buf = Vec::with_capacity(key_len);
    buf.resize(key_len, 0);

    let mut key_ctr = 0;
    let max_key_ctr = ALPHABET_LEN.pow(key_len as u32);
    while key_ctr < max_key_ctr {
        decrypt_ioc(&buf);
        key_ctr += 1;
        buf[key_len - 1] += 1;
        if buf[key_len - 1] < 26 {
            continue;
        }

        // when the last key is maxxed out at 25
        let mut idx = key_len as i32 - 1;
        while idx >= 0 {
            if buf[idx as usize] < 25 {
                buf[idx as usize] += 1;
                break;
            }
            buf[idx as usize] = 0;
            idx -= 1;
        }
    }
}

fn decrypt_ioc(key: &Vec<usize>) -> f64 {
    /*
        println!(
            "[{} {} {} {} {} {}]",
            key[0], key[1], key[2], key[3], key[4], key[5]
        );
    */
    0.0
}

fn calc_ioc(blocks: &Vec<String>) -> f64 {
    let mut char_ctr = [0_usize; vigenere::ALPHABET_LEN];
    for (block_idx, ciphertext) in blocks.iter().enumerate() {
        for v in ciphertext.chars() {
            let decoded = vigenere::decrypt(v, 0, block_idx);
            char_ctr[decoded as usize] += 1;
        }
    }

    char_ctr
        .iter()
        .map(|&v| (v as f64) / INPUT.len() as f64)
        .map(|v| v * v)
        .sum::<_>()
}
