import os
from collections import defaultdict

def analyze_folder(folder_path):
    file_types = defaultdict(int)
    files_seen = set()
    duplicates = []
    suspicious = []

    for filename in os.listdir(folder_path):
        ext = os.path.splitext(filename)[1]
        file_types[ext] += 1

        if filename in files_seen:
            duplicates.append(filename)
        else:
            files_seen.add(filename)

        if filename.lower().startswith("hack") or "virus" in filename.lower():
            suspicious.append(os.path.join(folder_path, filename))

    return file_types, duplicates, suspicious

def print_analysis(file_types, duplicates, suspicious):
    print("\n📊 File Types:")
    for ext, count in file_types.items():
        print(f"{ext or 'no extension'}: {count}")

    print("\n🧬 Duplicate Files:")
    print("\n".join(duplicates) if duplicates else "None")

    print("\n🚩 Suspicious Files:")
    print("\n".join(suspicious) if suspicious else "None")
