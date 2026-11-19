from model.storage import JsonStorage
from model.phone_book import PhoneBook
from view.console_view import ConsoleView
from controller.phone_book_controller import PhoneBookController


def main() -> None:
    storage = JsonStorage()
    model = PhoneBook(storage)
    view = ConsoleView()
    controller = PhoneBookController(model, view)
    controller.run()


if __name__ == "__main__":
    main()