import os
from cryptography.fernet import Fernet

def generate_key(key_path='key.key'):
    key = Fernet.generate_key()
    with open(key_path, 'wb') as f:
        f.write(key)

def load_key(key_path='key.key'):
    with open(key_path, 'rb') as f:
        return f.read()

def encrypt_folder(folder_path, key_path='key.key', output_folder='logs'):
    key = load_key(key_path)
    fernet = Fernet(key)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)

        with open(file_path, 'rb') as f:
            data = f.read()

        encrypted_data = fernet.encrypt(data)

        enc_file = os.path.join(output_folder, filename + '.enc')
        with open(enc_file, 'wb') as f:
            f.write(encrypted_data)

        print(f"Encrypted: {filename}")
