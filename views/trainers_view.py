import customtkinter as ctk
from tkinter import messagebox

import storage

from data_storage import Json_manager
from models.trainer import Trainer

from views.common import (
    page_title,
    toolbar,
    create_table,
    fill_table,
    open_dialog,
    dialog_title,
    add_entry,
    add_save_button,
)


class TrainersView:
    def __init__(self, parent):
        self.parent = parent
        self.show_trainers()

    def show_trainers(self):
        page_title(self.parent, "Trainers")

        bar = toolbar(self.parent)
        ctk.CTkButton(bar, text="+ Add Trainer", command=self.add_trainer).pack(
            side="right"
        )

        self.table = create_table(
            self.parent,
            ["ID", "Name", "Phone", "Email", "Specialization", "Members"],
            widths=[80, 160, 120, 220, 150, 90],
        )
        self.refresh_table()

    def refresh_table(self):

        rows = []

        members = storage.load("members")

        for trainer in Json_manager().All_trainers():
            members_count = sum(
                1
                for member in members
                if member.get("trainer_id") == trainer.trainer_id
            )

            rows.append(
                (
                    trainer.trainer_id,
                    trainer.name,
                    trainer.phone,
                    trainer.email,
                    trainer.specialization,
                    members_count,
                )
            )

        fill_table(self.table, rows)

    def add_trainer(self):
        window = open_dialog(self.parent, "Add Trainer", "450x520")
        dialog_title(window, "Add New Trainer")

        name_entry = add_entry(window, "Name")
        phone_entry = add_entry(window, "Phone")
        email_entry = add_entry(window, "Email")
        specialization_entry = add_entry(window, "Specialization (e.g. Yoga)")

        def save():

            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            email = email_entry.get().strip()
            specialization = specialization_entry.get().strip()

            if not name:
                messagebox.showerror("Error", "Name is required", parent=window)
                return

            if not phone:
                messagebox.showerror("Error", "Phone is required", parent=window)
                return

            if not email:
                messagebox.showerror("Error", "Email is required", parent=window)
                return

            if not specialization:
                messagebox.showerror(
                    "Error", "Specialization is required", parent=window
                )
                return

            trainer_id = storage.next_id("trainers", "trainer_id", "T")

            trainer = Trainer(trainer_id, name, phone, email, specialization)

            trainers = storage.load("trainers")

            trainers.append(trainer.to_dict())

            storage.save("trainers", trainers)

            messagebox.showinfo(
                "Success", f"Trainer {trainer.name} added successfully", parent=window
            )

            window.destroy()

            self.refresh_table()

        add_save_button(window, "Save Trainer", save)
