from models.person import Person


class Member(Person):
    def __init__(
        self,
        member_id: str,
        name: str,
        phone: str,
        email: str,
        date_of_birth: str,
        gender: str,
        trainer_id: str | None = None,
    ):
        super().__init__(member_id, name, phone, email)

        self.__date_of_birth = date_of_birth
        self.__gender = gender
        self.__trainer_id = trainer_id

    @property
    def member_id(self) -> str:
        return self.person_id

    @property
    def date_of_birth(self) -> str:
        return self.__date_of_birth

    @date_of_birth.setter
    def date_of_birth(self, value: str) -> None:
        self.__date_of_birth = value

    @property
    def gender(self) -> str:
        return self.__gender

    @gender.setter
    def gender(self, value: str) -> None:
        self.__gender = value

    @property
    def trainer_id(self) -> str | None:
        return self.__trainer_id

    @trainer_id.setter
    def trainer_id(self, value: str | None) -> None:
        self.__trainer_id = value

    def assign_trainer(self, trainer_id: str) -> None:
        self.trainer_id = trainer_id

    def remove_trainer(self) -> None:
        self.trainer_id = None

    def display_info(self) -> str:
        return f"Member: {self.name} - ID: {self.member_id}"

    def to_dict(self) -> dict:

        return {
            "member_id": self.member_id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "date_of_birth": self.date_of_birth,
            "gender": self.gender,
            "trainer_id": self.trainer_id,
        }
