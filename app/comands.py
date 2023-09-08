from app.AddressBook import AddressBook
from app.Fields import NameField, PhoneField
from app.Record import Record

ADDRESS_BOOK = AddressBook()

def input_error(handler):
    def inner(args):
        try:
            result = handler(*args)
            return result
        except KeyError:
            return f"Contact {args[0]} doesn't exist!"
        except ValueError:
            return "You are trying to set invalid value"
        except IndexError:
            return "You are sending invalid count of parameters. Please use help comand for hint"
    return inner

@input_error
def add_contact(*args):
    name, phones = args[0], args[1:]
    if name in ADDRESS_BOOK:
        return f'Contact with name "{name}" already exists.'
    name_field = NameField(name)
    phones_list = [ PhoneField(phone) for phone in set(phones) ]
    record = Record(name_field, phones_list)
    ADDRESS_BOOK.add_record(record)
    return f'Contact "{name}" added to conctacts.'

@input_error
def add_phones(*args):
    name, phones = args[0], args[1:]
    record = ADDRESS_BOOK.get_record(name)
    if record and len(phones):
        added_phones = []
        missed_phones = []
        response = ''
        for phone in set(phones):
            is_added = record.add_phone(PhoneField(phone))
            if is_added:
                added_phones.append(phone)
            else:
                missed_phones.append(phone)
        if len(added_phones):
            response += f'Phones {", ".join(added_phones)} added to contact "{name}"\n'
        if len(missed_phones):
            response += f'Phones {", ".join(missed_phones)} already exists for contact "{name}"'
        return response
    elif record and not len(phones):
        return "You send empty phones list"
    return f'Contact with name {name} doesn\'t exist'

@input_error
def change(*args):
    name, old_phone, new_phone = args[0], args[1], args[2]
    record = ADDRESS_BOOK.get_record(name)
    if record:
        result = record.update_phone(old_phone, new_phone)
        results = (
            f'Phone {new_phone} already exists for this record',
            f'Phone "{old_phone}" was changed to {new_phone} for contact "{name}"!',
            f'Phone "{old_phone}" doen\'t exist for contact {name}'
        )
        return results[int(result)]
    return f'Contact with name "{name}" doesn\'t exist.'

@input_error
def phones (*args):
    name = args[0]
    record = ADDRESS_BOOK.get_record(name)
    if record:
        return f"Contact '{record.name.value}': {', '.join([ phone.value for phone in record.phones ])}"
    return f'Contact with name "{name}" doesn\'t exist.'

@input_error
def remove_phone(*args):
    name, phone = args[0], args[1]
    record = ADDRESS_BOOK.get_record(name)
    if record:
        result = record.remove_phone(phone)
        results = (
            f'Contact phone with id "{phone}" was removed from contact "{name}"!',
            f'Phone "{phone}" doen\'t exist for contact {name}'
        )
        return results[int(result)]
    return f'Contact with "{name}" doesn\'t exist.'

@input_error
def remove_contact(*args):
    name = args[0]
    if name in ADDRESS_BOOK:
        ADDRESS_BOOK.pop(name)
        return f'Contact "{name}" removed from address book'
    return f'Contact "name" does\'t exists in address book'

@input_error
def show_all(*args):
    if len(args):
        raise IndexError
    output = "---CONTACTS---\n"
    if len(ADDRESS_BOOK):
        for record in ADDRESS_BOOK.values():
            phones = ", ".join([ phone.value for phone in record.phones ])
            output += f"{record.name.value} : {phones}\n"
        return output[:-1]
    else:
        output += "Contacts are empty"
        return output
    
@input_error    
def help(*args):
    return """
        --- CONTACTS HELP ---
        syntax: add contact {name} {phone(s)}
        description: adding number to contacts list 
        example: add contact ivan +380999999999 +380777777777

        syntax: add phones {name} {phone(s)}
        description: adding number to contacts list 
        example: add phones ivan +380999999999 +380777777777

        syntax: change {name} {old_phone_number} {new_phone_number}
        description: changing phone number for contact
        example: change ivan +380777777777 +380999999999

        syntax: phones {name}
        description: finding phones numbers by contact name
        example: phones ivan

        syntax: remove contact {name}
        description: removing contact from contacts list
        example: remove ivan

        syntax: remove phone {name} {phone_number}
        description: removing contact from contacts list
        example: remove ivan +380999999999

        syntax: show all
        description: showing list of contacts
        example: show all
    """

CLOSE_COMANDS = ("good bye", "close", "exit")
HANDLERS = {
    "add contact": add_contact,
    "add phones": add_phones,
    "change": change,
    "phones": phones,
    "remove phone": remove_phone,
    "remove contact": remove_contact,
    "show all": show_all,
    "help": help
}