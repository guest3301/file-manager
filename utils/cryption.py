import os, time, base64
import sys

from cryptography.fernet import Fernet
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

from utils.utils import scan_recurse

class Encryptor:
    def __init__(self, BASE_DIR): 
        self.key = None
        self.files = None
        self.BASE_DIR = BASE_DIR
        try:
            self.files = [item for item in scan_recurse(self.BASE_DIR) if item != "key.key"]
        except Exception as e:
            print(f"Exception: {e}")

    def derive_key(self, password):
        if isinstance(password, str):
            password = password.encode()
      # Fernet.generate_key()
        salt = b'somesuperrandomstuff' # os.urandom(16) 
        kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(),
        length=32,  # 256-bit key
        salt=salt,
        iterations=100000,
        backend=default_backend()
        )
        self.key = base64.urlsafe_b64encode(kdf.derive(password)) 
        return self.key

    def encrypt(self, password):
        self.key = self.derive_key(password)
        key_to_share = self.key
        try:
            self.files = [item for item in scan_recurse(self.BASE_DIR) if item != "key.key"]
        except Exception as e:
            print(f"Exception: {e}")
            return []
        for file in self.files.copy():
            try:
                if not os.path.isfile(file):
                    print(f"{file} not found or is not a file, skipping.")
                    continue
                if str(file.path).endswith('.enc'):
                    continue
                with open(file, 'rb') as f_in:
                    with open(str(file.path) + '.enc', 'wb') as f_out:
                        for chunk in iter(lambda: f_in.read(2 * 1024 * 1024), b''):
                            encrypted_chunk = Fernet(self.key).encrypt(chunk)
                            print(f"Encrypting {file.name} {len(chunk)};", end="\r")
                            f_out.write(encrypted_chunk)
                os.unlink(file.path)
                print(f'Encrypted: {file.path}')
            except Exception as e:
                print(f"Error encrypting {file}: {e}\nI care about you, alot. The key is here: {str(key_to_share.decode())}\nGood luck!")
        self.key = None
        return self.files, str(key_to_share.decode())
    
    def decrypt(self, keyy):
        try:
            # Validate the key length
            if len(base64.urlsafe_b64decode(keyy)) != 32:
                raise ValueError("Invalid key length. Key must be 32 url-safe base64-encoded bytes.")
            
            self.files = [item for item in scan_recurse(self.BASE_DIR) if item != "key.key"]
        except Exception as e:
            print(f"Exception: {e}")
            return []
        for file in self.files.copy():
            
                print(f"Decrypting {file}...", end="\r")
                if not os.path.isfile(file):
                    print(f"{file} not found or is not a file, skipping.")
                    continue
                if not str(file.path).endswith('.enc'):
                    continue
                with open(file, 'rb') as f_in:
                    with open(str(os.path.splitext(file.path)[0]), 'wb') as f_out:
                        try:
                            for chunk in iter(lambda: f_in.read(2 * 1024 * 1024), b''):
                                decrypted_chunk = Fernet(keyy).decrypt(chunk)
                                f_out.write(decrypted_chunk)
                        except:
                            for chunk in iter(lambda: f_in.read(100 * 1024 * 1024), b''):
                                decrypted_chunk = Fernet(keyy).decrypt(chunk)
                                f_out.write(decrypted_chunk)
                os.unlink(file.path)
                print(f'Decrypted: {file.path}')
                return self.files
            

def main():
    encryptor = Encryptor()
    encryptor.derive_key()  # Generate the encryption key
    print("(E)ncrypt/(D)ecrypt: ")
    opt = input().upper()
    if opt == "E":
        encryptor.encrypt(encryptor.key)
        encryptor.backup_key(encryptor.key)
        print("Encrypted.")
        print("key", encryptor.key)
    elif opt == "D":
        encryptor.decrypt(encryptor.key)
    else:
        print("Invalid option. Please choose (E) or (D).")
    return "Task finished"

if __name__ == "__main__":
    main()
'''
import time

def my_function():
 # Simulate some work
 for i in range(100000):
   pass

start_time = time.time()
my_function()
end_time = time.time()

execution_time = end_time - start_time
print(f"Execution time: {execution_time} seconds")
'''