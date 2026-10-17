import customtkinter as ctk

import storage

from views.common import page_title


class DashboardView:
    def __init__(self, parent):

        self.parent = parent

        self.show_dashboard()

    # =========================
    # DASHBOARD
    # =========================

    def show_dashboard(self):

        page_title(self.parent, "Dashboard")

        # -------------------------
        # Toolbar
        # -------------------------

        top_bar = ctk.CTkFrame(self.parent, fg_color="transparent")

        top_bar.pack(fill="x", padx=30, pady=(0, 5))

        ctk.CTkButton(
            top_bar, text="Refresh", width=100, command=self.refresh_dashboard
        ).pack(side="right")

        # -------------------------
        # Statistics
        # -------------------------

        stats = storage.dashboard_stats()

        cards_frame = ctk.CTkFrame(self.parent, fg_color="transparent")

        cards_frame.pack(fill="x", padx=30)

        cards = [
            ("Total Members", str(stats["total_members"])),
            ("Active Members", str(stats["active_members"])),
            ("No Membership", str(stats["no_membership"])),
            ("Total Trainers", str(stats["total_trainers"])),
            ("Today's Attendance", str(stats["today_attendance"])),
            ("Revenue This Month", storage.money(stats["monthly_revenue"])),
        ]

        # -------------------------
        # Cards - 2 rows x 3
        # -------------------------

        for index, (title, value) in enumerate(cards):
            row = index // 3
            column = index % 3

            self.create_card(cards_frame, title, value, row, column)

        # =========================
        # MEMBERSHIP OVERVIEW
        # =========================

        overview_frame = ctk.CTkFrame(self.parent)

        overview_frame.pack(fill="x", padx=30, pady=(20, 10))

        ctk.CTkLabel(
            overview_frame,
            text="Membership Overview",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(anchor="w", padx=20, pady=(15, 10))

        membership_stats = ctk.CTkFrame(overview_frame, fg_color="transparent")

        membership_stats.pack(fill="x", padx=20, pady=(0, 15))

        self.create_small_stat(
            membership_stats, "Active", stats["active_memberships"], 0
        )

        self.create_small_stat(
            membership_stats, "Upcoming", stats["upcoming_memberships"], 1
        )

        self.create_small_stat(
            membership_stats, "Expired", stats["expired_memberships"], 2
        )

        # =========================
        # RECENT ACTIVITY
        # =========================

        ctk.CTkLabel(
            self.parent,
            text="Recent Activity",
            font=ctk.CTkFont(size=20, weight="bold"),
        ).pack(anchor="w", padx=30, pady=(20, 10))

        activity = ctk.CTkTextbox(self.parent, height=180)

        activity.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        events = storage.recent_activity(limit=10)

        if events:
            activity.insert("1.0", "\n".join(f"• {event}" for event in events))

        else:
            activity.insert("1.0", "No activity yet.")

        activity.configure(state="disabled")

    # =========================
    # MAIN CARD
    # =========================

    def create_card(self, parent, title, value, row, column):

        card = ctk.CTkFrame(parent, height=110)

        card.grid(row=row, column=column, padx=8, pady=8, sticky="nsew")

        parent.grid_columnconfigure(column, weight=1, uniform="cards")

        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=14)).pack(
            pady=(18, 5), padx=10
        )

        ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=26, weight="bold")).pack(
            pady=(0, 15)
        )

    # =========================
    # SMALL MEMBERSHIP STAT
    # =========================

    def create_small_stat(self, parent, title, value, column):

        frame = ctk.CTkFrame(parent)

        frame.grid(row=0, column=column, padx=8, sticky="nsew")

        parent.grid_columnconfigure(column, weight=1, uniform="membership_stats")

        ctk.CTkLabel(frame, text=title).pack(pady=(12, 3))

        ctk.CTkLabel(
            frame, text=str(value), font=ctk.CTkFont(size=22, weight="bold")
        ).pack(pady=(0, 12))

    # =========================
    # REFRESH
    # =========================

    def refresh_dashboard(self):

        for widget in self.parent.winfo_children():
            widget.destroy()

        self.show_dashboard()
