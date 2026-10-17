from datetime import date, datetime


class Membership:
    DATE_FORMAT = "%Y-%m-%d"

    def __init__(
        self,
        membership_id: str,
        member_id: str,
        plan: str,
        start_date: str,
        end_date: str,
    ):
        self.__membership_id = membership_id
        self.__member_id = member_id
        self.__plan = plan

        self.__start_date = self._validate_date(start_date, "Start date")

        self.__end_date = self._validate_date(end_date, "End date")

        start = self._to_date(self.__start_date)
        end = self._to_date(self.__end_date)

        if end < start:
            raise ValueError("End date cannot be before start date")

    @staticmethod
    def _validate_date(value: str, field_name: str) -> str:

        try:
            datetime.strptime(value, Membership.DATE_FORMAT)

        except (TypeError, ValueError):
            raise ValueError(f"{field_name} must use YYYY-MM-DD")

        return value

    @staticmethod
    def _to_date(value: str):
        return datetime.strptime(value, Membership.DATE_FORMAT).date()

    @property
    def membership_id(self) -> str:
        return self.__membership_id

    @property
    def member_id(self) -> str:
        return self.__member_id

    @property
    def plan(self) -> str:
        return self.__plan

    @property
    def start_date(self) -> str:
        return self.__start_date

    @property
    def end_date(self) -> str:
        return self.__end_date

    @property
    def status(self) -> str:

        today = date.today()

        start = self._to_date(self.start_date)

        end = self._to_date(self.end_date)

        if today < start:
            return "Upcoming"

        if start <= today <= end:
            return "Active"

        return "Expired"

    def display_info(self) -> str:
        return f"Membership {self.membership_id} - {self.plan} - {self.status}"

    def to_dict(self) -> dict:
        return {
            "membership_id": self.membership_id,
            "member_id": self.member_id,
            "plan": self.plan,
            "start_date": self.start_date,
            "end_date": self.end_date,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Membership":

        return cls(
            membership_id=data["membership_id"],
            member_id=data["member_id"],
            plan=data["plan"],
            start_date=data["start_date"],
            end_date=data["end_date"],
        )
