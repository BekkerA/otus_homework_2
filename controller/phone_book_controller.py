from model.phone_book import PhoneBook
from model.storage import JsonStorage
from view.console_view import ConsoleView
from exceptions import PhoneBookError, InvalidPhoneError, InvalidNameError

EXIT_MARKER = "#"


class PhoneBookController:
    """Контроллер: связывает модель и представление."""

    def __init__(self, model: PhoneBook, view: ConsoleView):
        self.model = model
        self.view = view

    def run(self) -> None:
        while True:
            choice = self.view.show_main_menu()
            try:
                if choice == "1":
                    self._show_all()
                elif choice == "2":
                    self._add()
                elif choice == "3":
                    self._search()
                elif choice == "4":
                    self._edit()
                elif choice == "5":
                    self._delete()
                elif choice in ("6", "exit"):
                    return
            except PhoneBookError as exc:
                self.view.show_error(str(exc))

    # --- операции ---
    def _show_all(self) -> None:
        self.view.show_contacts(self.model.all_contacts())

    def _add(self) -> None:
        name = self.view.ask_name()
        phone = self._read_phone()
        if phone is None:
            self.view.show_message("Контакт не добавлен")
            return
        contact = self.model.add(name, phone)
        self.model.save()
        self.view.show_message("Контакт добавлен:")
        self.view.show_contact(contact)

    def _search(self) -> None:
        query = self.view.ask_search()
        if query == EXIT_MARKER:
            return
        found = self.model.search(query)
        self.view.show_contacts(found)

    def _edit(self) -> None:
        raw_id = self.view.ask_id()
        try:
            contact_id = int(raw_id)
        except ValueError:
            self.view.show_error("id должен быть числом.")
            return

        contact = self.model.get(contact_id)
        self.view.show_message("Контакт найден:")
        self.view.show_contact(contact)

        new_name = input(
            "Введите новое имя контакта или # для выхода без изменения: "
        )
        if new_name == EXIT_MARKER:
            return

        phone = self._read_phone()
        if phone is None:
            return

        updated = self.model.update(contact_id, new_name, phone)
        self.model.save()
        self.view.show_message("Контакт изменён:")
        self.view.show_contact(updated)

    def _delete(self) -> None:
        raw_id = self.view.ask_id()
        try:
            contact_id = int(raw_id)
        except ValueError:
            self.view.show_error("id должен быть числом.")
            return

        contact = self.model.get(contact_id)
        self.view.show_message("Контакт найден:")
        self.view.show_contact(contact)

        if self.view.ask_confirm_delete() == "1":
            self.model.delete(contact_id)
            self.model.save()
            self.view.show_message("Контакт удалён.")
        else:
            self.view.show_message("Удаление отменено.")

    # --- вспомогательные ---
    def _read_phone(self) -> str | None:
        while True:
            phone = self.view.ask_phone()
            if phone == EXIT_MARKER:
                return None
            try:
                return self.model.constructor_validate_phone(phone)
            except InvalidPhoneError as exc:
                self.view.show_error(str(exc))