from datetime import datetime


class Payment:
    ALLOWED_METHODS = (
        "Cash",
        "Card",
        "Bank Transfer",
    )

    def __init__(
        self,
        payment_id: str,
        member_id: str,
        membership_id: str,
        amount: float,
        payment_date: str,
        payment_method: str,
    ):
        self.__payment_id = payment_id
        self.__member_id = member_id
        self.__membership_id = membership_id

        self.amount = amount
        self.payment_date = payment_date
        self.payment_method = payment_method

    @property
    def payment_id(self) -> str:
        return self.__payment_id

    @property
    def member_id(self) -> str:
        return self.__member_id

    @property
    def membership_id(self) -> str:
        return self.__membership_id

    @property
    def amount(self) -> float:
        return self.__amount

    @amount.setter
    def amount(self, value: float) -> None:
        try:
            value = float(value)
        except (TypeError, ValueError):
            raise ValueError("Payment amount must be a number")

        if value <= 0:
            raise ValueError("Payment amount must be greater than zero")

        self.__amount = value

    @property
    def payment_date(self) -> str:
        return self.__payment_date

    @payment_date.setter
    def payment_date(self, value: str):
        try:
            datetime.strptime(value, "%Y-%m-%d")
        except (TypeError, ValueError):
            raise ValueError("Payment date must use YYYY-MM-DD")

        self.__payment_date = value

    @property
    def payment_method(self) -> str:
        return self.__payment_method

    @payment_method.setter
    def payment_method(self, value: str):
        if value not in self.ALLOWED_METHODS:
            raise ValueError("Invalid payment method")

        self.__payment_method = value

    def display_info(self) -> str:
        return (
            f"Payment {self.payment_id} - "
            f"Member: {self.member_id} - "
            f"Amount: €{self.amount:.2f}"
        )

    def to_dict(self) -> dict:
        return {
            "payment_id": self.payment_id,
            "member_id": self.member_id,
            "membership_id": self.membership_id,
            "amount": self.amount,
            "payment_date": self.payment_date,
            "payment_method": self.payment_method,
        }

    @classmethod
    def from_dict(cls, data: dict) -> "Payment":
        return cls(
            payment_id=data["payment_id"],
            member_id=data["member_id"],
            membership_id=data["membership_id"],
            amount=data["amount"],
            payment_date=data["payment_date"],
            payment_method=data["payment_method"],
        )
