from datetime import datetime


class Attendance:
    DATE_FORMAT = "%Y-%m-%d"
    TIME_FORMAT = "%H:%M"

    def __init__(
        self,
        attendance_id: str,
        member_id: str,
        attendance_date: str,
        check_in: str,
        check_out: str = "",
    ):

        if not str(attendance_id).strip():
            raise ValueError("Attendance ID cannot be empty")

        if not str(member_id).strip():
            raise ValueError("Member ID cannot be empty")

        self.__attendance_id = str(attendance_id).strip()

        self.__member_id = str(member_id).strip()

        self.__attendance_date = self._validate_date(attendance_date)

        self.__check_in = self._validate_time(check_in, "Check-in time")

        self.__check_out = ""

        if check_out:
            self.check_out_member(check_out)

    # =========================
    # VALIDATION
    # =========================

    @classmethod
    def _validate_date(cls, value: str) -> str:

        try:
            datetime.strptime(value, cls.DATE_FORMAT)

        except (TypeError, ValueError) as error:
            raise ValueError("Attendance date must use YYYY-MM-DD") from error

        return value

    @classmethod
    def _validate_time(cls, value: str, field_name: str) -> str:

        try:
            return datetime.strptime(value, cls.TIME_FORMAT).strftime(cls.TIME_FORMAT)

        except (TypeError, ValueError) as error:
            raise ValueError(f"{field_name} must use HH:MM") from error

    # =========================
    # PROPERTIES
    # =========================

    @property
    def attendance_id(self) -> str:
        return self.__attendance_id

    @property
    def member_id(self) -> str:
        return self.__member_id

    @property
    def attendance_date(self) -> str:
        return self.__attendance_date

    @property
    def check_in(self) -> str:
        return self.__check_in

    @property
    def check_out(self) -> str:
        return self.__check_out

    @property
    def is_open(self) -> bool:
        return self.check_out == ""

    # =========================
    # CHECK OUT
    # =========================

    def check_out_member(self, check_out: str) -> None:

        check_out = self._validate_time(check_out, "Check-out time")

        start = datetime.strptime(self.check_in, self.TIME_FORMAT)

        end = datetime.strptime(check_out, self.TIME_FORMAT)

        if end < start:
            raise ValueError("Check-out time cannot be before check-in time")

        self.__check_out = check_out

    # =========================
    # DISPLAY
    # =========================

    def display_info(self) -> str:

        status = "Open" if self.is_open else f"Out: {self.check_out}"

        return (
            f"Attendance {self.attendance_id} - "
            f"Member {self.member_id} - "
            f"{self.attendance_date} - "
            f"{status}"
        )

    # =========================
    # JSON
    # =========================

    def to_dict(self) -> dict:

        return {
            "attendance_id": self.attendance_id,
            "member_id": self.member_id,
            "date": self.attendance_date,
            "check_in": self.check_in,
            "check_out": self.check_out,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Attendance":

        return cls(
            attendance_id=data["attendance_id"],
            member_id=data["member_id"],
            attendance_date=data["date"],
            check_in=data["check_in"],
            check_out=data.get("check_out", ""),
        )
