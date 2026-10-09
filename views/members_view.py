import customtkinter as ctk
from tkinter import messagebox
from data_storage import Json_manager

import storage
from views.common import (page_title, toolbar, create_table, fill_table, selected_id,
                          open_dialog, dialog_title, add_entry, add_combo, add_save_button,
                          trainer_choices, trainer_choice_for, choice_id)

STATUS_FILTERS = ["All", "Active", "Expired", "No Membership"]


class MembersView:

    def __init__(self, parent):
        self.parent = parent
        self.show_members()

    # =========================
    # PAGE
    # =========================

    def show_members(self):
        page_title(self.parent, "Members")

        bar = toolbar(self.parent)

        self.search_entry = ctk.CTkEntry(bar, placeholder_text="Search by name, ID, phone or email", width=300)
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_table())  # live search
        self.search_entry.bind("<Return>", lambda e: self.refresh_table())

        ctk.CTkButton(bar, text="Search", command=self.refresh_table).pack(side="left")

        self.status_filter = ctk.CTkComboBox(bar, values=STATUS_FILTERS, width=150, state="readonly",
                                             command=lambda _: self.refresh_table())
        self.status_filter.set("All")
        self.status_filter.pack(side="left", padx=10)

        ctk.CTkButton(bar, text="+ Add Member", command=self.add_member_window).pack(side="right")

        self.member_table = create_table(
            self.parent, ["ID", "Name", "Phone", "Email", "Trainer", "Status"],
            widths=[80, 150, 120, 220, 140, 120])

        buttons = ctk.CTkFrame(self.parent, fg_color="transparent")
        buttons.pack(fill="x", padx=30, pady=15)
        ctk.CTkButton(buttons, text="Edit", width=100, command=self.edit_member).pack(side="left", padx=5)
        ctk.CTkButton(buttons, text="Assign Trainer", width=130, command=self.assign_trainer).pack(side="left", padx=5)
        ctk.CTkButton(buttons, text="Delete", width=100, fg_color="#c0392b", hover_color="#962d22",
                      command=self.delete_member).pack(side="left", padx=5)

        self.refresh_table()

    def refresh_table(self):
        text = self.search_entry.get().strip().lower()
        wanted = self.status_filter.get()

        rows=[]
        for member in Json_manager().All_members():
            # if member.get_name == text or member.get_member_id == text or member.get_email== text or member.get_phone == text:
                 
                trainer = Json_manager().get_trainer_by_ID(member.get_trainer_id())
                trainer_name = trainer.get_name() if trainer else "No trainer"
                rows.append((member.get_member_id(),member.get_name(),member.get_phone(),member.get_email(),trainer_name,"test"))







 
        fill_table(self.member_table,rows )

    # =========================
    # ADD / EDIT
    # =========================

    def add_member_window(self):
        self.member_form()

    def edit_member(self):
        member_id = selected_id(self.member_table)
        if not member_id:
            messagebox.showwarning("Edit Member", "Please select a member first.")
            return
        # get the member that been selected and send him to form to be edit
        self.member_form(storage.get_member(member_id))

    def member_form(self, member=None):
        editing = member is not None
        window = open_dialog(self.parent, "Edit Member" if editing else "Add New Member", "450x680")
        dialog_title(window, "Edit Member" if editing else "Add New Member")

        get = (lambda key: member.get(key, "")) if editing else (lambda key: "")

        name = add_entry(window, "Name", get("name"))
        phone = add_entry(window, "Phone", get("phone"))
        email = add_entry(window, "Email", get("email"))
        dob = add_entry(window, "Date of Birth (YYYY-MM-DD)", get("date_of_birth"))
        gender = add_combo(window, "Gender", ["Male", "Female"], get("gender") or None)
        trainer = add_combo(window, "Trainer", trainer_choices(),
                            trainer_choice_for(get("trainer_id")) if editing else "Unassigned")

        add_save_button(window, "Save Changes" if editing else "Save Member",
                        lambda: self.save_member(window, member, name, phone, email, dob, gender, trainer))

    def save_member(self, window, member, name, phone, email, dob, gender, trainer):
        fields = {
            "name": name.get().strip(),
            "phone": phone.get().strip(),
            "email": email.get().strip(),
            "date_of_birth": dob.get().strip(),
            "gender": gender.get(),
            "trainer_id": choice_id(trainer.get()),
        }

        # check the format of email and names,... and save the data after



        window.destroy()
        self.refresh_table()

    # =========================
    # ASSIGN TRAINER
    # =========================

    def assign_trainer(self):
        member_id = selected_id(self.member_table)
        if not member_id:
            messagebox.showwarning("Assign Trainer", "Please select a member first.")
            return

        # get the trainer

        window = open_dialog(self.parent, "Assign Trainer", "450x300")
        dialog_title(window, "Assign Trainer")
        ctk.CTkLabel(window, text=f"Member: {member['name']} ({member_id})").pack()
        trainer = add_combo(window, "Trainer", trainer_choices(), trainer_choice_for(member.get("trainer_id")))

        def save():




       
            window.destroy()
            self.refresh_table()

        add_save_button(window, "Save", save)

    # =========================
    # DELETE
    # =========================

    def delete_member(self):
        member_id = selected_id(self.member_table)
        if not member_id:
            messagebox.showwarning("Delete Member", "Please select a member first.")
            return

        # remove the record and update the view




        
            self.refresh_table()
