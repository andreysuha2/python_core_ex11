from typing import Optional
from datetime import datetime
from app.Fields import NameField, PhoneField, BirthdayField
from app.address_utils import find_index

class Record:
    def __init__(self, name: NameField, phones: list[PhoneField] = [], birthday: BirthdayField = None) -> None:
        self.name = name
        self.phones = phones
        self.birthday = birthday

    def __repr__(self) -> str:
        return f"{self.name.value}: {'|'.join([ phone.value for phone in self.phones ])}"

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
        if not self.has_phone(phone.value):
            self.phones.append(phone)
            return True
        return False

    def remove_phone(self, searching_phone: str) -> None:
        index = self.get_phone_index(searching_phone)
        if index != -1:
            self.phones.pop(index)
            return f'Phone "{searching_phone}" was removed from contact "{self.name}"!'
        return f'Phone "{searching_phone}" doen\'t exist for contact {self.name}'

    def update_phone(self, searching_phone: PhoneField, phone_number: PhoneField) -> None:
        if self.has_phone(phone_number):
            return f'Phone {searching_phone} already exists for this record'
        index = self.get_phone_index(searching_phone.value)
        if index != -1:
            self.phones[index] = phone_number
            return f'Phone "{searching_phone}" was changed to {phone_number} for contact "{self.name}"!'
        return f'Phone "{phone_number}" doen\'t exist for contact {self.name}'