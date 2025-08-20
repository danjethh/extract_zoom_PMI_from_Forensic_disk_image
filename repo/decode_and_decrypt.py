from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
import base64

# Input data
ciphertext_base64 = "gbfE5IKzmC1pUyRavQCa/oAz4yMQH9jWHftjfLlHM4RBfJeyFzOkXrmnZWXK+qPr8wxt7Y5sN1tviV2791Nn/IkRflbt6trFmC4fLrvT1KipEqkGGgtGo1T5q2hVJYxo1zuVEBpVHyQRpqYT62wvSA=="
key_hex = "517DA8C53C8EE388DFC457D05FC43912A8A9D75F665FEDE3508560C59DADC112"
iv_hex = "78334c44bdcda4e0124b0430c2a627d4"

# Decode the base64 encoded ciphertext
ciphertext = base64.b64decode(ciphertext_base64)

# Convert hexadecimal strings to bytes
key = bytes.fromhex(key_hex)
iv = bytes.fromhex(iv_hex)

# Create an AES cipher object
cipher = AES.new(key, AES.MODE_CBC, iv)

# Decrypt the ciphertext and remove padding
plaintext = unpad(cipher.decrypt(ciphertext), AES.block_size)

# Convert the plaintext to a string
plaintext_str = plaintext.decode('utf-8')

# Print the decrypted plaintext
print("Decrypted Text:", plaintext_str)
