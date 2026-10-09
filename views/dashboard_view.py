import customtkinter as ctk
from data_storage import Json_manager

from views.common import page_title


class DashboardView:

    def __init__(self, parent):
        self.parent = parent
        self.show_dashboard()

    def show_dashboard(self):
        page_title(self.parent, "Dashboard")

        members = Json_manager().read_from_json_file("members")
        # continue showing the info

        cards_frame = ctk.CTkFrame(self.parent, fg_color="transparent")
        cards_frame.pack(fill="x", padx=30)

        cards = [
            ("Total Members", str(len(members))),
            ("Active Members", str(4)),
            ("Expired Members", str(1)),
            ("Today's Attendance", str(1)),
            ("Revenue This Month", f"${float(200)}"),
        ]
        for column, (title, value) in enumerate(cards):
            self.create_card(cards_frame, title, value, column)

        ctk.CTkLabel(self.parent, text="Recent Activity",
                     font=ctk.CTkFont(size=20, weight="bold")).pack(anchor="w", padx=30, pady=(40, 15))

        activity = ctk.CTkTextbox(self.parent, height=240)
        activity.pack(fill="x", padx=30)
        activity.insert("1.0", "\n".join(f"• {text}" for text in self.recent_events()) or "No activity yet.")
        activity.configure(state="disabled")

    def recent_events(self, limit=10):

        # get all date in joson file and events and then sort them after
        # events = []






        return ["test"]

    def create_card(self, parent, title, value, column):
        card = ctk.CTkFrame(parent, height=120)
        card.grid(row=0, column=column, padx=8, pady=10, sticky="nsew")
        parent.grid_columnconfigure(column, weight=1, uniform="cards")

        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=15)).pack(pady=(20, 5), padx=10)
        ctk.CTkLabel(card, text=value, font=ctk.CTkFont(size=28, weight="bold")).pack(pady=(0, 15))
