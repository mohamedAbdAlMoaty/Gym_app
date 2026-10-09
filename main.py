import customtkinter as ctk

from views.dashboard_view import DashboardView
from views.members_view import MembersView
from views.trainers_view import TrainersView
from views.memberships_view import MembershipsView
from views.payments_view import PaymentsView
from views.attendance_view import AttendanceView


class GymApp(ctk.CTk):

    def __init__(self):
        super().__init__()

        self.title("Gym Management System")
        self.geometry("1200x700")
        self.minsize(1000, 600)

        ctk.set_appearance_mode("light")
        ctk.set_default_color_theme("blue")

        self.create_sidebar()
        self.create_main_area()

        self.show_dashboard()

    # =========================
    # SIDEBAR
    # =========================

    def create_sidebar(self):

        # create a container that I can put other widgets on it like buttons
        self.sidebar = ctk.CTkFrame(self,width=220,corner_radius=0)

        self.sidebar.pack(side="left",fill="y")

        title = ctk.CTkLabel(self.sidebar,text="GYM MANAGEMENT",font=ctk.CTkFont(size=20,weight="bold"))

        title.pack(pady=(30, 40))

        buttons = [
            ("Dashboard", self.show_dashboard),
            ("Members", self.show_members),
            ("Trainers", self.show_trainers),
            ("Memberships", self.show_memberships),
            ("Payments", self.show_payments),
            ("Attendance", self.show_attendance)
        ]

        for text, command in buttons:

            # create buttons on the container that have been created (sidebar) thats why sidebar became the parent
            button = ctk.CTkButton(self.sidebar,text=text,command=command,height=40)

            button.pack(fill="x",padx=20,pady=6)

    # =========================
    # MAIN AREA
    # =========================

    def create_main_area(self):

        self.main_frame = ctk.CTkFrame(self,corner_radius=0,fg_color="white")

        self.main_frame.pack(side="right",fill="both",expand=True)

    def clear_main(self):

        for widget in self.main_frame.winfo_children():
            widget.destroy()

    # =========================
    # VIEWS
    # =========================

    def show_dashboard(self):

        self.clear_main()

        DashboardView(self.main_frame)

    def show_members(self):

        self.clear_main()

        MembersView(self.main_frame)

    def show_trainers(self):

        self.clear_main()

        TrainersView( self.main_frame)

    def show_memberships(self):

        self.clear_main()

        MembershipsView(self.main_frame)

    def show_payments(self):

        self.clear_main()

        PaymentsView(self.main_frame)

    def show_attendance(self):

        self.clear_main()

        AttendanceView(self.main_frame)


if __name__ == "__main__":
    app = GymApp()
    app.mainloop()