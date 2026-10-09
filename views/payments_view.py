import customtkinter as ctk
from tkinter import messagebox
from data_storage import Json_manager

import storage
from views.common import (page_title, toolbar, create_table, fill_table,
                          open_dialog, dialog_title, add_entry, add_combo, add_save_button,
                          member_choices, choice_id)


class PaymentsView:

    PLANS = {
    "Monthly": {"months": 1, "price": 50.0},
    "3 Months": {"months": 3, "price": 120.0},
    "6 Months": {"months": 6, "price": 250.0},
    }

    PAYMENT_METHODS = ["Cash", "Card", "Bank Transfer"]

    def __init__(self, parent):
        self.parent = parent
        self.show_payments()

    def show_payments(self):
        page_title(self.parent, "Payments")

        bar = toolbar(self.parent)

        self.search_entry = ctk.CTkEntry(bar, placeholder_text="Search by member name or ID", width=280)
        self.search_entry.pack(side="left", padx=(0, 10))
        self.search_entry.bind("<KeyRelease>", lambda e: self.refresh_table())

        self.method_filter = ctk.CTkComboBox(bar, values=["All methods"] + storage.PAYMENT_METHODS, width=150,
                                             state="readonly", command=lambda _: self.refresh_table())
        self.method_filter.set("All methods")
        self.method_filter.pack(side="left")

        ctk.CTkButton(bar, text="+ Record Payment", command=self.record_payment).pack(side="right")

        self.table = create_table(
            self.parent, ["Payment ID", "Member ID", "Member", "Membership ID", "Amount", "Date", "Method"],
            widths=[90, 90, 150, 110, 90, 110, 120])

        self.total_label = ctk.CTkLabel(self.parent, text="", font=ctk.CTkFont(size=16, weight="bold"))
        self.total_label.pack(anchor="e", padx=30, pady=(0, 15))

        self.refresh_table()

    def refresh_table(self):
        text = self.search_entry.get().strip().lower()
        method = self.method_filter.get()






        
        fill_table(self.table, )
        self.total_label.configure(text=f"Total: {storage.money(total)}")

    # =========================
    # RECORD PAYMENT
    # =========================

    def record_payment(self):
        json_manager = Json_manager()
        if not json_manager.read_from_json_file("memberships"):
            messagebox.showwarning("Record Payment", "Create a membership first.")
            return

        window = open_dialog(self.parent, "Record Payment", "450x640")
        dialog_title(window, "Record Payment")

        def membership_values(member_choice):
            owned = storage.member_memberships(choice_id(member_choice))
            owned.sort(key=lambda m: m["end_date"], reverse=True)
            return [f"{m['membership_id']} - {m['plan']} (until {m['end_date']})" for m in owned]

        def on_member_change(choice):
            values = membership_values(choice)
            membership.configure(values=values or ["No memberships"])
            membership.set(values[0] if values else "No memberships")
            on_membership_change(membership.get())

        def on_membership_change(choice):
            plan = next((m["plan"] for m in Json_manager().read_from_json_file("memberships")
                         if m["membership_id"] == choice_id(choice)), None)
            amount.delete(0, "end")
            if plan:
                amount.insert(0, "50 Euro")

        members = Json_manager().member_choices()
        member = add_combo(window, "Member", members, command=on_member_change)
        membership = add_combo(window, "Membership", membership_values(members[0]) or ["No memberships"],
                               command=on_membership_change)
        amount = add_entry(window, "Amount (€)")
        pay_date = add_entry(window, "Payment Date (YYYY-MM-DD)", "2026-10-10")
        method = add_combo(window, "Payment Method", self.PAYMENT_METHODS)
        on_membership_change(membership.get())

        def save():
            membership_id = choice_id(membership.get())
            if membership_id == "No":
                messagebox.showerror("Validation Error", "This member has no membership yet.", parent=window)
                return

            # Complete




       
            window.destroy()

            self.refresh_table()

        add_save_button(window, "Save Payment", save)
