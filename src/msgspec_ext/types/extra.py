import re
from typing import Any
from datetime import datetime
from uuid import UUID
from msgspec import ValidationError


__all__ = ["DateStr", "UUIDStr"]


class DateStr:
    """A type for date strings in ISO format (YYYY-MM-DD)."""
    
    date_pattern = re.compile(r'^\d{4}-\d{2}-\d{2}$')

    def __init__(self, date: str):
        self.date = date

    @classmethod
    def validate(cls, value: Any) -> "DateStr":
        if not isinstance(value, str):
            raise ValidationError(f"Date must be a string, got {type(value).__name__}")
            
        if not cls.date_pattern.match(value):
            raise ValidationError("Invalid date format. Use YYYY-MM-DD")
            
        try:
            datetime.strptime(value, '%Y-%m-%d')
        except ValueError as e:
            raise ValidationError(f"Invalid date: {str(e)}")
            
        return cls(value)

    def __str__(self) -> str:
        return self.date

class UUIDStr:
    """A type for UUID strings."""

    def __init__(self, uuid: str):
        self.uuid = uuid

    @classmethod
    def validate(cls, value: Any) -> "UUIDStr":
        if not isinstance(value, str):
            raise ValidationError(f"UUID must be a string, got {type(value).__name__}")
            
        try:
            UUID(value)
        except ValueError as e:
            raise ValidationError(f"Invalid UUID format: {str(e)}")
            
        return cls(value)

    def __str__(self) -> str:
        return self.uuid
