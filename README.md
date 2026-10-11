# File Cache Scanner

A lightweight, standalone Python utility designed to scan a project directory, build a structured tree of folders and files, calculate **SHA256 hashes** for integrity verification, and cache file contents (handling both text and binary data).

## 🚀 Features

- **Recursive Scanning:** Automatically traverses the directory where it is executed.
- **Crypto Integrity:** Computes block-by-block `SHA256` hashes for every file.
- **Smart Caching:** Safely reads text files as UTF-8 strings and handles binary files (`.exe`, `.dll`, etc.) as raw byte streams without crashing.
- **Zero Dependencies:** Relies entirely on Python's standard library (`os`, `json`, `hashlib`).

---

## 📦 Usage

Run the script using your Python environment:

```powershell
python file-cache-scanner.py
