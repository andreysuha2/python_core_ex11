from typing import Optional
from datetime import datetime
from app.Fields import NameField, PhoneField, BirthdayField
from app.address_utils import find_index

class Record:
    def __init__(self, name: NameField, phones: list[PhoneField] = [], birthday: BirthdayField = None) -> None:
        self.name = name
        self.phones = phones
        self.birthday = birthday

    def days_to_birthday(self) -> Optional[int]:
        if not self.birthday:
            return None
        now = datetime.now()
        def get_diff(year):
            birthday = datetime(year, self.birthday.in_datetime.month, self.birthday.in_datetime.day)
            dif = birthday - now
            return dif.days if dif.days >= 0 else get_diff(year + 1)
        return get_diff(now.year)

    def get_phone_index(self, searching_phone) -> int:
        return find_index(lambda phone: phone.value == searching_phone, self.phones)

    def has_phone(self, searching_phone: str) -> bool:
        index = self.get_phone_index(searching_phone)
        return index != -1

    def add_phone(self, phone: PhoneField) -> None:
        if not phone.value:
            return 0
        if not self.has_phone(phone.value):
            self.phones.append(phone)
            return 1
        return 2

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