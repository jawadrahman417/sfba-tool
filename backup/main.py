import os
import argparse
from datetime import datetime
from cryptography.fernet import Fernet

SOURCE_DIR = "source_files"
BACKUP_DIR = "backup"
RESTORE_DIR = "restored_files"
LOG_FILE = "logs/backup_log.txt"
KEY_FILE = "key.key"

# Ensure required directories exist
os.makedirs(BACKUP_DIR, exist_ok=True)
os.makedirs(RESTORE_DIR, exist_ok=True)
os.makedirs(os.path.dirname(LOG_FILE), exist_ok=True)

# Logging function
def log(message):
    with open(LOG_FILE, 'a') as f:
        f.write(f"[{datetime.now()}] {message}\n")

# Load or create key
def load_key():
    if not os.path.exists(KEY_FILE):
        key = Fernet.generate_key()
        with open(KEY_FILE, 'wb') as f:
            f.write(key)
        print("✅ New encryption key created.")
    else:
        print("🔑 Using existing encryption key.")
    with open(KEY_FILE, 'rb') as f:
        return f.read()

# Analyze file for logging
def analyze_file(filepath):
    stats = os.stat(filepath)
    return {
        'name': os.path.basename(filepath),
        'size_kb': stats.st_size // 1024,
        'created': datetime.fromtimestamp(stats.st_ctime),
        'modified': datetime.fromtimestamp(stats.st_mtime)
    }

# Encrypt and backup
def backup_and_encrypt(fernet):
    for filename in os.listdir(SOURCE_DIR):
        src_path = os.path.join(SOURCE_DIR, filename)
        dst_path = os.path.join(BACKUP_DIR, filename + ".enc")

        try:
            with open(src_path, 'rb') as f:
                data = f.read()
            encrypted_data = fernet.encrypt(data)

            with open(dst_path, 'wb') as f:
                f.write(encrypted_data)

            info = analyze_file(src_path)
            log(f"✅ Encrypted '{info['name']}' | Size: {info['size_kb']} KB | Created: {info['created']}")
            print(f"✔️ Encrypted: {filename}")
        except Exception as e:
            log(f"❌ Failed to backup '{filename}': {e}")
            print(f"❌ Error: {filename} — {e}")

# Decrypt and restore
def decrypt_and_restore(fernet):
    for filename in os.listdir(BACKUP_DIR):
        if not filename.endswith(".enc"):
            continue

        enc_path = os.path.join(BACKUP_DIR, filename)
        orig_name = filename.replace(".enc", "")
        restore_path = os.path.join(RESTORE_DIR, orig_name)

        try:
            with open(enc_path, 'rb') as f:
                encrypted_data = f.read()
            decrypted_data = fernet.decrypt(encrypted_data)

            with open(restore_path, 'wb') as f:
                f.write(decrypted_data)

            log(f"✅ Restored '{orig_name}' from encrypted backup.")
            print(f"🔓 Restored: {orig_name}")
        except Exception as e:
            log(f"❌ Failed to restore '{filename}': {e}")
            print(f"❌ Error: {filename} — {e}")

# Main logic
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Secure File Backup & Restore")
    parser.add_argument('--decrypt', action='store_true', help="Decrypt and restore files")
    args = parser.parse_args()

    key = load_key()
    fernet = Fernet(key)

    if args.decrypt:
        decrypt_and_restore(fernet)
    else:
        backup_and_encrypt(fernet)
