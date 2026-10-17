import storage

from models.member import Member
from models.trainer import Trainer
from models.payment import Payment
from models.membership import Membership
from models.attendance import Attendance


class Json_manager:
    # =========================
    # FILE ACCESS
    # =========================

    def read_from_json_file(self, filename: str) -> list:

        return storage.load(filename)

    def write_to_json_file(self, filename: str, data: list) -> None:

        storage.save(filename, data)

    # =========================
    # MEMBERS
    # =========================

    def All_members(self) -> list[Member]:

        return [
            Member(
                member_id=item["member_id"],
                name=item["name"],
                phone=item["phone"],
                email=item["email"],
                date_of_birth=item["date_of_birth"],
                gender=item["gender"],
                trainer_id=item.get("trainer_id") or None,
            )
            for item in self.read_from_json_file("members")
        ]

    def search_on_members(self, text: str) -> list[Member]:

        text = text.strip().lower()

        if not text:
            return self.All_members()

        return [
            member
            for member in self.All_members()
            if text
            in (
                f"{member.member_id} {member.name} {member.phone} {member.email}"
            ).lower()
        ]

    def member_choices(self) -> list[str]:

        return [
            (f"{member.member_id} - {member.name}") for member in self.All_members()
        ]

    # =========================
    # TRAINERS
    # =========================

    def All_trainers(self) -> list[Trainer]:

        return [
            Trainer(
                trainer_id=item["trainer_id"],
                name=item["name"],
                phone=item["phone"],
                email=item["email"],
                specialization=item["specialization"],
            )
            for item in self.read_from_json_file("trainers")
        ]

    def get_trainer_by_ID(self, trainer_id: str | None) -> Trainer | None:

        if not trainer_id:
            return None

        return next(
            (
                trainer
                for trainer in self.All_trainers()
                if trainer.trainer_id == trainer_id
            ),
            None,
        )

    # =========================
    # MEMBERSHIPS
    # =========================

    def All_memberships(self) -> list[Membership]:

        return [
            Membership.from_dict(item)
            for item in self.read_from_json_file("memberships")
        ]

    # =========================
    # PAYMENTS
    # =========================

    def All_payments(self) -> list[Payment]:

        return [
            Payment.from_dict(item) for item in self.read_from_json_file("payments")
        ]

    # =========================
    # ATTENDANCE
    # =========================

    def All_attendance(self) -> list[Attendance]:

        return [
            Attendance.from_dict(item)
            for item in self.read_from_json_file("attendance")
        ]

    def add_attendance(
        self,
        member_id: str,
        check_date: str,
        check_time: str,
    ) -> Attendance:

        if not storage.get_member(member_id):
            raise ValueError("Member not found.")

        day = storage.parse_date(check_date)

        if day is None:
            raise ValueError(("Attendance date must use YYYY-MM-DD"))

        if storage.parse_time(check_time) is None:
            raise ValueError(("Check-in time must use HH:MM"))

        if not storage.has_active_membership_on(member_id, day):
            raise ValueError(
                ("Member cannot attend without an active membership on this date.")
            )

        if storage.open_attendance(member_id):
            raise ValueError(("This member already has an active check-in."))

        return storage.add_attendance(
            member_id=member_id,
            day=check_date,
            check_in=check_time,
        )

    def update_attendance_checkout(
        self,
        attendance_id: str,
        check_time: str,
    ) -> None:

        records = self.read_from_json_file("attendance")

        for index, item in enumerate(records):
            if str(item.get("attendance_id")) != str(attendance_id):
                continue

            attendance = Attendance.from_dict(item)

            if not attendance.is_open:
                raise ValueError(("This member is already checked out."))

            attendance.check_out_member(check_time)

            records[index] = attendance.to_dict()

            self.write_to_json_file("attendance", records)

            return

        raise ValueError("Attendance record not found.")
