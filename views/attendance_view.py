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

    # =========================
    # PAGE
    # =========================

    def show_attendance(self):

        page_title(self.parent, "Attendance")

        bar = toolbar(self.parent)

        self.search_entry = ctk.CTkEntry(
            bar,
            placeholder_text=("Search by member, ID or date"),
            width=280,
        )

        self.search_entry.pack(side="left", padx=(0, 10))

        self.search_entry.bind("<KeyRelease>", lambda event: self.refresh_table())

        self.today_only = ctk.CTkCheckBox(
            bar,
            text="Today only",
            command=self.refresh_table,
        )

        self.today_only.pack(side="left", padx=10)

        ctk.CTkButton(
            bar,
            text="Check Out Selected",
            command=self.check_out,
        ).pack(side="right", padx=(10, 0))

        ctk.CTkButton(
            bar,
            text="+ Check In",
            command=self.check_in,
        ).pack(side="right")

        self.table = create_table(
            self.parent,
            [
                "Attendance ID",
                "Member ID",
                "Member",
                "Date",
                "Check In",
                "Check Out",
            ],
            widths=[110, 90, 160, 110, 90, 90],
        )

        self.refresh_table()

    # =========================
    # REFRESH
    # =========================

    def refresh_table(self):

        records = self.json_manager.All_attendance()

        search_text = self.search_entry.get().strip().lower()

        today = datetime.now().strftime("%Y-%m-%d")

        rows = []

        for record in records:
            member_name = self._member_name(record.member_id)

            if self.today_only.get() and record.attendance_date != today:
                continue

            searchable = (
                f"{record.attendance_id} "
                f"{record.member_id} "
                f"{member_name} "
                f"{record.attendance_date}"
            ).lower()

            if search_text and search_text not in searchable:
                continue

            rows.append(
                (
                    record.attendance_id,
                    record.member_id,
                    member_name,
                    record.attendance_date,
                    record.check_in,
                    record.check_out or "-",
                )
            )

        fill_table(self.table, rows)

    # =========================
    # CHECK IN
    # =========================

    def check_in(self):

        names = self.json_manager.member_choices()

        if not names:
            messagebox.showwarning("Check In", "Add a member first.")

            return

        window = open_dialog(self.parent, "Check In", "450x430")

        dialog_title(window, "Member Check In")

        member = add_combo(window, "Member", names)

        day = add_entry(
            window,
            "Date (YYYY-MM-DD)",
            datetime.now().strftime("%Y-%m-%d"),
        )

        time_entry = add_entry(
            window,
            "Check-in time (HH:MM)",
            datetime.now().strftime("%H:%M"),
        )

        def save():

            member_id = choice_id(member.get().strip())

            date_text = day.get().strip()

            time_text = time_entry.get().strip()

            if not member_id:
                messagebox.showwarning(
                    "Check In",
                    "Please select a member.",
                    parent=window,
                )

                return

            try:
                self.json_manager.add_attendance(
                    member_id,
                    date_text,
                    time_text,
                )

            except ValueError as error:
                messagebox.showerror(
                    "Check In",
                    str(error),
                    parent=window,
                )

                return

            except Exception as error:
                messagebox.showerror(
                    "Check In",
                    (f"Could not save attendance:\n{error}"),
                    parent=window,
                )

                return

            window.destroy()

            self.refresh_table()

            messagebox.showinfo("Check In", "Attendance recorded successfully.")

        add_save_button(window, "Check In", save)

    # =========================
    # CHECK OUT
    # =========================

    def check_out(self):

        attendance_id = selected_id(self.table)

        if not attendance_id:
            messagebox.showwarning(
                "Check Out",
                ("Please select an attendance record first."),
            )

            return

        record = next(
            (
                item
                for item in self.json_manager.All_attendance()
                if item.attendance_id == attendance_id
            ),
            None,
        )

        if record is None:
            messagebox.showerror("Check Out", "Attendance record not found.")

            return

        if not record.is_open:
            messagebox.showinfo(
                "Check Out",
                ("This member is already checked out."),
            )

            return

        window = open_dialog(self.parent, "Check Out", "450x300")

        dialog_title(window, "Member Check Out")

        time_entry = add_entry(
            window,
            "Check-out time (HH:MM)",
            datetime.now().strftime("%H:%M"),
        )

        def save():

            try:
                (
                    self.json_manager.update_attendance_checkout(
                        attendance_id,
                        time_entry.get().strip(),
                    )
                )

            except ValueError as error:
                messagebox.showerror(
                    "Check Out",
                    str(error),
                    parent=window,
                )

                return

            except Exception as error:
                messagebox.showerror(
                    "Check Out",
                    (f"Could not save check-out:\n{error}"),
                    parent=window,
                )

                return

            window.destroy()

            self.refresh_table()

            messagebox.showinfo(
                "Check Out",
                ("Check-out recorded successfully."),
            )

        add_save_button(window, "Check Out", save)

    # =========================
    # MEMBER NAME
    # =========================

    def _member_name(self, member_id: str) -> str:

        member = next(
            (
                item
                for item in self.json_manager.All_members()
                if item.member_id == member_id
            ),
            None,
        )

        return member.name if member else "Unknown"
