from pathlib import Path
import json
from exceptions import PhoneBookStorageError

class JsonStorage:
    """Класс чтения/записи справочника в JSON-файл."""

    def __init__(self, file_path: Path | None = None):
        if file_path is None:
            base_dir = Path(__file__).resolve().parent.parent
            file_path = base_dir / "phone_book.json"
        self.file_path = file_path

    def load(self) -> dict:
        """Читает JSON. Если файла нет или он битый — возвращает пустую структуру."""
        empty = {"contacts": {}, "max_id": 0}
        if not self.file_path.exists():
            return empty
        try:
            data = json.loads(self.file_path.read_text(encoding="utf-8"))
        except (json.JSONDecodeError, OSError) as exc:
            raise PhoneBookStorageError(
                f"Ошибка чтения файла справочника: {exc}"
            ) from exc

        if not isinstance(data, dict):
            raise PhoneBookStorageError("Файл справочника повреждён.")

        contacts = data.get("contacts", {})
        if not isinstance(contacts, dict):
            contacts = {}

        max_id = data.get("max_id", 0)
        if contacts:
            max_in_file = max(int(k) for k in contacts.keys())
            max_id = max(max_id, max_in_file)

        return {"contacts": contacts, "max_id": max_id}

    def save(self, data: dict) -> None:
        try:
            self.file_path.write_text(
                json.dumps(data, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
        except OSError as exc:
            raise PhoneBookStorageError(
                f"Ошибка записи файла справочника: {exc}"
            ) from exc