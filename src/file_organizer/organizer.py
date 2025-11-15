from pathlib import Path
import shutil
from typing import List, Dict, Optional
from . import scanner, rules
from .strategies.base import BaseStrategy

class FileOrganizer:
    def __init__(self, strategy: BaseStrategy, dry_run=False):
        self.strategy = strategy
        self.dry_run = dry_run
        self.operations_log = []

    def organize(self, source_dir, destination_dir=None, recursive=False):
        source_path = Path(source_dir)

        if destination_dir is None:
            destination_dir = source_path
        else:
            destination_dir = Path(destination_dir)

        if not source_path.exists():
            raise FileNotFoundError(f"Source directory not found {source_path}")
        print(f"Scanning {source_path}...")
        files = scanner.scan_directory(source_path, recursive=recursive)

        if not files:
            print("No files to organize.")
            return {'files_processed': 0, 'categories': {}}

        print(f"Found {len(files)} files to organize")

        organized = self._categorize_files(files)

        stats = self._execute_operations(organized, destination_dir)

        return stats

    def _categorize_files(self, files: List[Path]) -> Dict[str, List[Path]]:
        categorized = {}

        for file_path in files:
            target_folder = self.strategy.get_target_folder(file_path)

            if target_folder not in categorized:
                categorized[target_folder] = []

            categorized[target_folder].append(file_path)
        return categorized

    def _execute_operations(self, categorized: Dict[str, List[Path]], destination_dir: Path) -> dict:
        stats = {
            'files_processed': 0,
            'files_moved': 0,
            'categories': {},
            'errors': []
        }

        for target_folder, files in categorized.items():
            target_path = destination_dir / target_folder

            if self.dry_run:
                print(f"\n[DRY RUN] Would create: {target_path}")
            else:
                target_path.mkdir(parents=True, exist_ok=True)
                print(f"\nProcessing: {target_folder}/")

            for file_path in files:
                stats['files_processed'] += 1

                try:
                    success = self._move_file(file_path, target_path)
                    if success:
                        stats['files_moved'] += 1

                        if target_folder not in stats['categories']:
                            stats['categories'][target_folder] = 0
                        stats['categories'][target_folder] += 1

                except Exception as e:
                    error_msg = f"Error moving {file_path.name}: {e}"
                    stats['errors'].append(error_msg)
                    print(f"  ✗ {error_msg}")

        return stats

    def _move_file(self, source: Path, target_dir: Path) -> bool:
        destination = target_dir / source.name

        if destination.exists():
            destination = self._resolve_conflict(destination)

        if self.dry_run:
            print(f"  [DRY RUN] {source.name} -> {target_dir.name}/")
            self.operations_log.append(('move', source, destination))
            return True
        else:
            shutil.move(str(source), str(destination))
            print(f"  ✓ {source.name}")
            self.operations_log.append(('move', source, destination))
            return True

    def _resolve_conflict(self, file_path: Path) -> Path:
        counter = 1
        stem = file_path.stem
        suffix = file_path.suffix
        parent = file_path.parent

        while file_path.exists():
            file_path = parent / f"{stem}_{counter}{suffix}"
            counter += 1

        return file_path

    def get_operations_log(self):
        return self.operations_log

    def print_summary(self, stats: dict):
        print("\n" + "=" * 60)
        if self.dry_run:
            print("DRY RUN")
        else:
            print("ORGANIZATION COMPLETE")
        print("=" * 60)

        print(f"Files processed: {stats['files_processed']}")
        print(f"Files moved: {stats['files_moved']}")

        if stats['categories']:
            print(f"\nFiles organized into {len(stats['categories'])} categories:")

            for category, count in stats['categories'].items():
                print(f"  {category}: {count} files")

        if stats['errors']:
            print(f"\nErrors: {len(stats['errors'])}")
            for error in stats['errors']:
                print(f"  - {error}")

if __name__ == "__main__":
    from .strategies.extension import ExtensionStrategy
    from .strategies.date import DateStrategy

    print("File Organizer Test")
    print("=" * 60)

    print("\nExample 1: Extension-based organization (DRY RUN)")
    print("=" * 60)

    strategy = ExtensionStrategy()
    organizer = FileOrganizer(strategy, dry_run=True)

    try:
        stats = organizer.organize(".", recursive=False)
        organizer.print_summary(stats)
    except Exception as e:
        print(f"Error: {e}")

    print("\n\nExample 2: Date-based organization (DRY RUN)")
    print("-" * 60)
    date_strategy = DateStrategy(format='monthly')
    date_organizer = FileOrganizer(date_strategy, dry_run=True)

    try:
        stats = date_organizer.organize(".", recursive=False)
        date_organizer.print_summary(stats)
    except Exception as e:
        print(f"Error: {e}")
