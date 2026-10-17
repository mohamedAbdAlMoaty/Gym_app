import customtkinter as ctk

import storage

from views.common import page_title

from views.theme import (
    BG,
    SURFACE,
    SURFACE_2,
    BORDER,
    ACCENT,
    ACCENT_HOVER,
    CYAN,
    GREEN,
    AMBER,
    RED,
    TEXT,
    TEXT_2,
    MUTED,
    FONT,
)


class DashboardView:
    def __init__(self, parent):

        self.parent = parent

        self.show_dashboard()

    # =========================
    # DASHBOARD
    # =========================

    def show_dashboard(self):

        page_title(self.parent, "Dashboard")

        # =========================
        # TOP BAR
        # =========================

        top_bar = ctk.CTkFrame(self.parent, fg_color="transparent")

        top_bar.pack(fill="x", padx=34, pady=(0, 8))

        ctk.CTkLabel(
            top_bar,
            text="LIVE DATA",
            font=ctk.CTkFont(family=FONT, size=10, weight="bold"),
            text_color=GREEN,
        ).pack(side="left")

        ctk.CTkButton(
            top_bar,
            text="↻  Refresh",
            width=110,
            height=36,
            corner_radius=10,
            fg_color=SURFACE_2,
            hover_color=ACCENT,
            border_width=1,
            border_color=BORDER,
            font=ctk.CTkFont(family=FONT, size=12, weight="bold"),
            command=(self.refresh_dashboard),
        ).pack(side="right")

        # =========================
        # GET LIVE STATS
        # =========================

        stats = storage.dashboard_stats()

        # =========================
        # STAT CARDS
        # =========================

        cards_frame = ctk.CTkFrame(self.parent, fg_color="transparent")

        cards_frame.pack(fill="x", padx=26)

        cards = [
            ("Total Members", str(stats["total_members"]), "MEMBERS", ACCENT),
            ("Active Members", str(stats["active_members"]), "ACTIVE", GREEN),
            ("No Membership", str(stats["no_membership"]), "PENDING", AMBER),
            ("Total Trainers", str(stats["total_trainers"]), "COACHES", CYAN),
            ("Today's Attendance", str(stats["today_attendance"]), "TODAY", GREEN),
            (
                "Revenue This Month",
                storage.money(stats["monthly_revenue"]),
                "REVENUE",
                CYAN,
            ),
        ]

        for index, (title, value, badge, color) in enumerate(cards):
            row = index // 3

            column = index % 3

            self.create_card(cards_frame, title, value, badge, color, row, column)

        # =========================
        # LOWER AREA
        # =========================

        lower = ctk.CTkFrame(self.parent, fg_color="transparent")

        lower.pack(fill="both", expand=True, padx=34, pady=(14, 24))

        lower.grid_columnconfigure(0, weight=1)

        lower.grid_columnconfigure(1, weight=2)

        lower.grid_rowconfigure(0, weight=1)

        # =========================
        # MEMBERSHIP OVERVIEW
        # =========================

        overview = ctk.CTkFrame(
            lower,
            fg_color=SURFACE,
            corner_radius=16,
            border_width=1,
            border_color=BORDER,
        )

        overview.grid(row=0, column=0, padx=(0, 8), sticky="nsew")

        ctk.CTkLabel(
            overview,
            text="Membership Health",
            font=ctk.CTkFont(family=FONT, size=18, weight="bold"),
            text_color=TEXT,
        ).pack(anchor="w", padx=20, pady=(18, 2))

        ctk.CTkLabel(
            overview,
            text=("Current membership distribution"),
            font=ctk.CTkFont(family=FONT, size=11),
            text_color=MUTED,
        ).pack(anchor="w", padx=20, pady=(0, 15))

        # Active
        self.create_status_row(
            overview,
            "Active",
            stats["active_memberships"],
            GREEN,
        )

        # Upcoming
        self.create_status_row(
            overview,
            "Upcoming",
            stats["upcoming_memberships"],
            AMBER,
        )

        # Expired
        self.create_status_row(
            overview,
            "Expired",
            stats["expired_memberships"],
            RED,
        )

        # =========================
        # RECENT ACTIVITY
        # =========================

        activity_card = ctk.CTkFrame(
            lower,
            fg_color=SURFACE,
            corner_radius=16,
            border_width=1,
            border_color=BORDER,
        )

        activity_card.grid(row=0, column=1, padx=(8, 0), sticky="nsew")

        activity_card.grid_rowconfigure(1, weight=1)

        activity_card.grid_columnconfigure(0, weight=1)

        # -------------------------
        # Activity Header
        # -------------------------

        activity_header = ctk.CTkFrame(activity_card, fg_color="transparent")

        activity_header.grid(row=0, column=0, sticky="ew", padx=20, pady=(18, 8))

        ctk.CTkLabel(
            activity_header,
            text="Recent Activity",
            font=ctk.CTkFont(family=FONT, size=18, weight="bold"),
            text_color=TEXT,
        ).pack(side="left")

        ctk.CTkLabel(
            activity_header,
            text="Latest 10 events",
            font=ctk.CTkFont(family=FONT, size=10),
            text_color=MUTED,
        ).pack(side="right")

        # -------------------------
        # Scrollable Events
        # -------------------------

        events_frame = ctk.CTkScrollableFrame(
            activity_card,
            fg_color="transparent",
            corner_radius=0,
        )

        events_frame.grid(row=1, column=0, sticky="nsew", padx=12, pady=(0, 12))

        events = storage.recent_activity(limit=10)

        if events:
            for event in events:
                self.create_activity_row(events_frame, event)

        else:
            ctk.CTkLabel(
                events_frame,
                text="No activity yet.",
                font=ctk.CTkFont(family=FONT, size=12),
                text_color=MUTED,
            ).pack(pady=30)

    # =========================
    # MAIN STAT CARD
    # =========================

    def create_card(self, parent, title, value, badge, color, row, column):

        card = ctk.CTkFrame(
            parent,
            height=124,
            fg_color=SURFACE,
            corner_radius=16,
            border_width=1,
            border_color=BORDER,
        )

        card.grid(row=row, column=column, padx=8, pady=8, sticky="nsew")

        card.grid_propagate(False)

        parent.grid_columnconfigure(column, weight=1, uniform="dashboard_cards")

        # Colored line
        accent = ctk.CTkFrame(
            card,
            width=4,
            corner_radius=4,
            fg_color=color,
        )

        accent.pack(side="left", fill="y", padx=(0, 14), pady=14)

        content = ctk.CTkFrame(card, fg_color="transparent")

        content.pack(side="left", fill="both", expand=True, pady=14)

        top = ctk.CTkFrame(content, fg_color="transparent")

        top.pack(fill="x")

        ctk.CTkLabel(
            top,
            text=title,
            font=ctk.CTkFont(family=FONT, size=12, weight="bold"),
            text_color=MUTED,
        ).pack(side="left")

        # Small badge
        ctk.CTkLabel(
            top,
            text=badge,
            font=ctk.CTkFont(family=FONT, size=9, weight="bold"),
            text_color=color,
        ).pack(side="right", padx=14)

        # Value
        ctk.CTkLabel(
            content,
            text=value,
            font=ctk.CTkFont(family=FONT, size=27, weight="bold"),
            text_color=TEXT,
        ).pack(anchor="w", pady=(12, 0))

    # =========================
    # MEMBERSHIP STATUS ROW
    # =========================

    def create_status_row(self, parent, title, value, color):

        row = ctk.CTkFrame(
            parent,
            fg_color=SURFACE_2,
            corner_radius=12,
            height=58,
        )

        row.pack(fill="x", padx=18, pady=6)

        row.pack_propagate(False)

        # Status Dot
        dot = ctk.CTkFrame(
            row,
            width=10,
            height=10,
            corner_radius=5,
            fg_color=color,
        )

        dot.pack(side="left", padx=(16, 10))

        ctk.CTkLabel(
            row,
            text=title,
            font=ctk.CTkFont(family=FONT, size=12, weight="bold"),
            text_color=TEXT_2,
        ).pack(side="left")

        ctk.CTkLabel(
            row,
            text=str(value),
            font=ctk.CTkFont(family=FONT, size=18, weight="bold"),
            text_color=color,
        ).pack(side="right", padx=16)

    # =========================
    # ACTIVITY ROW
    # =========================

    def create_activity_row(self, parent, event):

        row = ctk.CTkFrame(
            parent,
            fg_color=SURFACE_2,
            corner_radius=10,
        )

        row.pack(fill="x", pady=4)

        # Accent line
        ctk.CTkFrame(
            row,
            width=4,
            height=36,
            corner_radius=3,
            fg_color=ACCENT,
        ).pack(side="left", padx=(10, 10), pady=8)

        ctk.CTkLabel(
            row,
            text=event,
            anchor="w",
            justify="left",
            font=ctk.CTkFont(family=FONT, size=11),
            text_color=TEXT_2,
        ).pack(side="left", fill="x", expand=True, padx=(0, 12), pady=10)

    # =========================
    # REFRESH
    # =========================

    def refresh_dashboard(self):

        for widget in self.parent.winfo_children():
            widget.destroy()

        self.show_dashboard()
