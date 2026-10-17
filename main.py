import customtkinter as ctk

from views.dashboard_view import DashboardView
from views.members_view import MembersView
from views.trainers_view import TrainersView
from views.memberships_view import MembershipsView
from views.payments_view import PaymentsView
from views.attendance_view import AttendanceView

from views.theme import (
    BG,
    SIDEBAR,
    SURFACE_2,
    ACCENT,
    ACCENT_HOVER,
    TEXT,
    MUTED,
    FONT,
)


class GymApp(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("GymFlow | Gym Management System")

        self.geometry("1360x820")

        self.minsize(1120, 680)

        ctk.set_appearance_mode("dark")

        ctk.set_default_color_theme("dark-blue")

        self.configure(fg_color=BG)

        # Store sidebar buttons
        self.nav_buttons = {}

        # Current page
        self.active_page = None

        self.create_sidebar()

        self.create_main_area()

        self.show_dashboard()

    # =========================
    # SIDEBAR
    # =========================

    def create_sidebar(self):

        self.sidebar = ctk.CTkFrame(
            self,
            width=250,
            corner_radius=0,
            fg_color=SIDEBAR,
        )

        self.sidebar.pack(side="left", fill="y")

        self.sidebar.pack_propagate(False)

        # =========================
        # BRAND
        # =========================

        brand = ctk.CTkFrame(self.sidebar, fg_color="transparent")

        brand.pack(fill="x", padx=22, pady=(26, 30))

        # Logo square
        logo = ctk.CTkFrame(
            brand,
            width=46,
            height=46,
            corner_radius=14,
            fg_color=ACCENT,
        )

        logo.pack(side="left")

        logo.pack_propagate(False)

        ctk.CTkLabel(
            logo,
            text="GF",
            font=ctk.CTkFont(family=FONT, size=17, weight="bold"),
            text_color="white",
        ).place(relx=0.5, rely=0.5, anchor="center")

        # Brand text
        brand_text = ctk.CTkFrame(brand, fg_color="transparent")

        brand_text.pack(side="left", padx=(12, 0))

        ctk.CTkLabel(
            brand_text,
            text="GYMFLOW",
            font=ctk.CTkFont(family=FONT, size=21, weight="bold"),
            text_color=TEXT,
        ).pack(anchor="w")

        ctk.CTkLabel(
            brand_text,
            text="Management Suite",
            font=ctk.CTkFont(family=FONT, size=11),
            text_color=MUTED,
        ).pack(anchor="w")

        # =========================
        # WORKSPACE LABEL
        # =========================

        ctk.CTkLabel(
            self.sidebar,
            text="WORKSPACE",
            font=ctk.CTkFont(family=FONT, size=10, weight="bold"),
            text_color=MUTED,
        ).pack(anchor="w", padx=26, pady=(0, 9))

        # =========================
        # SIDEBAR BUTTONS
        # =========================

        buttons = [
            ("dashboard", "▦   Dashboard", self.show_dashboard),
            ("members", "●   Members", self.show_members),
            ("trainers", "◆   Trainers", self.show_trainers),
            ("memberships", "▤   Memberships", self.show_memberships),
            ("payments", "€   Payments", self.show_payments),
            ("attendance", "✓   Attendance", self.show_attendance),
        ]

        for key, text, command in buttons:
            button = ctk.CTkButton(
                self.sidebar,
                text=text,
                command=command,
                height=46,
                corner_radius=12,
                anchor="w",
                font=ctk.CTkFont(family=FONT, size=14, weight="bold"),
                fg_color="transparent",
                hover_color=SURFACE_2,
                text_color=MUTED,
                border_width=0,
            )

            button.pack(fill="x", padx=16, pady=4)

            self.nav_buttons[key] = button

    # =========================
    # MAIN AREA
    # =========================

    def create_main_area(self):

        self.main_frame = ctk.CTkFrame(
            self,
            corner_radius=0,
            fg_color=BG,
        )

        self.main_frame.pack(side="right", fill="both", expand=True)

    # =========================
    # CLEAR CURRENT PAGE
    # =========================

    def clear_main(self):

        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # =========================
    # ACTIVE SIDEBAR BUTTON
    # =========================

    def set_active_page(self, key):

        self.active_page = key

        for name, button in self.nav_buttons.items():
            if name == key:
                button.configure(
                    fg_color=ACCENT,
                    hover_color=ACCENT_HOVER,
                    text_color="white",
                )

            else:
                button.configure(
                    fg_color="transparent",
                    hover_color=SURFACE_2,
                    text_color=MUTED,
                )

    # =========================
    # VIEWS
    # =========================

    def show_dashboard(self):

        self.clear_main()

        self.set_active_page("dashboard")

        DashboardView(self.main_frame)

    def show_members(self):

        self.clear_main()

        self.set_active_page("members")

        MembersView(self.main_frame)

    def show_trainers(self):

        self.clear_main()

        self.set_active_page("trainers")

        TrainersView(self.main_frame)

    def show_memberships(self):

        self.clear_main()

        self.set_active_page("memberships")

        MembershipsView(self.main_frame)

    def show_payments(self):

        self.clear_main()

        self.set_active_page("payments")

        PaymentsView(self.main_frame)

    def show_attendance(self):

        self.clear_main()

        self.set_active_page("attendance")

        AttendanceView(self.main_frame)


if __name__ == "__main__":
    app = GymApp()

    app.mainloop()
