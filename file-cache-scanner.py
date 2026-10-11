import os
import json
import hashlib

def get_file_sha256(full_path):
    """Calculates the SHA256 hash of a file block by block for efficiency."""
    sha256_hash = hashlib.sha256()
    try:
        with open(full_path, "rb") as f:
            for byte_block in iter(lambda: f.read(4096), b""):
                sha256_hash.update(byte_block)
        return sha256_hash.hexdigest()
    except Exception:
        return None

def build_directory_cache():
    root_dir = os.path.dirname(os.path.abspath(__file__))
    
    file_cache = {}
    directories_list = []
    files_list = []

    print(f"Scanning directory: {root_dir}\n")

    for dirpath, dirnames, filenames in os.walk(root_dir):
        rel_dir = os.path.relpath(dirpath, root_dir)
        if rel_dir == ".":
            rel_dir = ""

        # Collect directories
        for d in dirnames:
            folder_path = os.path.join(rel_dir, d) if rel_dir else d
            full_folder_path = os.path.join(dirpath, d)
            directories_list.append({
                "path": folder_path,
                "full_path": full_folder_path
            })

        # Collect files
        for f in filenames:
            file_rel_path = os.path.join(rel_dir, f) if rel_dir else f
            
            # Skip the script itself from self-caching in real-time
            full_path = os.path.join(dirpath, f)
            if os.path.abspath(__file__) == full_path:
                continue

            # Calculate SHA256 hash
            file_hash = get_file_sha256(full_path)

            # Prepare cache entry
            cache_entry = {
                "full_path": full_path,
                "sha256": file_hash
            }

            try:
                # Try to read as a text file in UTF-8 encoding
                with open(full_path, "r", encoding="utf-8") as file_obj:
                    content = file_obj.read()
                    cache_entry["status"] = "cached_text"
                    cache_entry["data"] = content
            except UnicodeDecodeError:
                # If the file is binary, read it in bytes
                try:
                    with open(full_path, "rb") as file_obj:
                        binary_data = file_obj.read()
                        cache_entry["status"] = "cached_binary_bytes"
                        cache_entry["size_bytes"] = len(binary_data)
                except Exception as e:
                    cache_entry["status"] = "error"
                    cache_entry["message"] = str(e)
            except Exception as e:
                cache_entry["status"] = "error"
                cache_entry["message"] = str(e)

            file_cache[file_rel_path] = cache_entry
            files_list.append({
                "path": file_rel_path,
                "full_path": full_path,
                "sha256": file_hash
            })

    return {
        "root_directory": root_dir,
        "directories": directories_list,
        "files": files_list,
        "cache": file_cache
    }

if __name__ == "__main__":
    result = build_directory_cache()

    print("=== DIRECTORIES LIST ===")
    for folder in result["directories"]:
        print(f"[DIR]  {folder['full_path']}")

    print("\n=== FILES LIST (SHA256 + FULL PATH) ===")
    for file_info in result["files"]:
        print(f"SHA256: {file_info['sha256']}  |  PATH: {file_info['full_path']}")

    print(f"\nTotal directories: {len(result['directories'])}, Total files: {len(result['files'])}")
