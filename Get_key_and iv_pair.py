import hashlib

sid = b"S-1-5-21-1700811478-3337692859-4283507474-1001"

# Calculate the SHA-256 hash for the SID
key = hashlib.sha256(sid).digest()

# Hash the key itself
iv = hashlib.sha256(key).digest()

# Extract the first 16 bytes (128 bits) for the initialization vector (IV)
iv = iv[:16]

# Print the key and IV in hexadecimal format
print("Key:", " ".join(format(n, '02x') for n in key))
print("IV:", " ".join(format(n, '02x') for n in iv))
