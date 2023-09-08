import re
from .Field import Field

class PhoneField(Field):    
    @Field.value.setter
    def value(self, phone):
        if re.search('(\+38)?\(?0\d{2}\)?\d{7}$', phone):
            self._value = phone
