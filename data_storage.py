from models.member import Member
from models.trainer import Trainer
from models.payment import Payment
from models.membership import Membership
from pathlib import Path

class Json_manager:
    ...
    # Get all payments
    def All_payments(self):
        return [
            Payment.from_dict(payment)
            for payment in self.read_from_json_file("payments")
        ]

    # Get all attendance records
    def All_attendance(self):
        return self.read_from_json_file("attendance")

    # Add a check-in record
    def add_attendance(self, member_id, check_date, check_time):
        records = self.All_attendance()
        members = self.read_from_json_file("members")

        member_exists = any(
            str(member.get("member_id")) == str(member_id)
            for member in members
        )
        if not member_exists:
            raise ValueError("Member not found.")

        for record in records:
            if (
                str(record.get("member_id")) == str(member_id)
                and not record.get("check_out")
            ):
                raise ValueError("This member already has an active check-in.")

        numeric_ids = [
            int(record["attendance_id"])
            for record in records
            if str(record.get("attendance_id", "")).isdigit()
        ]
        attendance_id = max(numeric_ids, default=0) + 1

        new_record = {
            "attendance_id": attendance_id,
            "member_id": member_id,
            "date": check_date,
            "check_in": check_time,
            "check_out": ""
        }

        records.append(new_record)
        self.write_to_json_file("attendance", records)
        return attendance_id

    # Update a check-in record with check-out time
    def update_attendance_checkout(self, attendance_id, check_time):
        records = self.All_attendance()
        for record in records:
            if str(record.get("attendance_id")) == str(attendance_id):
                if record.get("check_out"):
                    raise ValueError("This member is already checked out.")
                record["check_out"] = check_time
                self.write_to_json_file("attendance", records)
                return
        raise ValueError("Attendance record not found.")

    # Get all memberships
    def All_memberships(self):
        return [
            Membership.from_dict(membership)
            for membership in self.read_from_json_file("memberships")
        ]
