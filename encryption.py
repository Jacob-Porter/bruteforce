from Crypto.Cipher import AES
import itertools
import string
import random

# plaintext = b'[REDACTED(ha ha!)] A N D DOJAND You osdBesda'

# key_string = ''.join(random.choices(string.ascii_uppercase, k=6))
# key_string = key_string + key_string + key_string + key_string
# print(key_string)
# key_bytes = bytes(key_string, 'utf-8')
# key = key_bytes

# cipher_enc = AES.new(key, AES.MODE_EAX)
# nonce = cipher_enc.nonce
# ciphertext, tag = cipher_enc.encrypt_and_digest(plaintext)

# ciphertext = b''
# nonce = b''



# key = "AAAA"*4
# key = bytes(key, 'utf-8')
#print("key:", key)




def generate_combinations_and_decrypt(ciphertext, nonce, common_words):
    combinations = itertools.product(string.ascii_uppercase, repeat=6)
    count = 0
    for combination in combinations:
        count += 1
        if count % 1000000 == 0: # print every 1 million iterations for my sanity
            print(count)
        key = ''.join(combination * 4)
        key_bytes = bytes(key, 'utf-8') # key in bytes
        cipher_dec = AES.new(key_bytes, AES.MODE_EAX, nonce=nonce)
        plaintext = cipher_dec.decrypt(ciphertext)
        
        try:
            plaintext_decoded = plaintext.decode('utf-8')
            # count how many common_words were found in the plaintext
            n = sum(1 for word in common_words if word in plaintext_decoded.upper())
            
            # Write the plaintext and key to a file
            with open(f"plaintext_{n}.txt", "a", encoding='utf-8') as file:
                file.write(f"{key_bytes.decode('utf-8')}\n{plaintext_decoded}\n\n")
                print("!! potential find !!")
        
        except UnicodeDecodeError:
            # Skip any keys that result in decoding errors
            continue


# Assuming ciphertext and nonce have been read from files as binary
ciphertext = b''
with open("ciphertext", "rb") as f:
    ciphertext = f.read()

nonce = b''
with open("nonce", "rb") as f:
    nonce = f.read()

common_words = ["THE", "AND", "HAVE", "YOU", "BE", "THAT", "GOOD"]

print('ciphertext:', ciphertext)
print('nonce:', nonce)

print('starting')
generate_combinations_and_decrypt(ciphertext, nonce, common_words)
print('finish')