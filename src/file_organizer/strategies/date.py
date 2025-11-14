from pathlib import Path
from datetime import datetime
from .base import BaseStrategy

class DateStrategy(BaseStrategy):

    def __init__(self, format='monthly'):
        if format not in ['daily', 'monthly', 'yearly']:
            raise ValueError("Format must be 'daily', 'monthly', or 'yearly'")

        self.format = format

    def get_target_folder(self, file_path):
        file_path = Path(file_path)
        if not file_path.exists():
            modified_time = datetime.now()
        else:
            timestamp = file_path.stat().st_mtime
            modified_time = datetime.fromtimestamp(timestamp)

        if self.format == 'daily':
            return modified_time.strftime('%Y-%m-%d')
        elif self.format == 'monthly':
            return modified_time.strftime('%Y-%m')
        elif self.format == 'yearly':
            return modified_time.strftime('%Y')

    def __str__(self):
        return f"DateStrategy(format={self.format})"

if __name__ == "__main__":
    from pathlib import Path

    print("Date Strategy Test:")
    print("=" * 50)

    formats = ['daily', 'monthly', 'yearly']
    test_file = Path(__file__)

    for fmt in formats:
        strategy = DateStrategy(format=fmt)
        folder = strategy.get_target_folder(test_file)
        print(f"{fmt:10} format -> {folder}")

    print("\nNote: Dates are based on file modification time")