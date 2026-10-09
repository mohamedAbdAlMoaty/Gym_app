from models.person import Person


class Trainer(Person):
    def __init__(
        self, trainer_id: str, name: str, phone: str, email: str, specialization: str
    ):
        super().__init__(trainer_id, name, phone, email)

        self.__specialization = specialization

    @property
    def trainer_id(self) -> str:
        return self.person_id

    @property
    def specialization(self) -> str:
        return self.__specialization

    @specialization.setter
    def specialization(self, value: str) -> None:
        if not value.strip():
            raise ValueError("Specialization cannot be empty")

        self.__specialization = value

    def display_info(self) -> str:
        return f"Trainer: {self.name} - Specialization: {self.specialization}"

    def to_dict(self) -> dict:
        return {
            "trainer_id": self.trainer_id,
            "name": self.name,
            "phone": self.phone,
            "email": self.email,
            "specialization": self.specialization,
        }
