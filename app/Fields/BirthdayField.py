from datetime import datetime
from .Field import Field

class BirthdayField(Field):
    birthday_format = '%d-%m-%Y'

    @Field.value.setter
    def value(self, val):
        if val:
            try:
                now = datetime.now()
                bday = datetime.strptime(val, BirthdayField.birthday_format)
                if (now - bday).days > 0:
                    self._value = val
            except ValueError:
                pass
    
    @property
    def in_datetime(self):
        return datetime.strptime(self.value, BirthdayField.birthday_format) if self.value else None