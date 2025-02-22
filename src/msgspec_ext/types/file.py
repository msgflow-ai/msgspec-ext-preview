from pathlib import Path
from typing import Any
from msgspec import ValidationError


__all__ = ["FilePath"]


class FilePath:
    """A type for file system paths with validation."""

    def __init__(self, path: str, *, check_exists: bool = True):
        self.path = Path(path)
        self._check_exists = check_exists
        if check_exists:
            self._validate_exists()

    @classmethod
    def validate(cls, value: Any, *, check_exists: bool = True) -> "FilePath":
        """
        Validates a file path.
        
        Args:
            value: The path string to validate
            check_exists: Whether to verify if the path exists
            
        Returns:
            FilePath instance
        """
        if isinstance(value, Path):
            path_str = str(value)
        elif isinstance(value, str):
            path_str = value
        else:
            raise ValidationError(f"Path must be a string or Path object, got {type(value).__name__}")

        try:
            path = Path(path_str)
            if path.is_absolute():
                resolved_path = path.resolve()
            else:
                resolved_path = Path.cwd() / path
        except Exception as e:
            raise ValidationError(f"Invalid path format: {str(e)}")

        return cls(str(resolved_path), check_exists=check_exists)

    def _validate_exists(self) -> None:
        """ Checks if path exists in file system """
        if not self.path.exists():
            raise ValidationError(f"Path does not exist: {self.path}")

    @property
    def absolute(self) -> Path:
        """ Returns the absolute path """
        return self.path.absolute()

    @property
    def is_file(self) -> bool:
        """ Checks if path is a file """
        return self.path.is_file()

    @property
    def is_dir(self) -> bool:
        """ Checks if path is a directory """
        return self.path.is_dir()

    @property
    def suffix(self) -> str:
        """ Returns the file extension """
        return self.path.suffix

    def __str__(self) -> str:
        return str(self.path)

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(path='{self.path}')"