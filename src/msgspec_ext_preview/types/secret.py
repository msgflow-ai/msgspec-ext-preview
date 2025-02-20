from typing import Any, Union, ClassVar
from msgspec import ValidationError


__all__ = ["SecretStr", "SecretBytes"]


class _Secret:
    """Base class for secret types that hide their values."""
    
    def __str__(self) -> str:
        return "**********"

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}('**********')"

    def get_secret_value(self) -> Union[str, bytes]:
        return self.secret

class SecretStr(_Secret):
    """A type for sensitive strings (such as passwords)."""

    min_length: ClassVar[int] = 1
    max_length: ClassVar[int] = 4096

    def __init__(self, secret: str):
        self.secret = secret

    @classmethod
    def validate(cls, value: Any) -> "SecretStr":
        if not isinstance(value, str):
            raise ValidationError(f"Secret must be a string, got {type(value).__name__}")
            
        if len(value) < cls.min_length:
            raise ValidationError(f"Secret must be at least {cls.min_length} character long")
            
        if len(value) > cls.max_length:
            raise ValidationError(f"Secret length exceeds maximum of {cls.max_length} characters")
            
        return cls(value)

class SecretBytes(_Secret):
    """A type for sensitive binary data."""

    max_length: ClassVar[int] = 1024 * 1024  # 1MB

    def __init__(self, secret: bytes):
        self.secret = secret

    @classmethod
    def validate(cls, value: Any) -> "SecretBytes":
        if not isinstance(value, bytes):
            raise ValidationError(f"Secret must be bytes, got {type(value).__name__}")
            
        if len(value) > cls.max_length:
            raise ValidationError(f"Secret length exceeds maximum of {cls.max_length} bytes")
            
        return cls(value)