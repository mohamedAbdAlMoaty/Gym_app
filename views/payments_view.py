import customtkinter as ctk
from tkinter import messagebox

import storage

from data_storage import Json_manager

from views.common import (
    page_title,
    toolbar,
    create_table,
    fill_table,
    open_dialog,
    dialog_title,
    add_entry,
    add_combo,
    add_save_button,
    member_choices,
    choice_id,
)


class PaymentsView:
    def __init__(self, parent):
        self.parent = parent
        self.show_payments()

    # =========================
    # PAGE
    # =========================

    def show_payments(self):

        page_title(self.parent, "Payments")

        bar = toolbar(self.parent)

        self.search_entry = ctk.CTkEntry(
            bar,
            placeholder_text=("Search by member name or ID"),
            width=280,
        )

        self.search_entry.pack(side="left", padx=(0, 10))

        self.search_entry.bind("<KeyRelease>", lambda event: self.refresh_table())

        self.method_filter = ctk.CTkComboBox(
            bar,
            values=["All methods", *storage.PAYMENT_METHODS],
            width=150,
            state="readonly",
            command=lambda _: self.refresh_table(),
        )

        self.method_filter.set("All methods")

        self.method_filter.pack(side="left")

        ctk.CTkButton(
            bar,
            text="+ Record Payment",
            command=self.record_payment,
        ).pack(side="right")

        self.table = create_table(
            self.parent,
            [
                "Payment ID",
                "Member ID",
                "Member",
                "Membership ID",
                "Amount",
                "Date",
                "Method",
            ],
            widths=[
                90,
                90,
                150,
                110,
                90,
                110,
                120,
            ],
        )

        self.total_label = ctk.CTkLabel(
            self.parent,
            text="",
            font=ctk.CTkFont(size=16, weight="bold"),
        )

        self.total_label.pack(
            anchor="e",
            padx=30,
            pady=(0, 15),
        )

        self.refresh_table()

    # =========================
    # TABLE
    # =========================

    def refresh_table(self):

        text = self.search_entry.get().strip().lower()

        selected_method = self.method_filter.get()

        rows = []

        total = 0.0

        payments = Json_manager().All_payments()

        for payment in payments:
            member_name = storage.member_name(payment.member_id)

            searchable_text = (
                f"{payment.payment_id} {payment.member_id} {member_name}"
            ).lower()

            if text and text not in searchable_text:
                continue

            if (
                selected_method != "All methods"
                and payment.payment_method != selected_method
            ):
                continue

            rows.append(
                (
                    payment.payment_id,
                    payment.member_id,
                    member_name,
                    payment.membership_id,
                    storage.money(payment.amount),
                    payment.payment_date,
                    payment.payment_method,
                )
            )

            total += payment.amount

        fill_table(self.table, rows)

        self.total_label.configure(text=(f"Total: {storage.money(total)}"))

    # =========================
    # RECORD PAYMENT
    # =========================

    def record_payment(self):

        members = member_choices()

        if not members:
            messagebox.showwarning("Record Payment", "Add a member first.")
            return

        memberships = storage.load("memberships")

        if not memberships:
            messagebox.showwarning("Record Payment", "Create a membership first.")
            return

        window = open_dialog(self.parent, "Record Payment", "450x640")

        dialog_title(window, "Record Payment")

        # -------------------------
        # Memberships for member
        # -------------------------

        def membership_values(member_choice):

            member_id = choice_id(member_choice)

            owned = storage.member_memberships(member_id)

            owned.sort(
                key=lambda item: item["end_date"],
                reverse=True,
            )

            return [
                (f"{item['membership_id']} - {item['plan']} (until {item['end_date']})")
                for item in owned
            ]

        # -------------------------
        # Membership changed
        # -------------------------

        def on_membership_change(choice):

            membership_id = choice_id(choice)

            selected = next(
                (
                    item
                    for item in storage.load("memberships")
                    if (item["membership_id"] == membership_id)
                ),
                None,
            )

            amount.delete(0, "end")

            if selected:
                plan = selected["plan"]

                price = storage.PLANS[plan]["price"]

                amount.insert(0, str(price))

        # -------------------------
        # Member changed
        # -------------------------

        def on_member_change(choice):

            values = membership_values(choice)

            if values:
                membership.configure(values=values)

                membership.set(values[0])

            else:
                membership.configure(values=["No memberships"])

                membership.set("No memberships")

            on_membership_change(membership.get())

        # -------------------------
        # Fields
        # -------------------------

        member = add_combo(
            window,
            "Member",
            members,
            command=on_member_change,
        )

        initial_memberships = membership_values(members[0])

        membership = add_combo(
            window,
            "Membership",
            (initial_memberships or ["No memberships"]),
            command=on_membership_change,
        )

        amount = add_entry(window, "Amount (€)")

        pay_date = add_entry(
            window,
            "Payment Date (YYYY-MM-DD)",
            storage.today_str(),
        )

        method = add_combo(
            window,
            "Payment Method",
            storage.PAYMENT_METHODS,
        )

        on_membership_change(membership.get())

        # =========================
        # SAVE
        # =========================

        def save():

            member_id = choice_id(member.get())

            if membership.get() == "No memberships":
                messagebox.showerror(
                    "Validation Error",
                    ("This member has no membership yet."),
                    parent=window,
                )
                return

            membership_id = choice_id(membership.get())

            # Amount
            try:
                payment_amount = float(amount.get().strip())

            except ValueError:
                messagebox.showerror(
                    "Validation Error",
                    ("Amount must be a valid number."),
                    parent=window,
                )
                return

            # Date
            payment_date = pay_date.get().strip()

            if storage.parse_date(payment_date) is None:
                messagebox.showerror(
                    "Validation Error",
                    ("Payment date must use YYYY-MM-DD."),
                    parent=window,
                )
                return

            try:
                payment = storage.add_payment(
                    member_id=member_id,
                    membership_id=membership_id,
                    amount=payment_amount,
                    payment_date=payment_date,
                    method=method.get(),
                )

            except ValueError as error:
                messagebox.showerror(
                    "Validation Error",
                    str(error),
                    parent=window,
                )

                return

            messagebox.showinfo(
                "Payment Saved",
                (f"Payment {payment.payment_id} saved successfully."),
                parent=window,
            )

            window.destroy()

            self.refresh_table()

        add_save_button(window, "Save Payment", save)
