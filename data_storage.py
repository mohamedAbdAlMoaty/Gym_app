import json
from models.member import Member
from models.trainer import Trainer
from pathlib import Path


class Json_manager:
    WORK_DIR = "data"

    def read_from_json_file(self, filename):

        file_path = Path(self.WORK_DIR) / f"{filename}.json"
        with open(file_path, "r") as f:
            return json.load(f)

    def append_on_json_file(self, filename, data):

        file_path = Path(self.WORK_DIR) / f"{filename}.json"
        with open(file_path, "a") as f:
            json.dump(data, f, indent=2)

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

    def All_trainers(self):
        return [
            Trainer(
                t["trainer_id"], t["name"], t["phone"], t["email"], t["specialization"]
            )
            for t in (self.read_from_json_file("trainers"))
        ]

    def get_trainer_by_ID(self, id):
        return next(
            (
                Trainer(
                    t["trainer_id"],
                    t["name"],
                    t["phone"],
                    t["email"],
                    t["specialization"],
                )
                for t in self.read_from_json_file("trainers")
                if t["trainer_id"] == id
            ),
            None,
        )

    def member_names(self):
        return [m["name"] for m in (self.read_from_json_file("members"))]

    def member_choices(self):
        return [
            f"{m['member_id']} - {m['name']}"
            for m in (self.read_from_json_file("members"))
        ]
