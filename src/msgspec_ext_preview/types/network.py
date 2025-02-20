import re
import ipaddress
from typing import Any, Optional, ClassVar
from msgspec import ValidationError


__all__ = [
    "AnyUrl", 
    "HttpUrl", 
    "PostgresDsn", 
    "RedisDsn", 
    "AmqpDsn", 
    "EmailStr",
    "IPvAnyAddress",
    "IPv4Address",
    "IPv6Address",
    "IPvAnyInterface",
    "IPvAnyNetwork",
    "MacAddress"
]


class AnyUrl:
    """A generic type for URLs.
    
    Validates whether the string is a valid URL with proper format and components.
    
    Attributes:
        url: The validated URL string
        allowed_schemes: List of allowed URL schemes (protocols)
        max_length: Maximum allowed length for the URL
    """
    
    allowed_schemes: ClassVar[tuple[str, ...]] = ("http", "https", "ftp", "postgres", "postgresql", 
                                                 "redis", "amqp", "mongodb", "kafka")
    max_length: ClassVar[int] = 2083  # Maximum URL length commonly supported by browsers
    
    # More comprehensive URL pattern that validates components
    url_pattern = re.compile(
        r"^"
        r"(?P<scheme>[a-z][a-z0-9+.-]*)?://"  # scheme (optional)
        r"(?P<auth>[^/@]*@)?"  # authentication (optional)
        r"(?P<host>[^/:]+)"  # host (required)
        r"(?P<port>:[0-9]+)?"  # port (optional)
        r"(?P<path>/[^?#]*)?"  # path (optional)
        r"(?P<query>\?[^#]*)?"  # query (optional)
        r"(?P<fragment>#.*)?"  # fragment (optional)
        r"$"
    )

    def __init__(self, url: str):
        self.url = url

    @classmethod
    def validate(cls, value: Any) -> "AnyUrl":
        """Validate and create a URL instance.
        
        Args:
            value: The URL string to validate
            
        Returns:
            An instance of the URL class
            
        Raises:
            ValidationError: If the URL is invalid
        """
        if not isinstance(value, str):
            raise ValidationError(f"URL must be a string, got {type(value).__name__}")
        
        if not value:
            raise ValidationError("URL cannot be empty")
            
        if len(value) > cls.max_length:
            raise ValidationError(f"URL length exceeds maximum of {cls.max_length} characters")

        match = cls.url_pattern.match(value)
        if not match:
            raise ValidationError("Invalid URL format")
            
        parts = match.groupdict()
        scheme = parts["scheme"]
        
        if scheme and scheme not in cls.allowed_schemes:
            raise ValidationError(f"Invalid URL scheme. Allowed schemes: {', '.join(cls.allowed_schemes)}")
            
        host = parts["host"]
        if not host:
            raise ValidationError("URL must contain a host")
            
        # Validate port if present
        port = parts["port"]
        if port:
            try:
                port_num = int(port[1:])  # Remove the leading ":"
                if not 1 <= port_num <= 65535:
                    raise ValueError
            except ValueError:
                raise ValidationError("Invalid port number")

        return cls(value)

    def __str__(self) -> str:
        return self.url
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(url='{self.url}')"

class HttpUrl(AnyUrl):
    """A type specific to HTTP/HTTPS URLs."""
    
    allowed_schemes = ("http", "https")

    @classmethod
    def validate(cls, value: Any) -> "HttpUrl":
        url = super().validate(value)
        scheme = cls.url_pattern.match(value).group("scheme")
        if scheme not in cls.allowed_schemes:
            raise ValidationError("URL must use http or https scheme")
        return cls(url.url)

class PostgresDsn(AnyUrl):
    """A type for PostgreSQL connection URLs."""
    
    allowed_schemes = ("postgres", "postgresql")

    @classmethod
    def validate(cls, value: Any) -> "PostgresDsn":
        url = super().validate(value)
        scheme = cls.url_pattern.match(value).group("scheme")
        if scheme not in cls.allowed_schemes:
            raise ValidationError("URL must use postgres or postgresql scheme")
        return cls(url.url)

class RedisDsn(AnyUrl):
    """A type for Redis connection URLs."""
    
    allowed_schemes = ("redis",)

    @classmethod
    def validate(cls, value: Any) -> "RedisDsn":
        url = super().validate(value)
        scheme = cls.url_pattern.match(value).group("scheme")
        if scheme not in cls.allowed_schemes:
            raise ValidationError("URL must use redis scheme")
        return cls(url.url)

class AmqpDsn(AnyUrl):
    """A type for AMQP connection URLs."""
    
    allowed_schemes = ("amqp",)

    @classmethod
    def validate(cls, value: Any) -> "AmqpDsn":
        url = super().validate(value)
        scheme = cls.url_pattern.match(value).group("scheme")
        if scheme not in cls.allowed_schemes:
            raise ValidationError("URL must use amqp scheme")
        return cls(url.url)

class MongoDsn(AnyUrl):
    """A type for MongoDB connection URLs."""
    
    allowed_schemes = ("mongodb",)

    @classmethod
    def validate(cls, value: Any) -> "MongoDsn":
        url = super().validate(value)
        scheme = cls.url_pattern.match(value).group("scheme")
        if scheme not in cls.allowed_schemes:
            raise ValidationError("URL must use mongodb scheme")
        return cls(url.url)

class KafkaDns(AnyUrl):
    """A type for Kafka connection URLs."""
    
    allowed_schemes = ("kafka",)

    @classmethod
    def validate(cls, value: Any) -> "KafkaDns":
        url = super().validate(value)
        scheme = cls.url_pattern.match(value).group("scheme")
        if scheme not in cls.allowed_schemes:
            raise ValidationError("URL must use kafka scheme")
        return cls(url.url)
    
class EmailStr:
    """A type for email addresses.
    
    Validates whether the string is a valid email address following RFC 5322 standards.
    """
    
    email_pattern = re.compile(r'''(?:[a-z0-9!#$%&'*+/=?^_`{|}~-]+(?:\.[a-z0-9!#$%&'*+/=?^_`{|}~-]+)*|"(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21\x23-\x5b\x5d-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])*")@(?:(?:[a-z0-9](?:[a-z0-9-]*[a-z0-9])?\.)+[a-z0-9](?:[a-z0-9-]*[a-z0-9])?|\[(?:(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9]))\.){3}(?:(2(5[0-5]|[0-4][0-9])|1[0-9][0-9]|[1-9]?[0-9])|[a-z0-9-]*[a-z0-9]:(?:[\x01-\x08\x0b\x0c\x0e-\x1f\x21-\x5a\x53-\x7f]|\\[\x01-\x09\x0b\x0c\x0e-\x7f])+)\])''', re.IGNORECASE)
    max_length: ClassVar[int] = 254  # RFC 5321

    def __init__(self, email: str):
        self.email = email

    @classmethod
    def validate(cls, value: Any) -> "EmailStr":
        if not isinstance(value, str):
            raise ValidationError(f"Email must be a string, got {type(value).__name__}")
        
        if not value:
            raise ValidationError("Email cannot be empty")
            
        if len(value) > cls.max_length:
            raise ValidationError(f"Email length exceeds maximum of {cls.max_length} characters")

        if not cls.email_pattern.match(value):
            raise ValidationError("Invalid email format")
            
        _, domain = value.rsplit("@", 1)
        if not 1 < len(domain) <= 255:
            raise ValidationError("Invalid domain length")
            
        return cls(value)

    def __str__(self) -> str:
        return self.email
        
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(email='{self.email}')"

class IPvAnyAddress:
    """A type for IP addresses (IPv4 or IPv6)."""

    def __init__(self, ip: str, version: Optional[int] = None):
        self.ip = ip
        self.version = version
        self._ip_address = ipaddress.ip_address(ip)

    @classmethod
    def validate(cls, value: Any, version: Optional[int] = None) -> "IPvAnyAddress":
        if not isinstance(value, str):
            raise ValidationError(f"IP address must be a string, got {type(value).__name__}")
            
        try:
            ip = ipaddress.ip_address(value)
            if version and ip.version != version:
                raise ValidationError(f"IP address must be version {version}")
            return cls(value, version=ip.version)
        except ValueError as e:
            raise ValidationError(f"Invalid IP address: {str(e)}")

    def is_private(self) -> bool:
        return self._ip_address.is_private

    def is_global(self) -> bool:
        return self._ip_address.is_global

    def is_multicast(self) -> bool:
        return self._ip_address.is_multicast

    def __str__(self) -> str:
        return self.ip
        
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(ip='{self.ip}', version={self.version})"

class IPv4Address(IPvAnyAddress):
    """A type specifically for IPv4 addresses."""

    @classmethod
    def validate(cls, value: Any) -> "IPv4Address":
        return super().validate(value, version=4)

class IPv6Address(IPvAnyAddress):
    """A type specifically for IPv6 addresses."""

    @classmethod
    def validate(cls, value: Any) -> "IPv6Address":
        return super().validate(value, version=6)

class IPvAnyInterface:
    """A type for network interfaces (IP address with mask)."""

    def __init__(self, interface: str, version: Optional[int] = None):
        self.interface = interface
        self.version = version
        self._ip_interface = ipaddress.ip_interface(interface)

    @classmethod
    def validate(cls, value: Any, version: Optional[int] = None) -> "IPvAnyInterface":
        if not isinstance(value, str):
            raise ValidationError(f"Network interface must be a string, got {type(value).__name__}")
            
        try:
            interface = ipaddress.ip_interface(value)
            if version and interface.version != version:
                raise ValidationError(f"Network interface must be version {version}")
            return cls(value, version=interface.version)
        except ValueError as e:
            raise ValidationError(f"Invalid network interface: {str(e)}")

    def get_network(self) -> "IPvAnyNetwork":
        return IPvAnyNetwork(str(self._ip_interface.network))

    def get_ip(self) -> IPvAnyAddress:
        return IPvAnyAddress(str(self._ip_interface.ip))

    def __str__(self) -> str:
        return self.interface
        
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(interface='{self.interface}', version={self.version})"

class IPvAnyNetwork:
    """A type for IP networks (IP address with netmask)."""

    def __init__(self, network: str, version: Optional[int] = None):
        self.network = network
        self.version = version
        self._ip_network = ipaddress.ip_network(network)

    @classmethod
    def validate(cls, value: Any, version: Optional[int] = None) -> "IPvAnyNetwork":
        if not isinstance(value, str):
            raise ValidationError(f"Network must be a string, got {type(value).__name__}")
            
        try:
            network = ipaddress.ip_network(value)
            if version and network.version != version:
                raise ValidationError(f"Network must be version {version}")
            return cls(value, version=network.version)
        except ValueError as e:
            raise ValidationError(f"Invalid network: {str(e)}")

    def get_broadcast(self) -> Optional[IPvAnyAddress]:
        broadcast = self._ip_network.broadcast_address
        return IPvAnyAddress(str(broadcast)) if broadcast else None

    def get_netmask(self) -> IPvAnyAddress:
        return IPvAnyAddress(str(self._ip_network.netmask))

    def __str__(self) -> str:
        return self.network
        
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(network='{self.network}', version={self.version})"

class MacAddress:
    """A type for MAC addresses with validation."""

    MAC_PATTERNS = {
        "canonical": re.compile(r"^([0-9A-Fa-f]{2}[:-]){5}([0-9A-Fa-f]{2})$"),
        "cisco": re.compile(r"^([0-9A-Fa-f]{4}\.){2}([0-9A-Fa-f]{4})$"),
        "bare": re.compile(r"^[0-9A-Fa-f]{12}$")
    }

    def __init__(self, address: str):
        self.address = address
        self._normalized = self._normalize(address)

    @classmethod
    def validate(cls, value: Any) -> "MacAddress":
        """
        Validates a MAC address.
        
        Accepts formats:
        - XX:XX:XX:XX:XX:XX
        - XX-XX-XX-XX-XX-XX
        - XXXX.XXXX.XXXX
        - XXXXXXXXXXXX
        
        where X is a hexadecimal digit
        """
        if not isinstance(value, str):
            raise ValidationError(f"MAC address must be a string, got {type(value).__name__}")

        # Check if it matches any known format
        if not any(pattern.match(value) for pattern in cls.MAC_PATTERNS.values()):
            raise ValidationError(
                "Invalid MAC address format. Use XX:XX:XX:XX:XX:XX, "
                "XX-XX-XX-XX-XX-XX, XXXX.XXXX.XXXX or XXXXXXXXXXXX"
            )

        return cls(value)

    @staticmethod
    def _normalize(address: str) -> str:
        """ Normalizes MAC address to canonical format (XX:XX:XX:XX:XX:XX) """
        # Remove separators
        clean = re.sub(r"[.:-]", "", address)
        
        # Insert : each two new characters
        return ":".join(clean[i:i+2] for i in range(0, 12, 2))

    @property
    def canonical(self) -> str:
        """ Returns the address in canonical format (XX:XX:XX:XX:XX:XX) """
        return self._normalized

    @property
    def cisco(self) -> str:
        """ Returns the address in Cisco format (XXXX.XXXX.XXXX) """
        clean = re.sub(r"[.:-]", "", self.address)
        return ".".join(clean[i:i+4] for i in range(0, 12, 4))

    @property
    def bare(self) -> str:
        """ Returns the address without separators (XXXXXXXXXXXX) """
        return re.sub(r'[.:-]', '', self.address)

    def is_unicast(self) -> bool:
        """ Checks if it is a unicast address (least significant bit of the first byte is 0) """
        first_byte = int(self.bare[:2], 16)
        return first_byte & 0x01 == 0

    def is_multicast(self) -> bool:
        """ Checks if it is a multicast address (least significant bit of the first byte is 1) """
        return not self.is_unicast()

    def __str__(self) -> str:
        return self.canonical

    def __repr__(self) -> str:
        return f"{self.__class__.__name__}(address='{self.canonical}')"