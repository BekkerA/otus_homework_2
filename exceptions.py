class PhoneBookError(Exception):
    """Базовое исключение приложения."""
    pass


class PhoneBookStorageError(PhoneBookError):
    """Ошибка чтения/записи файла справочника."""
    pass


class InvalidPhoneError(PhoneBookError):
    """Некорректный номер телефона."""
    pass


class ContactNotFoundError(PhoneBookError):
    """Контакт с указанным id не найден."""
    pass


class InvalidNameError(PhoneBookError):
    """Некорректное имя контакта."""
    pass