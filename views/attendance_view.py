import customtkinter as ctk
from datetime import datetime
from tkinter import messagebox
from data_storage import Json_manager

from views.common import (page_title, toolbar, create_table, fill_table, selected_id,
                          open_dialog, dialog_title, add_entry, add_combo, add_save_button,
                          member_choices, choice_id)


class AttendanceView:

    def __init__(self, parent):
        self.parent = parent
        self.show_attendance()

    def show_attendance(self):
        page_title(self.parent, "Attendance")

        bar = toolbar(self.parent)

        self.search_entry = ctk.CTkEntry(bar, placeholder_text="Search by member, ID or date", width=280)
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_table())

        self.today_only = ctk.CTkCheckBox(bar, text="Today only", command=self.refresh_table)
        self.today_only.pack(side="left", padx=10)

        ctk.CTkButton(bar, text="Check Out Selected", command=self.check_out).pack(side="right", padx=(10, 0))
        ctk.CTkButton(bar, text="+ Check In", command=self.check_in).pack(side="right")

        self.table = create_table(
            self.parent, ["Attendance ID", "Member ID", "Member", "Date", "Check In", "Check Out"],
            widths=[110, 90, 160, 110, 90, 90])
        self.refresh_table()

    def refresh_table(self):
        json_manager = Json_manager()
        # print(json_manager.read_from_json_file("attendance"))

        text = self.search_entry.get().strip().lower()
        
        # load the data and then pass this to fill_table()



        
        fill_table(self.table, )

    # =========================
    # CHECK IN
    # =========================

    def check_in(self):
        if not Json_manager.member_names:
            messagebox.showwarning("Check In", "Add a member first.")
            return

        window = open_dialog(self.parent, "Check In", "450x430")
        dialog_title(window, "Member Check In")

        member = add_combo(window, "Member", Json_manager.member_names)
        day = add_entry(window, "Date (YYYY-MM-DD)", "2026-10-10")
        time_entry = add_entry(window, "Check-in time (HH:MM)", datetime.now().strftime("%H:%M"))

        def save():
            member_id = choice_id(member.get())
            # check_date 
            # check_time 








            # add_attendance(member_id, check_date.strftime(storage.DATE_FORMAT), check_time)
            window.destroy()
            self.refresh_table()

        add_save_button(window, "Check In", save)

    # =========================
    # CHECK OUT
    # =========================

    def check_out(self):
        attendance_id = selected_id(self.table)
        if not attendance_id:
            messagebox.showwarning("Check Out", "Please select an attendance record first.")
            return

        # check the attendance storage and if the member checkout alredy show this
            messagebox.showinfo("Check Out", "This member is already checked out.")
            return

        window = open_dialog(self.parent, "Check Out", "450x300")
        dialog_title(window, "Member Check Out")
        # ctk.CTkLabel(window, text=f"{storage.member_name(record['member_id'])} — in at "
                                #   f"{record['check_in']} ({record['date']})").pack()
        time_entry = add_entry(window, "Check-out time (HH:MM)", datetime.now().strftime("%H:%M"))

        def save():

            # write the data in storage

         


            window.destroy()
            self.refresh_table()

        add_save_button(window, "Check Out", save)
