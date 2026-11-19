from dataclasses import dataclass
from otus_homework_2.exceptions import InvalidPhoneError, InvalidNameError
import re


@dataclass
class Contact:
    """Модель контакта."""
    id: int
    name: str
    phone: str

    PHONE_PATTERN = re.compile(r'^\+*\d+$')
    MIN_PHONE_LENGTH = 4

    def __post_init__(self):
        self.validate_name(self.name)
        self.validate_phone(self.phone)

    @staticmethod
    def validate_name(name: str) -> str:
        if not name or not name.strip():
            raise InvalidNameError("Имя контакта не может быть пустым.")
        return name.strip()

    @classmethod
    def validate_phone(cls, phone: str) -> str:
        """Проверка корректности телефона."""
        if len(phone) < cls.MIN_PHONE_LENGTH:
            raise InvalidPhoneError(
                "Длина телефона должна быть не менее 4 символов."
            )
        if not cls.PHONE_PATTERN.fullmatch(phone):
            raise InvalidPhoneError(
                "Телефон может содержать только цифры и '+' в начале."
            )
        return phone

    def to_dict(self) -> dict:
        return {"name": self.name, "phone": self.phone}

    @classmethod
    def from_dict(cls, contact_id: int, data: dict) -> "Contact":
        return cls(id=contact_id, name=data["name"], phone=data["phone"])

    def __str__(self) -> str:
        return f"id={self.id} имя={self.name} телефон={self.phone}"