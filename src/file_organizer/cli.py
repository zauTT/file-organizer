import sys
import argparse
from pathlib import Path
from . import organizer
from .strategies.extension import ExtensionStrategy
from .strategies.date import DateStrategy

def create_parser():
    parser = argparse.ArgumentParser(
        description='Organize files by extensions or date',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
  Examples:
    %(prog)s ~/Downloads --mode extension --dry-run
    %(prog)s ~/Documents --mode date --format monthly
    %(prog)s . --mode extension --recursive
    %(prog)s ~/Desktop --mode date --format daily --destination ~/Organized
        """
    )

    parser.add_argument(
        'source',
        help='Source directory to organize'
    )

    parser.add_argument(
        '--mode', '-m',
        choices=['extension', 'date'],
        default='extension',
        help='Organization mode (default: extension)'
    )

    parser.add_argument(
        '--format', '-f',
        choices=['daily', 'monthly', 'yearly'],
        default='monthly',
        help='Date format for date mode (default: monthly)'
    )

    parser.add_argument(
        '--destination', '-d',
        help='Destination directory (default: same as source)'
    )

    parser.add_argument(
        '--recursive', '-r',
        action='store_true',
        help='Scan subdirectories recursively'
    )

    parser.add_argument(
        '--dry-run',
        action='store_true',
        help='Preview changes without actually moving files'
    )

    return parser


def main():
    parser = create_parser()
    args = parser.parse_args()

    source_path = Path(args.source)
    if not source_path.exists():
        print(f"Error: Source directory not found: {source_path}")
        sys.exit(1)

    if not source_path.is_dir():
        print(f"Error: Source is not a directory: {source_path}")
        sys.exit(1)
    
    if args.mode == 'extension':
        strategy = ExtensionStrategy()
        print(f"Using extension-based organization")
    elif args.mode == 'date':
        strategy = DateStrategy(format=args.format)
        print(f"Using date-based organization (format: {args.format})")
    else:
        print(f"Error: Unknown mode: {args.mode}")
        sys.exit(1)

    print(f"Source: {source_path}")
    if args.destination:
        print(f"Destination: {args.destination}")
    if args.recursive:
        print("Recursive: Yes")
    if args.dry_run:
        print("DRY RUN MODE - No files will be moved")

    print("\n" + "-" * 60)

    file_organizer = organizer.FileOrganizer(strategy, dry_run=args.dry_run)

    try:
        stats = file_organizer.organize(
            source_dir=args.source,
            destination_dir=args.destination,
            recursive=args.recursive
        )

        file_organizer.print_summary(stats)

        if stats['errors']:
            sys.exit(1)
        else:
            sys.exit(0)

    except KeyboardInterrupt:
        print("\n\nOperation cancelled by user.")
        sys.exit(130)

if __name__ == "__main__":
    main()