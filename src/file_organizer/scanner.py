from pathlib import Path
from typing import List
from . import rules

def scan_directory(directory_path, recursive=False):
    directory = Path(directory_path)

    if not directory.exists():
        raise FileNotFoundError(f"Directory not found: {directory}")

    if not directory.is_dir():
        raise NotADirectoryError(f"Path is not a directory: {directory}")

    files = []

    if recursive:
        all_items = directory.rglob('*')
    else:
        all_items = directory.iterdir()

    for item in all_items:
        if item.is_dir():
            continue

        if rules.should_ignore(item.name):
            continue
        
        if is_hidden(item):
            continue

        files.append(item)

    return files

def is_hidden(file_path):
    if file_path.name.startswith('.'):
        return True

    for parent in file_path.parents:
        if parent.name.startswith('.'):
            return True
    
    return False

def get_file_count(directory_path, recursive=False):
    files = scan_directory(directory_path, recursive)
    return len(files)

def preview_scan(directory_path, recursive=False, limit=10):
    files = scan_directory(directory_path, recursive)
    return files[:limit]

def get_files_by_category(directory_path, recursive=False):
    files = scan_directory(directory_path, recursive)

    categorized = {}

    for file_path in files:
        category = rules.get_category_for_file(file_path.name)

        if category not in categorized:
            categorized[category] = []

        categorized[category].append(file_path)

    return categorized

if __name__ == "__main__":
    import sys

    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = "."

    print(f"Scanning directory: {test_dir}")
    print("=" * 60)

    try:
        print("\n1. Non-recursive scan:")
        files = scan_directory(test_dir, recursive=False)
        print(f"Found {len(files)} files")

        print("\nFirst 5 files:")
        for file in files[:5]:
            category = rules.get_category_for_file(file.name)
            print(f"  {file.name:30} -> {category}")

        print("\n2. Files grouped by category:")
        categorized = get_files_by_category(test_dir, recursive=False)
        for category, file_list in categorized.items():
            print(f"  {category}: {len(file_list)} files")

        print("\n3. Recursive scan:")
        recursive_files = scan_directory(test_dir, recursive=True)
        print(f"Found {len(recursive_files)} files (including subdirectories)")

    except FileNotFoundError as e:
        print(f"Error: {e}")
    except NotADirectoryError as e:
        print(f"Error: {e}")
    except Exception as e:
        print(f"Unexpected error: {e}")
