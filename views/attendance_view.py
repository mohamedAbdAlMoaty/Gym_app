
import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox

from data_storage import Json_manager
from views.common import (
    page_title,
    toolbar,
    create_table,
    fill_table,
    selected_id,
    open_dialog,
    dialog_title,
    add_entry,
    add_combo,
    add_save_button,
    choice_id,
)


class AttendanceView:

    def __init__(self, parent):
        self.parent = parent
        self.json_manager = Json_manager()
        self.show_attendance()

    def show_attendance(self):
        page_title(self.parent, "Attendance")

        bar = toolbar(self.parent)

        self.search_entry = ctk.CTkEntry(
            bar,
            placeholder_text="Search by member, ID or date",
            width=280
        )
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind(
            "<KeyRelease>",
            lambda event: self.refresh_table()
        )

        self.today_only = ctk.CTkCheckBox(
            bar,
            text="Today only",
            command=self.refresh_table
        )
        self.today_only.pack(side="left", padx=10)

        ctk.CTkButton(
            bar,
            text="Check Out Selected",
            command=self.check_out
        ).pack(side="right", padx=(10, 0))

        ctk.CTkButton(
            bar,
            text="+ Check In",
            command=self.check_in
        ).pack(side="right")

        self.table = create_table(
            self.parent,
            [
                "Attendance ID",
                "Member ID",
                "Member",
                "Date",
                "Check In",
                "Check Out"
            ],
            widths=[110, 90, 160, 110, 90, 90]
        )

        self.refresh_table()

    # =========================
    # REFRESH TABLE
    # =========================

    def refresh_table(self):
        records = self.json_manager.All_attendance()
        members = self.json_manager.read_from_json_file("members")

        member_map = {
            str(member["member_id"]): member["name"]
            for member in members
        }

        search_text = self.search_entry.get().strip().lower()
        today = datetime.now().strftime("%Y-%m-%d")

        rows = []

        for record in records:
            attendance_id = record.get("attendance_id", "")
            member_id = record.get("member_id", "")
            member_name = member_map.get(str(member_id), "Unknown")
            date = record.get("date", "")
            check_in = record.get("check_in", "")
            check_out = record.get("check_out", "")

            if self.today_only.get() and date != today:
                continue

            searchable = " ".join([
                str(attendance_id),
                str(member_id),
                member_name,
                str(date)
            ]).lower()

            if search_text and search_text not in searchable:
                continue

            rows.append([
                attendance_id,
                member_id,
                member_name,
                date,
                check_in,
                check_out
            ])

        fill_table(self.table, rows)

    # =========================
    # CHECK IN
    # =========================

    def check_in(self):
        names = self.json_manager.member_choices()

        if not names:
            messagebox.showwarning(
                "Check In",
                "Add a member first."
            )
            return

        window = open_dialog(
            self.parent,
            "Check In",
            "450x430"
        )

        dialog_title(window, "Member Check In")

        member = add_combo(window, "Member", names)

        day = add_entry(
            window,
            "Date (YYYY-MM-DD)",
            datetime.now().strftime("%Y-%m-%d")
        )

        time_entry = add_entry(
            window,
            "Check-in time (HH:MM)",
            datetime.now().strftime("%H:%M")
        )

        def save():
            selected_member = member.get().strip()
            date_text = day.get().strip()
            time_text = time_entry.get().strip()

            if not selected_member:
                messagebox.showwarning(
                    "Check In",
                    "Please select a member."
                )
                return

            try:
                check_date = datetime.strptime(
                    date_text, "%Y-%m-%d"
                ).strftime("%Y-%m-%d")

                check_time = datetime.strptime(
                    time_text, "%H:%M"
                ).strftime("%H:%M")

                member_id = choice_id(selected_member)

                self.json_manager.add_attendance(
                    member_id,
                    check_date,
                    check_time
                )

            except ValueError as error:
                messagebox.showerror(
                    "Check In",
                    str(error) if "already has an active" in str(error)
                    else "Invalid date or time. Use YYYY-MM-DD and HH:MM."
                )
                return

            except Exception as error:
                messagebox.showerror(
                    "Check In",
                    f"Could not save attendance:\n{error}"
                )
                return

            window.destroy()
            self.refresh_table()

            messagebox.showinfo(
                "Check In",
                "Attendance recorded successfully."
            )

        add_save_button(window, "Check In", save)

    # =========================
    # CHECK OUT
    # =========================

    def check_out(self):
        attendance_id = selected_id(self.table)

        if not attendance_id:
            messagebox.showwarning(
                "Check Out",
                "Please select an attendance record first."
            )
            return

        records = self.json_manager.All_attendance()

        record = next(
            (
                item for item in records
                if str(item["attendance_id"]) == str(attendance_id)
            ),
            None
        )

        if record is None:
            messagebox.showerror(
                "Check Out",
                "Attendance record not found."
            )
            return

        if record.get("check_out"):
            messagebox.showinfo(
                "Check Out",
                "This member is already checked out."
            )
            return

        window = open_dialog(
            self.parent,
            "Check Out",
            "450x300"
        )

        dialog_title(window, "Member Check Out")

        time_entry = add_entry(
            window,
            "Check-out time (HH:MM)",
            datetime.now().strftime("%H:%M")
        )

        def save():
            time_text = time_entry.get().strip()

            try:
                check_time = datetime.strptime(
                    time_text, "%H:%M"
                ).strftime("%H:%M")

                self.json_manager.update_attendance_checkout(
                    attendance_id,
                    check_time
                )

            except ValueError as error:
                messagebox.showerror(
                    "Check Out",
                    str(error)
                )
                return

            except Exception as error:
                messagebox.showerror(
                    "Check Out",
                    f"Could not save check-out:\n{error}"
                )
                return

            window.destroy()
            self.refresh_table()

            messagebox.showinfo(
                "Check Out",
                "Check-out recorded successfully."
            )

        add_save_button(window, "Check Out", save)
