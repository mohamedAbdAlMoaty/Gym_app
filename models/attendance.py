from datetime import date 
from typing import Any
class attendance:
    def __init__(self , attendance_id :int , member_id :int , attendance_date:str |None = None,):
        #when there is no attendance date the date will calculate automatically 
        #prevent attendance_id value equal zero or less than zero 
        if attendance_id <=0:
            raise ValueError ("Attendance Id Must be Greater Than zero")
        #prevent attendance_id value equal zero or less than zero 
        if member_id <=0:
            raise ValueError ("Member Id Must be Greater Than zero")
        #detect attendance date 
        if attendance_date is None:
            attendance_date = date.today().isoformat()
        #make sure the date is valid YYYY-MM-DD ex 2026-10-10 not "today"
        try:
            date.fromisoformat(attendance_date)
        except ValueError as exc:
            raise ValueError("Attendance date must use YYYY-MM-DD") from exc
        self.__attendance_id = attendance_id
        self.__member_id = member_id
        self.__attendance_date = attendance_date
    @property
    def attendance_id(self) -> int:
        return self.__attendance_id
    @property
    def member_id(self) -> int:
     return self.__member_id
    @property
    def attendace_date(self)-> str:
        return self.__attendance_date
        #make attendances dict
    def attendance_dict (self) ->dict [str , Any]:
        return {
            "attendance_id":self.attendance_id, 
            "member_id":self.member_id, 
            "attendace_date":self.attendace_date,
            }
    """
    if read data from json file . we can conert it to dict and can reinitiate object
    """
    @classmethod
    def from_attendance_dict(cls , data:dict[str , Any]) ->"attendance":
        return cls(
            int(data["attendance_id"]), 
            int(data["member_id"]), 
            str(data["attendance_date"])
        )

