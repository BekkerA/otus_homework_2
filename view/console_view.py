from model.contact import Contact


class ConsoleView:
    """Слой представления: ввод/вывод в консоль."""

    MAIN_MENU = [
        "показать все контакты",
        "создать контакт",
        "найти контакт",
        "изменить контакт",
        "удалить контакт",
        "для выхода из программы",
    ]

    def show_main_menu(self) -> str:
        text = f"Введите число от 1 до {len(self.MAIN_MENU)}:\n"
        for i, item in enumerate(self.MAIN_MENU, start=1):
            text += f"{i} - {item}\n"
        return input(text)

    def show_contacts(self, contacts: list[Contact]) -> None:
        print(f"Всего контактов = {len(contacts)}")
        for i, contact in enumerate(contacts, start=1):
            print(f"Контакт {i} : {contact}")

    def show_contact(self, contact: Contact) -> None:
        print(contact)

    def show_message(self, message: str) -> None:
        print(message)

    def show_error(self, message: str) -> None:
        print(f"Ошибка: {message}")

    def ask_name(self) -> str:
        return input("Введите имя контакта: ")

    def ask_phone(self) -> str:
        return input(
            """
        Введите номер телефона (телефон может содержать цифры,
        телефон может начинаться со знака '+',
        длина телефона должна быть не менее 4 символов,
        для выхода в главное меню введите #:
        """
        )

    def ask_id(self) -> str:
        return input("Введите id контакта: ")

    def ask_search(self) -> str:
        return input(
            """
        Введите текст для поиска по телефонному справочнику.
        Для выхода в главное меню введите #
        """
        )

    def ask_confirm_delete(self) -> str:
        return input("Для подтверждения удаления контакта введите 1: ")