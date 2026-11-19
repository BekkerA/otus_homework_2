from model.contact import Contact
from model.storage import JsonStorage
from exceptions import ContactNotFoundError, PhoneBookStorageError


class PhoneBook:
    """Класс телефонного справочника (бизнес-логика)."""

    def __init__(self, storage: JsonStorage):
        self._storage = storage
        self._contacts: dict[int, Contact] = {}
        self._max_id: int = 0
        self._load()

    def _load(self) -> None:
        try:
            data = self._storage.load()
        except PhoneBookStorageError:
            data = {"contacts": {}, "max_id": 0}
        self._max_id = data["max_id"]
        self._contacts = {
            int(cid): Contact.from_dict(int(cid), cdata)
            for cid, cdata in data["contacts"].items()
        }

    def save(self) -> None:
        data = {
            "contacts": {
                str(cid): contact.to_dict()
                for cid, contact in self._contacts.items()
            },
            "max_id": self._max_id,
        }
        self._storage.save(data)

    # --- CRUD ---
    def all_contacts(self) -> list[Contact]:
        return list(self._contacts.values())

    def add(self, name: str, phone: str) -> Contact:
        contact = Contact(id=0, name=name, phone=phone)  # валидация
        self._max_id += 1
        contact = Contact(id=self._max_id, name=name, phone=phone)
        self._contacts[contact.id] = contact
        return contact

    def get(self, contact_id: int) -> Contact:
        if contact_id not in self._contacts:
            raise ContactNotFoundError(
                f"Контакт с id={contact_id} не найден."
            )
        return self._contacts[contact_id]

    def update(self, contact_id: int, name: str, phone: str) -> Contact:
        self.get(contact_id)  # бросит, если нет
        contact = Contact(id=contact_id, name=name, phone=phone)
        self._contacts[contact_id] = contact
        return contact

    def delete(self, contact_id: int) -> Contact:
        contact = self.get(contact_id)
        del self._contacts[contact_id]
        return contact

    def search(self, query: str) -> list[Contact]:
        query = str(query)
        result = []
        for contact in self._contacts.values():
            if (
                query in str(contact.id)
                or query in contact.name
                or query in contact.phone
            ):
                result.append(contact)
        return result