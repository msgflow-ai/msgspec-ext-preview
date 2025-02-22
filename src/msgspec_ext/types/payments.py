import re
from enum import Enum
from typing import Any
from msgspec import ValidationError


__all__ = ["PaymentCardBrand", "PaymentCardNumber"]


class PaymentCardBrand(str, Enum):
    """Enum for credit card brands"""
    visa = "visa"
    mastercard = "mastercard"
    amex = "amex"
    discover = "discover"
    diners = "diners"
    jcb = "jcb"
    unionpay = "unionpay"
    maestro = "maestro"

class PaymentCardNumber:
    """A type for payment card numbers with validation and brand detection."""

    CARD_PATTERNS = {
        PaymentCardBrand.visa: r"^4[0-9]{12}(?:[0-9]{3})?$",
        PaymentCardBrand.mastercard: r"^5[1-5][0-9]{14}$",
        PaymentCardBrand.amex: r"^3[47][0-9]{13}$",
        PaymentCardBrand.discover: r"^6(?:011|5[0-9]{2})[0-9]{12}$",
        PaymentCardBrand.diners: r"^3(?:0[0-5]|[68][0-9])[0-9]{11}$",
        PaymentCardBrand.jcb: r"^(?:2131|1800|35\d{3})\d{11}$",
        PaymentCardBrand.unionpay: r"^62[0-9]{14,17}$",
        PaymentCardBrand.maestro: r"^(?:5[0678]\d\d|6304|6390|67\d\d)\d{8,15}$"
    }

    def __init__(self, number: str):
        self.number = number
        self._brand = self._detect_brand()

    @classmethod
    def validate(cls, value: Any) -> "PaymentCardNumber":
        if not isinstance(value, str):
            raise ValidationError(f"Card number must be a string, got {type(value).__name__}")
        
        clean_number = re.sub(r"[\s-]", "", value)
        
        if not clean_number.isdigit():
            raise ValidationError("Card number must contain only digits")
        
        if not cls._is_valid_length(clean_number):
            raise ValidationError("Invalid card number length")
            
        if not cls._luhn_check(clean_number):
            raise ValidationError("Invalid card number (Luhn check failed)")
            
        if not any(re.match(pattern, clean_number) for pattern in cls.CARD_PATTERNS.values()):
            raise ValidationError("Unknown card brand or invalid number format")
            
        return cls(clean_number)

    @staticmethod
    def _is_valid_length(number: str) -> bool:
        """ Checks if the number length is between 13 and 19 digits """
        return 13 <= len(number) <= 19

    @staticmethod
    def _luhn_check(number: str) -> bool:
        """ Implements the Luhn algorithm for card number validation """
        digits = [int(d) for d in number]
        odd_digits = digits[-1::-2]
        even_digits = digits[-2::-2]
        checksum = sum(odd_digits)
        for d in even_digits:
            checksum += sum(divmod(d * 2, 10))
        return checksum % 10 == 0

    def _detect_brand(self) -> PaymentCardBrand:
        """ Detects card brand based on number """
        for brand, pattern in self.CARD_PATTERNS.items():
            if re.match(pattern, self.number):
                return brand
        return None

    @property
    def brand(self) -> PaymentCardBrand:
        """ Returns the card flag """
        return self._brand

    @property
    def bin(self) -> str:
        """ Returns the first 6 digits of the card (BIN) """
        return self.number[:6]

    @property
    def last4(self) -> str:
        """ Returns the last 4 digits of the card """
        return self.number[-4:]

    @property
    def masked(self) -> str:
        """ Returns the masked card number """
        return f"{self.bin}{'*' * (len(self.number) - 10)}{self.last4}"

    def __str__(self) -> str:
        return self.masked

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(number='{self.masked}')"