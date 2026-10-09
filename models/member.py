class member():
  
    def __init__(self,member_id,name,phone,email,date_of_birth,gender,trainer_id):
        self.__member_id = member_id
        self.__name = name
        self.__phone = phone
        self.__email = email
        self.__date_of_birth = date_of_birth
        self.__gender = gender
        self.__trainer_id = trainer_id







    def get_member_id(self):
        return self.__member_id

    def set_member_id(self, member_id):
        self.__member_id = member_id

    def get_name(self):
        return self.__name

    def set_name(self, name):
        self.__name = name

    def get_phone(self):
        return self.__phone

    def set_phone(self, phone):
        self.__phone = phone

    def get_email(self):
        return self.__email

    def set_email(self, email):
        self.__email = email

    def get_date_of_birth(self):
        return self.__date_of_birth

    def set_date_of_birth(self, date_of_birth):
        self.__date_of_birth = date_of_birth

    def get_gender(self):
        return self.__gender

    def set_gender(self, gender):
        self.__gender = gender

    def get_trainer_id(self):
        return self.__trainer_id



    def set_trainer_id(self, trainer_id):
        self.__trainer_id = trainer_id

    def test(self):
        return self.get_name    