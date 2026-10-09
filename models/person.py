from abc import ABC, abstractmethod


class Person(ABC):
    def __init__(self, person_id: str, name: str, phone: str, email: str):
        self.__person_id = person_id
        self.__name = name
        self.__phone = phone
        self.__email = email

    @property
    def person_id(self) -> str:
        return self.__person_id

    @property
    def name(self) -> str:
        return self.__name

    @name.setter
    def name(self, value: str) -> None:
        if not value.strip():
            raise ValueError("Name cannot be empty")

        self.__name = value

    @property
    def phone(self) -> str:
        return self.__phone

    @phone.setter
    def phone(self, value: str) -> None:
        self.__phone = value

    @property
    def email(self) -> str:
        return self.__email

    @email.setter
    def email(self, value: str) -> None:
        self.__email = value

    def get_name(self) -> str:
        return self.name

    def get_phone(self) -> str:
        return self.phone

    def get_email(self) -> str:
        return self.email

    def set_name(self, value: str) -> None:
        self.name = value

    def set_phone(self, value: str) -> None:
        self.phone = value

    def set_email(self, value: str) -> None:
        self.email = value

    @abstractmethod
    def display_info(self) -> str:
        pass
