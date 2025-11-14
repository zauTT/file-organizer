from abc import ABC, abstractmethod
from pathlib import Path

class BaseStrategy(ABC):
    @abstractmethod
    def get_target_folder(self, file_path):
        pass

    def get_file_info(self, file_path):
        file_path = Path(file_path)

        return {
            'name': file_path.name,
            'stem': file_path.stem,
            'suffix': file_path.suffix,
            'size': file_path.stat().st_size if file_path.exists() else 0,
            'modified': file_path.stat().st_mtime if file_path.exists() else 0,
        }

    def __str__(self):
        return self.__class__.__name__