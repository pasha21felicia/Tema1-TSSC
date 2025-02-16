# import the libraries for AES decrypt/encrypt
from Crypto.Cipher import AES
import base64

# FIRST PART OF THE SCRIPT, RUN LIKE THIS AND TAKE NOTE OF Your public key (yours)

# Server's provided parameters
p = 150043801044950244101982965055686596126318041393119861817227788947655736600543
g = 2
my_pub = 11121529160866467219908814286940075860606556119693900365005105132087728382175
BLOCK_SIZE = 32
PADDING = b'\x00'

# Calculate the multiplicative inverse of my_pub (mod p)
yours = p - 1
print("Your public key:", yours)


# SECOND PART OF THE SCRIPT
# decomment the lines below and add at line 26 the encrypted flag from the server, run the full script

# shared = p - 1
# key = shared.to_bytes((shared.bit_length() + 7) // 8, byteorder='big')[0:BLOCK_SIZE]

# # Encrypted flag from the server
# encrypted_flag = base64.b64decode('pUY54eNOtlpeH3zc8GaVPNrLy3rC4XXqgWoYR8sTKS8c/j2sLJqr1C9KsTpS1ruWJfXgplpYmXKFGtNdetN2MA==')

# # Decrypt the flag
# cipher = AES.new(key, AES.MODE_ECB)
# flag = cipher.decrypt(encrypted_flag).rstrip(PADDING).decode("ASCII")
# print("Decrypted flag:", flag)
