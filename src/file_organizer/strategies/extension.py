from pathlib import Path
from .. import rules
from .base import BaseStrategy

class ExtensionStrategy(BaseStrategy):

    def get_target_folder(self, file_path):
        file_path = Path(file_path)

        category = rules.get_category_for_file(file_path.name)

        return category

if __name__ == "__main__":
    strategy = ExtensionStrategy()

    test_files = [
        "report.pdf",
        "photo.JPG",
        "data.csv",
        "presentation.pptx",
        "unknown.xyz",
        "noextension"
    ]

    print("Extension Strategy Test:")
    print("=" * 50)
    for filename in test_files:
        folder = strategy.get_target_folder(Path(filename))
        print(f"{filename:25} -> {folder}")