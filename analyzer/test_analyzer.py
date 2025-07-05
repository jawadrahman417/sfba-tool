# test_analyze.py
from analyzer.file_analyzer import analyze_folder, print_analysis

folder = 'source_files'  # or any folder you want to scan
file_types, duplicates, suspicious = analyze_folder(folder)
print_analysis(file_types, duplicates, suspicious)
