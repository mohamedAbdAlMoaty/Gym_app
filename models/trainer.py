class Trainer:
    def __init__(self, trainer_id, name, phone, email, specialization):
        self.__trainer_id = trainer_id
        self.__name = name
        self.__phone = phone
        self.__email = email
        self.__specialization = specialization

   
    def get_trainer_id(self):
        return self.__trainer_id

    def get_name(self):
        return self.__name

    def get_phone(self):
        return self.__phone

    def get_email(self):
        return self.__email

    def get_specialization(self):
        return self.__specialization

 
    def set_trainer_id(self, value):
        self.__trainer_id = value

    def set_name(self, value):
        self.__name = value

    def set_phone(self, value):
        self.__phone = value

    def set_email(self, value):
        self.__email = value

    def set_specialization(self, value):
        self.__specialization = value

