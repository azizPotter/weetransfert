from Crypto.Cipher import AES
from Crypto.Random import get_random_bytes
from Crypto.Util.Padding import pad, unpad
import hashlib
import base64

class UrlService:
    @staticmethod
    def generate_key(from_email, to_email):
        # Générer une clé de 32 octets à partir des e-mails
        key = hashlib.sha256((from_email + to_email).encode()).digest()
        return key

    @staticmethod
    def encrypt_url(file_path, from_email, to_email):
        # Chiffrer l'URL
        key = UrlService.generate_key(from_email, to_email)
        cipher = AES.new(key, AES.MODE_CBC, iv=get_random_bytes(16))
        encrypted_url = cipher.encrypt(pad(file_path.encode(), AES.block_size))
        return base64.b64encode(cipher.iv + encrypted_url).decode()

    @staticmethod
    def decrypt_url(file_path_crypted, from_email, to_email):
        # Déchiffrer l'URL
        key = UrlService.generate_key(from_email, to_email)
        file_path_crypted = base64.b64decode(file_path_crypted.encode())
        iv = file_path_crypted[:16]
        ciphertext = file_path_crypted[16:]
        cipher = AES.new(key, AES.MODE_CBC, iv)
        decrypted_url = unpad(cipher.decrypt(ciphertext), AES.block_size).decode()
        return decrypted_url