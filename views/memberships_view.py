import customtkinter as ctk
from tkinter import messagebox
from data_storage import Json_manager

from views.common import (page_title, toolbar, create_table, fill_table, selected_id,
                          open_dialog, dialog_title, add_entry, add_combo, add_save_button,
                          member_choices, plan_choices, choice_id)


class MembershipsView:

    PLANS = {
        "Monthly": {"months": 1, "price": 50.0},
        "3 Months": {"months": 3, "price": 120.0},
        "6 Months": {"months": 6, "price": 250.0},
        }
    PAYMENT_METHODS = ["Cash", "Card", "Bank Transfer"]

    def __init__(self, parent):
        self.parent = parent
        self.show_memberships()

    def show_memberships(self):
        page_title(self.parent, "Memberships")

        bar = toolbar(self.parent)

        self.search_entry = ctk.CTkEntry(bar, placeholder_text="Search by member name or ID", width=280)
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_table())

        ctk.CTkButton(bar, text="Search", command=self.refresh_table).pack(side="left")

        self.status_filter = ctk.CTkComboBox(bar, values=["All", "Active", "Expired"], width=130,
                                             state="readonly", command=lambda _: self.refresh_table())
        self.status_filter.set("All")
        self.status_filter.pack(side="left", padx=10)

        ctk.CTkButton(bar, text="Renew Selected", command=self.renew_membership).pack(side="right", padx=(10, 0))
        ctk.CTkButton(bar, text="+ New Membership", command=self.new_membership).pack(side="right")

        self.table = create_table(
            self.parent, ["ID", "Member ID", "Member", "Type", "Start Date", "End Date", "Status"],
            widths=[80, 90, 150, 100, 110, 110, 90])
        self.refresh_table()

    def refresh_table(self):
        text = self.search_entry.get().strip().lower()
        wanted = self.status_filter.get()

        # load the data






       
        fill_table(self.table, )

    # =========================
    # NEW / RENEW
    # =========================

    def new_membership(self):

    #    make sure in the json storge there is a otherwise show
            # messagebox.showwarning("New Membership", "Add a member first.")



         
        self.membership_form("New Membership")

    def renew_membership(self):
        membership_id = selected_id(self.table)
        if not membership_id:
            messagebox.showwarning("Renew Membership", "Please select a membership first.")
            return
        # get the selected member and get their values from storage and send them to form




        self.membership_form("Renew Membership", "M001", "Monthly")

    def membership_form(self, title, member_id=None, plan=None):
        renewing = member_id is not None
        window = open_dialog(self.parent, title, "450x600")
        dialog_title(window, title)

        member_values =Json_manager().member_names() 
        member = add_combo(window, "Member", member_values)

        plan_values =[f"{plan} - €{info['price']:.0f}" for plan, info in self.PLANS.items()]
        default_plan = next((p for p in plan_values if plan and p.startswith(plan + " - ")), None)
        plan_combo = add_combo(window, "Membership Type", plan_values, default_plan)

        start = add_entry(window, "Start Date (YYYY-MM-DD)","2026-11-11")
        method = add_combo(window, "Payment Method", self.PAYMENT_METHODS)

        ctk.CTkLabel(window, text="The payment is recorded automatically.",
                     text_color="gray").pack(pady=(12, 0))

        def save():





  
            # create_membership(selected_member, plan_name, start_date, method.get())

            window.destroy()
            self.refresh_table()

        add_save_button(window, "Save", save)


def create_membership(member_id, plan, start, method, amount=None):
    # put the data in storage
    pass      
  

def choice_id_plan(choice):
    """'3 Months - €120' -> '3 Months'."""
    return choice.split(" - ")[0]
