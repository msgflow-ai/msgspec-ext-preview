from typing import List
from src.msgspec_ext_preview import *


http_url = HttpUrl.validate("https://example.com:8080/path?query=1#fragment")
postgres_url = PostgresDsn.validate("postgresql://user:pass@localhost:5432/db")
redis_url = RedisDsn.validate("redis://localhost:6379/0")


# Email
email = EmailStr.validate("user@example.com")

# IPs
ipv4 = IPv4Address.validate("192.168.1.1")
ipv6 = IPv6Address.validate("2001:db8::1")

# Network
network = IPvAnyNetwork.validate("192.168.1.0/24")
print(network.get_broadcast())  # 192.168.1.255

# Secrets
password = SecretStr.validate("mysecret")
print(password)  # **********
print(password.get_secret_value())  # mysecret

date = DateStr.validate("2024-01-18")

uuid = UUIDStr.validate("123e4567-e89b-12d3-a456-426614174000")

phone = PhoneNumber.validate("+5511999999999")    


card = PaymentCardNumber.validate("4111111111111111")
print(card.brand)  # PaymentCardBrand.visa
print(card.masked)  # 411111******1111
print(card.bin)    # 411111
print(card.last4)  # 1111

file_path = FilePath.validate("/path/to/file.txt", check_exists=False)
print(file_path.suffix)  # .txt
print(file_path.is_file)  # False
print(file_path.absolute)  # /absolute/path/to/file.txt

mac = MacAddress.validate("00:11:22:33:44:55")
print(mac.canonical)  # 00:11:22:33:44:55
print(mac.cisco)     # 0011.2233.4455
print(mac.bare)      # 001122334455
print(mac.is_unicast())  # True


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_",
        case_sensitive=False
    )
    
    debug: bool
    secret_key: SecretStr
    allowed_hosts: List[str]
    database_url: str
    redis_url: RedisDsn
    mongo_url: str
    kafka_url: str
    email_admin: str
    email_support: str
    server_ip: str
    network_interface: str
    network_address: str
    api_key: str
    db_password: str
    amqp_url: str
    cache_ttl: int
    log_level: str

# Carrega as configurações
settings = AppSettings()

# Exibe os valores carregados
print("Debug:", settings.debug)
print("Secret Key:", settings.secret_key)
print("Allowed Hosts:", settings.allowed_hosts)
print("Database URL:", settings.database_url)
print("Redis URL:", settings.redis_url)
print("Mongo URL:", settings.mongo_url)
print("Kafka URL:", settings.kafka_url)
print("Email Admin:", settings.email_admin)
print("Email Support:", settings.email_support)
print("Server IP:", settings.server_ip)
print("Network Interface:", settings.network_interface)
print("Network Address:", settings.network_address)
print("API Key:", settings.api_key)
print("DB Password:", settings.db_password)
print("AMQP URL:", settings.amqp_url)
print("Cache TTL:", settings.cache_ttl)
print("Log Level:", settings.log_level)


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_prefix="APP_"
    )
    
    database_url: PostgresDsn
    redis_url: RedisDsn
    email: EmailStr
    secret_key: SecretStr

settings = AppSettings()

print(settings.database_url)  # postgres://user:password@localhost:5432/dbname
print(settings.secret_key)    # ********