import os
from cryptography.fernet import Fernet

def load_key(key_path='key.key'):
    with open(key_path, 'rb') as f:
        return f.read()

def decrypt_folder(folder_path, key_path='key.key', output_folder='restored_files'):
    key = load_key(key_path)
    fernet = Fernet(key)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for filename in os.listdir(folder_path):
        if filename.endswith('.enc'):
            enc_path = os.path.join(folder_path, filename)
            dec_path = os.path.join(output_folder, filename.replace('.enc', '.dec'))

            with open(enc_path, 'rb') as f:
                encrypted = f.read()

            decrypted = fernet.decrypt(encrypted)

            with open(dec_path, 'wb') as f:
                f.write(decrypted)

            print(f"Decrypted: {filename}")
