
import json
from pathlib import Path

from models.member import Member
from models.trainer import Trainer
from models.payment import Payment


class Json_manager:

    WORK_DIR = Path(__file__).resolve().parent / "data"

    # Create the data directory if it does not exist
    def __init__(self):
        self.WORK_DIR.mkdir(parents=True, exist_ok=True)

    # Read data from a JSON file
    def read_from_json_file(self, filename):
        file_path = self.WORK_DIR / f"{filename}.json"

        if not file_path.exists():
            return []

        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)

    # Save data to a JSON file
    def write_to_json_file(self, filename, data):
        file_path = self.WORK_DIR / f"{filename}.json"

        with open(file_path, "w", encoding="utf-8") as file:
            json.dump(
                data,
                file,
                indent=2,
                ensure_ascii=False
            )

    # Append data to an existing JSON file
    def append_on_json_file(self, filename, data):
        records = self.read_from_json_file(filename)
        records.append(data)
        self.write_to_json_file(filename, records)

    # Get all members
    def All_members(self):
        return [
            Member(
                m["member_id"],
                m["name"],
                m["phone"],
                m["email"],
                m["date_of_birth"],
                m["gender"],
                m.get("trainer_id"),
            )
            for m in self.read_from_json_file("members")
        ]

    # Search members
    def search_on_members(self, text):
        text = str(text).lower()

        return [
            Member(
                m["member_id"],
                m["name"],
                m["phone"],
                m["email"],
                m["date_of_birth"],
                m["gender"],
                m.get("trainer_id"),
            )
            for m in self.read_from_json_file("members")
            if (
                text in str(m.get("member_id", "")).lower()
                or text in str(m.get("name", "")).lower()
                or text in str(m.get("phone", "")).lower()
                or text in str(m.get("email", "")).lower()
            )
        ]

    # Get all trainers
    def All_trainers(self):
        return [
            Trainer(
                t["trainer_id"],
                t["name"],
                t["phone"],
                t["email"],
                t["specialization"]
            )
            for t in self.read_from_json_file("trainers")
        ]

    # Get trainer by ID
    def get_trainer_by_ID(self, id):
        return next(
            (
                Trainer(
                    t["trainer_id"],
                    t["name"],
                    t["phone"],
                    t["email"],
                    t["specialization"]
                )
                for t in self.read_from_json_file("trainers")
                if str(t["trainer_id"]) == str(id)
            ),
            None
        )

    # Get member names
    def member_names(self):
        return [
            m["name"]
            for m in self.read_from_json_file("members")
        ]

    # Get member choices for ComboBox
    def member_choices(self):
        return [
            f"{m['member_id']} - {m['name']}"
            for m in self.read_from_json_file("members")
        ]

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

        # Verify that the member exists
        members = self.read_from_json_file("members")

        member_exists = any(
            str(member.get("member_id")) == str(member_id)
            for member in members
        )

        if not member_exists:
            raise ValueError("Member not found.")

        # Prevent a second check-in before checking out
        for record in records:
            if (
                str(record.get("member_id")) == str(member_id)
                and not record.get("check_out")
            ):
                raise ValueError(
                    "This member already has an active check-in."
                )

        # Generate the next attendance ID
        numeric_ids = [
            int(record["attendance_id"])
            for record in records
            if str(record.get("attendance_id", "")).isdigit()
        ]

        attendance_id = max(numeric_ids, default=0) + 1

        # Create the attendance record
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

                # Prevent checking out twice
                if record.get("check_out"):
                    raise ValueError(
                        "This member is already checked out."
                    )

                record["check_out"] = check_time

                self.write_to_json_file("attendance", records)

                return

        raise ValueError("Attendance record not found.")
