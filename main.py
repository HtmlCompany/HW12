from collections import UserDict
from datetime import date, timedelta
from itertools import islice
import csv


class Field:
    def __init__(self, value:str) -> None:
        self.value = value

    def __str__(self) -> str:
        return str(self.value)

class Name(Field):
    def __init__(self, value:str) -> None:
        super().__init__(value)

    def __str__(self) -> str:
        return super().__str__()

class Phone(Field):
    def __init__(self, value:str) -> None:
        self.__value = None
        self.value = value
        super().__init__(value)
    
    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if len(value) == 10:
            self.__value = value
        else:
            raise ValueError("In phone must be 10 digits")

class Birthday(Field):
    def __init__(self, value: date) -> None:
        self.__value = None
        self.value = value
        super().__init__(value)

    @property
    def value(self):
        return self.__value
    
    @value.setter
    def value(self, value):
        if not isinstance(value, date):
            raise ValueError("Not a date")
        self.__value = value

    def __str__(self) -> str:
        return super().__str__()

class Record:
    def __init__(self, name:str, birthday) -> None:
        self.name = Name(name)
        self.phones = []
        self.birthday = Birthday(birthday)

    def add_phone(self, phone:str):
        self.phones.append(Phone(phone))
    
    def remove_phone(self, f_phone:str):
        for i in self.phones:
            if i.value == f_phone:
                self.phones.remove(i)
                print(f"Deleted phone: {i}")
    
    def edit_phone(self, old_phone: str, new_phone:str):
        counter = 0
        for i in self.phones:
            if i.value == old_phone:
                i.value = new_phone
                print(f"Old phone:{old_phone}, nwe phone: {new_phone}")
            else:
                counter += 1
                if counter == len(self.phones):
                    raise ValueError
            
    def find_phone(self, find_phone:str):
        for i in self.phones:
            if i.value == find_phone:
                return i

    def days_to_birthday(self):
        dt_birthday = self.birthday.value.replace(year=date.today().year) - date.today()
        return f"Days to birthday {self.name}: {dt_birthday}"

    def __str__(self) -> str:
        return f"Contact name: {self.name.value}, phones: {'; '.join(p.value for p in self.phones)}, bd:{self.birthday}"

class AddressBook(UserDict):
    def add_record(self, record: Record):
        self.data[record.name.value] = record

    def find(self, name:Name):
        if name in self.data.keys():
            return self.data[name]
        else:
            return None

    def delete(self, name:Name):
        if name in self.data.keys():
            self.data.pop(name)
            print(f"Deleted {name}")
        else:
            print(f"No contact {name} to delete")
    
    def iterator(self, n = 2):
        self.counter = 0
        while self.counter < len(book.data.items()):
            yield islice(book.data.values(), self.counter, self.counter + n)
            # print(book.data.items())
            self.counter += n
    
    def save_to_file(self, filename: str):
        with open(filename, "w") as file:
            field_names = ['name', 'info']
            writer = csv.DictWriter(file, fieldnames=field_names)
            writer.writeheader()
            for name, record in book.data.items():
                writer.writerow({field_names[0]: name, field_names[1]: record})
    
    def load_from_file(self, filename: str):
        data = {}
        with open(filename, "r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                #print(row)
                data[row["name"]] = row["info"]
        return data
    
    def search_in_book(self, search_info: str):
        matches = []
        for name, record in book.data.items():
            #print(str(record))
            if str(record).find(search_info) != -1:
                matches.append(str(name))
        return matches


book = AddressBook()

user1 = Record("Ramis", date(1959, 11, 9))
user1.add_phone("1234567890")

user2 = Record("Aqil", date(1959, 11, 9))
user2.add_phone("1234567890")

user3 = Record("Tofik", date(1959, 11, 9))
user3.add_phone("1234567890")

user4 = Record("User 4", date(1959, 11, 9))
user4.add_phone("1234567890")

book.add_record(user1)
book.add_record(user2)
book.add_record(user3)
book.add_record(user4)

for i in book.iterator(2):
    print(" ".join([str(r) for r in list(i)]))

book.save_to_file("test.csv")
print(book.load_from_file("test.csv"))
print(book.search_in_book("123"))