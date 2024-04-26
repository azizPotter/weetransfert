from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import base64
import os
import hashlib


class CryptoService: 
    def __init__(self):
         self.private_key = self.load_or_generate_private_key()

    def load_or_generate_private_key(self):
        private_key_path = os.getenv("PRIVATE_KEY_PATH")
        if private_key_path and os.path.exists(private_key_path) and os.path.getsize(private_key_path) > 0:
            # Load the private key from the file if it exists and is not empty
            with open(private_key_path, "rb") as key_file:
                private_key = serialization.load_pem_private_key(
                    key_file.read(),
                    password=None,
                    backend=default_backend()
                )
        else:
            # Generate a new private key if the file doesn't exist or is empty
            private_key = rsa.generate_private_key(
                public_exponent=65537,
                key_size=2048,
                backend=default_backend()
            )
            # Save the private key to the file
            with open(private_key_path, "wb") as key_file:
                key_file.write(
                    private_key.private_bytes(
                        encoding=serialization.Encoding.PEM,
                        format=serialization.PrivateFormat.TraditionalOpenSSL,
                        encryption_algorithm=serialization.NoEncryption()
                    ) 
                )
        return private_key

    def hash_data(self, data):
        # Create a hash object using SHA-256
        digest = hashlib.sha256()
        # Update the hash object with the data
        digest.update(data.encode())
        # Get the hexadecimal representation of the hash
        hashed_data = digest.hexdigest()
        return hashed_data

    def generate_key(from_email, to_email):
        # GENERATE A KEY WITH USER EMAIL
        key = hashlib.sha256((from_email + to_email).encode()).digest()
        return key

    def encrypt_url(self, file_path, from_email, to_email):
        # ENCRYPT URL
        key =  CryptoService.generate_key(from_email, to_email)
        cipher = AES.new(key, AES.MODE_CBC, iv=get_random_bytes(16))
        encrypted_url = cipher.encrypt(pad(file_path.encode(), AES.block_size))
        return base64.b64encode(cipher.iv + encrypted_url).decode()

    def decrypt_url(self, file_path_crypted, from_email, to_email):
        # DECRYPT URL
        key = CryptoService.generate_key(from_email, to_email)
        file_path_crypted = base64.b64decode(file_path_crypted.encode())
        iv = file_path_crypted[:16]
        ciphertext = file_path_crypted[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_url = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
        return decrypted_url