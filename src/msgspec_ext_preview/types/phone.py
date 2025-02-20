import re
from typing import Any
from msgspec import ValidationError


__all__ = ["PhoneNumber"]


class PhoneNumber:
    """A type for phone numbers in E.164 format."""
    
    phone_pattern = re.compile(r'^\+?[1-9]\d{1,14}$')

    def __init__(self, number: str):
        self.number = number

    @classmethod
    def validate(cls, value: Any) -> "PhoneNumber":
        if not isinstance(value, str):
            raise ValidationError(f"Phone number must be a string, got {type(value).__name__}")
            
        clean_number = re.sub(r"[\s\-\(\)]", "", value)
            
        if not cls.phone_pattern.match(clean_number):
            raise ValidationError("Invalid phone number format. Use E.164 format: +[country][number]")
            
        return cls(clean_number)

    def __str__(self) -> str:
        return self.number