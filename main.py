import os
import shutil
import argparse
from datetime import datetime

# Directories and log file path
SOURCE_DIR = "source_files"
BACKUP_DIR = "backup"
LOG_FILE = "logs/backup_log.txt"

# Ensure required folders exist
os.makedirs(SOURCE_DIR, exist_ok=True)
os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

def log(message):
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{datetime.now()}] {message}\n")

def analyze_file(filepath):
    stats = os.stat(filepath)
    return {
        'name': os.path.basename(filepath),
        'size_kb': stats.st_size // 1024,
        'created': datetime.fromtimestamp(stats.st_ctime),
        'modified': datetime.fromtimestamp(stats.st_mtime)
    }

def basic_encrypt(content, key=5):
    return ''.join([chr((ord(char) + key) % 256) for char in content])

def basic_decrypt(content, key=5):
    return ''.join([chr((ord(char) - key) % 256) for char in content])

def backup_and_encrypt():
    for filename in os.listdir(SOURCE_DIR):
        src_path = os.path.join(SOURCE_DIR, filename)
        dst_path = os.path.join(BACKUP_DIR, filename + ".enc")

        print(f"🔒 Encrypting: {filename}...")

        with open(src_path, 'r', encoding='utf-8', errors='ignore') as f:
            data = f.read()

        encrypted_data = basic_encrypt(data)

        with open(dst_path, 'w', encoding='utf-8') as f:
            f.write(encrypted_data)

        info = analyze_file(src_path)
        log(f"Encrypted: '{info['name']}' | Size: {info['size_kb']} KB | Created: {info['created']}")

    print("\n✔️ Backup and encryption complete.")

def decrypt_files():
    for filename in os.listdir(BACKUP_DIR):
        if not filename.endswith(".enc"):
            continue

        src_path = os.path.join(BACKUP_DIR, filename)
        dst_path = os.path.join(BACKUP_DIR, filename.replace(".enc", ".dec"))

        try:
            print(f"🔓 Decrypting: {filename}...")
            with open(src_path, 'r', encoding='utf-8', errors='ignore') as f:
                encrypted_data = f.read()

            decrypted_data = basic_decrypt(encrypted_data)

            with open(dst_path, 'w', encoding='utf-8') as f:
                f.write(decrypted_data)

            info = analyze_file(dst_path)
            print(f"✅ Decrypted: {filename} | Output: {info['name']} | Size: {info['size_kb']} KB")
            log(f"Decrypted: {filename} | Output: {info['name']} | Size: {info['size_kb']} KB")

        except Exception as e:
            print(f"❌ Error: {filename} — {str(e)}")
            log(f"Decryption error for {filename}: {str(e)}")

    print("\n✔️ Basic decryption complete.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Secure File Backup & Analyzer (SFBA)")
    parser.add_argument('--basic-decrypt', '--decrypt', dest='basic_decrypt', action='store_true', help="Decrypt using basic Caesar-style method")
    args = parser.parse_args()

    if args.basic_decrypt:
        decrypt_files()
    else:
        backup_and_encrypt()
