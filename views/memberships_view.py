import customtkinter as ctk
from tkinter import messagebox

import storage

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
    member_choices,
    plan_choices,
    choice_id,
)


STATUS_FILTERS = [
    "All",
    "Active",
    "Upcoming",
    "Expired",
]


class MembershipsView:
    def __init__(self, parent):
        self.parent = parent
        self.show_memberships()

    # =========================
    # PAGE
    # =========================

    def show_memberships(self):

        page_title(self.parent, "Memberships")

        bar = toolbar(self.parent)

        self.search_entry = ctk.CTkEntry(
            bar,
            placeholder_text=("Search by member name, member ID or membership ID"),
            width=300,
        )

        self.search_entry.pack(side="left", padx=(0, 10))

        self.search_entry.bind("<KeyRelease>", lambda event: self.refresh_table())

        self.status_filter = ctk.CTkComboBox(
            bar,
            values=STATUS_FILTERS,
            width=140,
            state="readonly",
            command=lambda _: self.refresh_table(),
        )

        self.status_filter.set("All")

        self.status_filter.pack(side="left", padx=10)

        ctk.CTkButton(
            bar,
            text="Renew Selected",
            command=self.renew_membership,
        ).pack(side="right", padx=(10, 0))

        ctk.CTkButton(
            bar,
            text="+ New Membership",
            command=self.new_membership,
        ).pack(side="right")

        self.table = create_table(
            self.parent,
            [
                "ID",
                "Member ID",
                "Member",
                "Type",
                "Start Date",
                "End Date",
                "Status",
            ],
            widths=[
                80,
                90,
                150,
                110,
                110,
                110,
                100,
            ],
        )

        self.refresh_table()

    # =========================
    # TABLE
    # =========================

    def refresh_table(self):

        text = self.search_entry.get().strip().lower()

        wanted = self.status_filter.get()

        rows = []

        try:
            memberships = Json_manager().All_memberships()

        except Exception as error:
            messagebox.showerror(
                "Memberships Error",
                (f"Could not load memberships:\n{error}"),
            )

            return

        for membership in memberships:
            member_name = storage.member_name(membership.member_id)

            status = membership.status

            searchable = (
                f"{membership.membership_id} "
                f"{membership.member_id} "
                f"{member_name} "
                f"{membership.plan}"
            ).lower()

            if text and text not in searchable:
                continue

            if wanted != "All" and status != wanted:
                continue

            rows.append(
                (
                    membership.membership_id,
                    membership.member_id,
                    member_name,
                    membership.plan,
                    membership.start_date,
                    membership.end_date,
                    status,
                )
            )

        fill_table(self.table, rows)

    # =========================
    # NEW
    # =========================

    def new_membership(self):

        members = member_choices()

        if not members:
            messagebox.showwarning("New Membership", "Add a member first.")

            return

        self.membership_form("New Membership")

    # =========================
    # RENEW
    # =========================

    def renew_membership(self):

        membership_id = selected_id(self.table)

        if not membership_id:
            messagebox.showwarning(
                "Renew Membership",
                ("Please select a membership first."),
            )

            return

        membership = storage.get_membership(membership_id)

        if not membership:
            messagebox.showerror("Renew Membership", "Membership not found.")

            return

        if not storage.get_member(membership["member_id"]):
            messagebox.showerror(
                "Renew Membership",
                ("The member linked to this membership no longer exists."),
            )

            return

        self.membership_form("Renew Membership", membership)

    # =========================
    # FORM
    # =========================

    def membership_form(self, title, existing=None):

        renewing = existing is not None

        window = open_dialog(self.parent, title, "450x600")

        dialog_title(window, title)

        # -------------------------
        # MEMBER
        # -------------------------

        if renewing:
            member = storage.get_member(existing["member_id"])

            member_values = [(f"{member['member_id']} - {member['name']}")]

            default_member = member_values[0]

        else:
            member_values = member_choices()

            default_member = None

        member_combo = add_combo(
            window,
            "Member",
            member_values,
            default_member,
        )

        # -------------------------
        # PLAN
        # -------------------------

        plans = plan_choices()

        default_plan = None

        if renewing:
            default_plan = next(
                (
                    value
                    for value in plans
                    if value.startswith(existing["plan"] + " - ")
                ),
                None,
            )

        plan_combo = add_combo(
            window,
            "Membership Type",
            plans,
            default_plan,
        )

        # -------------------------
        # START DATE
        # -------------------------

        if renewing:
            default_start = storage.renewal_start(existing["member_id"]).strftime(
                storage.DATE_FORMAT
            )

        else:
            default_start = storage.today_str()

        start_entry = add_entry(
            window,
            "Start Date (YYYY-MM-DD)",
            default_start,
        )

        # -------------------------
        # PAYMENT METHOD
        # -------------------------

        method_combo = add_combo(
            window,
            "Payment Method",
            storage.PAYMENT_METHODS,
        )

        ctk.CTkLabel(
            window,
            text=("The payment is recorded automatically."),
            text_color="gray",
        ).pack(pady=(12, 0))

        # =========================
        # SAVE
        # =========================

        def save():

            member_id = choice_id(member_combo.get())

            plan = self.plan_name(plan_combo.get())

            start_date = storage.parse_date(start_entry.get().strip())

            if not member_id:
                messagebox.showerror(
                    "Validation Error",
                    "Please select a member.",
                    parent=window,
                )

                return

            if plan not in storage.PLANS:
                messagebox.showerror(
                    "Validation Error",
                    "Invalid membership plan.",
                    parent=window,
                )

                return

            if start_date is None:
                messagebox.showerror(
                    "Validation Error",
                    ("Start date must use YYYY-MM-DD."),
                    parent=window,
                )

                return

            try:
                membership, payment = storage.create_membership(
                    member_id=member_id,
                    plan=plan,
                    start=start_date,
                    method=method_combo.get(),
                )

            except ValueError as error:
                messagebox.showerror(
                    "Validation Error",
                    str(error),
                    parent=window,
                )

                return

            except Exception as error:
                messagebox.showerror(
                    "Membership Error",
                    str(error),
                    parent=window,
                )

                return

            messagebox.showinfo(
                "Membership Saved",
                (
                    f"Membership "
                    f"{membership.membership_id} "
                    f"saved successfully.\n\n"
                    f"End date: "
                    f"{membership.end_date}\n"
                    f"Payment: "
                    f"{payment.payment_id}"
                ),
                parent=window,
            )

            window.destroy()

            self.refresh_table()

        add_save_button(
            window,
            ("Renew Membership" if renewing else "Save Membership"),
            save,
        )

    # =========================
    # HELPERS
    # =========================

    @staticmethod
    def plan_name(choice):

        return choice.split(" - ")[0]
