from app.Fields import NameField, PhoneField
from app.address_utils import find_index

class Record:
    def __init__(self, name: NameField, phones: list[PhoneField] = [] ) -> None:
        self.name = name
        self.phones = phones

    def get_phone_index(self, searching_phone) -> int:
        return find_index(lambda phone: phone.value == searching_phone, self.phones)

    def has_phone(self, searching_phone: str) -> bool:
        index = self.get_phone_index(searching_phone)
        return index != -1

    def add_phone(self, phone: PhoneField) -> None:
        if (not self.has_phone(phone.value)):
            self.phones.append(phone)
            return True
        return False

    def remove_phone(self, searching_phone: str) -> None:
        index = self.get_phone_index(searching_phone)
        if index != -1:
            self.phones.pop(index)
            return 0
        return 1

    def update_phone(self, searching_phone: str, phone_number: str) -> None:
        if self.has_phone(phone_number):
            return 0
        index = self.get_phone_index(searching_phone)
        if index != -1:
            self.phones[index].value = phone_number
            return 1
        return 2