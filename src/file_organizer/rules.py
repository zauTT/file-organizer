from pathlib import Path

DEFAULT_RULES = {
      "Documents": [".pdf", ".doc", ".docx", ".txt", ".rtf", ".odt"],
      "Spreadsheets": [".xlsx", ".xls", ".csv", ".ods"],
      "Presentations": [".pptx", ".ppt", ".odp", ".key"],
      "Text_Files": [".txt", ".md", ".log", ".json", ".xml"],
      "Archives": [".zip", ".rar", ".7z", ".tar", ".gz", ".bz2"],
}

IGNORED_FILES = {
    ".DS_Store",
    "Thumbs.db",
    "desktop.ini",
    ".gitkeep",
    ".gitignore"
}

DEFAULT_CATEGORY = "Other"

NO_EXTENSION_CATEGORY = "No_Extension"

def get_category_for_file(filename):
    extension = Path(filename).suffix

    if not extension:
        return NO_EXTENSION_CATEGORY

    extension = extension.lower()

    for category, extensions in DEFAULT_RULES.items():
        if extension in extensions:
            return category

    return DEFAULT_CATEGORY

def should_ignore(filename):
    name = Path(filename).name

    if name in IGNORED_FILES:
        return True

    return False

def normalize_extension(filename):
    extension = Path(filename).suffix
    return extension.lower() if extension else ""

def get_all_extensions():
    all_extensions = [
        ext
        for extensions in DEFAULT_RULES.values()
        for ext in extensions
    ]
    return all_extensions

def get_all_categories():
    return list(DEFAULT_RULES.keys())

if __name__ == "__main__":
    test_files = [
        "report.pdf",
        "data.CSV",
        "presentation.PPTX",
        "unknown.xyz",
        "noextension",
        ".DS_Store",
    ]

    print("Testing file categorization:")
    print("=" * 40)
    for file in test_files:
        if should_ignore(file):
            print(f"{file:20} -> IGNORED")
        else:
            category = get_category_for_file(file)
            print(f"{file:20} -> {category}")

    print("\nAll known extensions:", len(get_all_extensions()))
    print("All categories:", get_all_categories)

