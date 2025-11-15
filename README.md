# File Organizer

A Python command-line tool to automatically organize files by extension type or modification date.

## Features

- **Organization Modes:**
  - **Extension**: Organize files by type (Documents, Images, Videos, etc.)
  - **Date**: Organize files by modification date (daily, monthly, or yearly)

- **Safety Features:**
  - Dry-run mode to preview changes without moving files
  - Automatic conflict resolution (renames duplicates)
  - Error handling and logging

- **Flexible Options:**
  - Recursive directory scanning
  - Custom destination directory
  - Multiple date formats

## Requirements

- Python 3.7+
- No external dependencies (uses Python standard library only)

## Installation

1. Clone the repository:
```bash
git clone <your-repo-url>
cd file-organizer
```

2. No additional installation needed - uses Python standard library only!

## Usage

### Basic Examples

**Preview what would happen (dry-run):**
```bash
python3 organize.py ~/Downloads --dry-run
```

**Organize by file extension:**
```bash
python3 organize.py ~/Downloads --mode extension
```

**Organize by date (monthly):**
```bash
python3 organize.py ~/Documents --mode date --format monthly
```

**Organize recursively (include subdirectories):**
```bash
python3 organize.py ~/Desktop --recursive
```

**Use custom destination:**
```bash
python3 organize.py ~/Downloads --destination ~/Organized
```

### Command-Line Options

```
usage: organize.py [-h] [--mode {extension,date}]
                   [--format {daily,monthly,yearly}]
                   [--destination DESTINATION] [--recursive] [--dry-run]
                   source

positional arguments:
  source                Source directory to organize

options:
  -h, --help            Show help message and exit
  --mode, -m {extension,date}
                        Organization mode (default: extension)
  --format, -f {daily,monthly,yearly}
                        Date format for date mode (default: monthly)
  --destination, -d DESTINATION
                        Destination directory (default: same as source)
  --recursive, -r       Scan subdirectories recursively
  --dry-run             Preview changes without actually moving files
```

## File Categories

When using extension mode, files are organized into these categories:

- **Documents**: `.pdf`, `.doc`, `.docx`, `.txt`, `.rtf`, `.odt`
- **Spreadsheets**: `.xlsx`, `.xls`, `.csv`, `.ods`
- **Presentations**: `.pptx`, `.ppt`, `.odp`, `.key`
- **Text Files**: `.txt`, `.md`, `.log`, `.json`, `.xml`
- **Archives**: `.zip`, `.rar`, `.7z`, `.tar`, `.gz`, `.bz2`
- **Images**: `.jpg`, `.jpeg`, `.png`, `.gif`, `.bmp`, `.svg`
- **Videos**: `.mp4`, `.avi`, `.mkv`, `.mov`, `.wmv`
- **Audio**: `.mp3`, `.wav`, `.flac`, `.aac`, `.ogg`
- **Other**: Unknown file types
- **No_Extension**: Files without extensions

## Date Formats

When using date mode:

- **daily**: `2025-11-15/`
- **monthly**: `2025-11/`
- **yearly**: `2025/`

## Project Structure

```
file-organizer/
├── organize.py              # Entry point script
├── src/
│   └── file_organizer/
│       ├── cli.py           # Command-line interface
│       ├── organizer.py     # Main organization logic
│       ├── scanner.py       # Directory scanning
│       ├── rules.py         # File categorization rules
│       └── strategies/      # Organization strategies
│           ├── base.py
│           ├── extension.py
│           └── date.py
├── README.md
└── requirements.txt
```

## Examples

### Organize Downloads by File Type

```bash
# Preview first
python3 organize.py ~/Downloads --dry-run

# Actually organize
python3 organize.py ~/Downloads
```

**Before:**
```
Downloads/
├── report.pdf
├── photo.jpg
├── data.csv
└── music.mp3
```

**After:**
```
Downloads/
├── Documents/
│   └── report.pdf
├── Images/
│   └── photo.jpg
├── Spreadsheets/
│   └── data.csv
└── Audio/
    └── music.mp3
```

### Organize Documents by Month

```bash
python3 organize.py ~/Documents --mode date --format monthly
```

**Result:**
```
Documents/
├── 2025-11/
│   ├── file1.pdf
│   └── file2.docx
├── 2025-10/
│   └── file3.txt
└── 2024-12/
    └── old_file.pdf
```

## Safety Tips

1. **Always use `--dry-run` first** to preview changes
2. **Backup important files** before organizing
3. **Test on a small directory** first
4. **Check permissions** - macOS users may need to grant Full Disk Access to Terminal

## macOS Permissions

If you get a "Permission denied" error on macOS:

1. Go to **System Settings** → **Privacy & Security**
2. Click **Full Disk Access**
3. Add **Terminal** (or your terminal app)
4. Restart your terminal

## Contributing

Feel free to submit issues or pull requests!

## License

MIT License (or your preferred license)

## Author

zautt
