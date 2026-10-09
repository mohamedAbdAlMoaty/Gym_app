import customtkinter as ctk
from tkinter import messagebox

from views.common import (page_title, toolbar, create_table, fill_table,
                          open_dialog, dialog_title, add_entry, add_save_button)


class TrainersView:

    def __init__(self, parent):
        self.parent = parent
        self.show_trainers()

    def show_trainers(self):
        page_title(self.parent, "Trainers")

        bar = toolbar(self.parent)
        ctk.CTkButton(bar, text="+ Add Trainer", command=self.add_trainer).pack(side="right")

        self.table = create_table(
            self.parent, ["ID", "Name", "Phone", "Email", "Specialization", "Members"],
            widths=[80, 160, 120, 220, 150, 90])
        self.refresh_table()

    def refresh_table(self):
        # check the storage of trainers and load the data and then pass this to fill_table()
        





        fill_table(self.table, )

    def add_trainer(self):
        window = open_dialog(self.parent, "Add Trainer", "450x520")
        dialog_title(window, "Add New Trainer")

        name_entry = add_entry(window, "Name")
        phone_entry = add_entry(window, "Phone")
        email_enty = add_entry(window, "Email")
        specialization_entry = add_entry(window, "Specialization (e.g. Yoga)")

        def save():
            
            name = name_entry.get().strip()
            phone = phone_entry.get().strip()
            email = email_enty.get().strip()
            specialization =  specialization_entry.get().strip()

            # append data in the json trainer


         

            window.destroy()
            # messagebox.showinfo("Success", f"Trainer {name} added {'trainer_id'}")
            self.refresh_table()

        add_save_button(window, "Save Trainer", save)
