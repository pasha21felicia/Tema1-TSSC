I'm glad that the solution worked for you. Here's a brief and clear explanation of how the code works:

Import the necessary libraries (AES for encryption/decryption and base64 for encoding/decoding).

Set the server's provided parameters for the Diffie-Hellman key exchange: the prime number p, the generator g, and the server's public key my_pub. Also, set the block size and padding for AES encryption.

Set your public key to p - 1. This is the key you will send to the server during the Diffie-Hellman key exchange.

The server calculates the shared secret as pow(yours, my_priv, p). Due to Fermat's Little Theorem, when your public key is p - 1, the shared secret becomes p - 1.

Convert the shared secret p - 1 to bytes and truncate it to the required block size (32 bytes in this case) to use as the decryption key for AES.

Decode the base64-encoded encrypted flag provided by the server.

Decrypt the flag using the AES cipher in ECB mode and the derived key. Since the flag was padded with null bytes (b'\x00'), remove the padding by calling rstrip(PADDING).

Decode the decrypted flag bytes as an ASCII string and print the flag.

By setting your public key to p - 1, you cause the server to calculate a shared secret that allows you to decrypt the flag successfully. The key to this solution is understanding the properties of the modulo operation and exploiting Fermat's Little Theorem to generate a predictable shared secret.