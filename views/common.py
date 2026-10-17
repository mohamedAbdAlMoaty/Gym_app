"""Shared UI helpers used by all views."""

import customtkinter as ctk

from tkinter import ttk

import storage

from views.theme import (
    BG,
    SURFACE,
    SURFACE_2,
    SURFACE_3,
    BORDER,
    ACCENT,
    ACCENT_HOVER,
    TEXT,
    TEXT_2,
    MUTED,
    FONT,
    PAGE_SUBTITLES,
)


def clear(parent):

    for widget in parent.winfo_children():
        widget.destroy()


# =========================
# PAGE TITLE
# =========================


def page_title(parent, text):

    header = ctk.CTkFrame(parent, fg_color="transparent")

    header.pack(fill="x", padx=34, pady=(28, 16))

    title_box = ctk.CTkFrame(header, fg_color="transparent")

    title_box.pack(side="left")

    ctk.CTkLabel(
        title_box,
        text=text,
        font=ctk.CTkFont(family=FONT, size=30, weight="bold"),
        text_color=TEXT,
    ).pack(anchor="w")

    ctk.CTkLabel(
        title_box,
        text=PAGE_SUBTITLES.get(text, "Gym management workspace"),
        font=ctk.CTkFont(family=FONT, size=12),
        text_color=MUTED,
    ).pack(anchor="w", pady=(3, 0))

    return header


# =========================
# TOOLBAR
# =========================


def toolbar(parent):

    bar = ctk.CTkFrame(
        parent,
        fg_color=SURFACE,
        corner_radius=14,
        border_width=1,
        border_color=BORDER,
    )

    bar.pack(fill="x", padx=34, pady=(4, 12), ipady=10)

    return bar


# =========================
# TABLES
# =========================


def create_table(parent, columns, widths=None):

    frame = ctk.CTkFrame(
        parent,
        fg_color=SURFACE,
        corner_radius=16,
        border_width=1,
        border_color=BORDER,
    )

    frame.pack(fill="both", expand=True, padx=34, pady=10)

    # -------------------------
    # TREEVIEW STYLE
    # -------------------------

    style = ttk.Style()

    try:
        style.theme_use("clam")

    except Exception:
        pass

    style.configure(
        "Gym.Treeview",
        background=SURFACE,
        fieldbackground=SURFACE,
        foreground=TEXT_2,
        borderwidth=0,
        rowheight=40,
        font=(FONT, 10),
    )

    style.configure(
        "Gym.Treeview.Heading",
        background=SURFACE_2,
        foreground=MUTED,
        relief="flat",
        borderwidth=0,
        font=(FONT, 10, "bold"),
        padding=(8, 12),
    )

    style.map(
        "Gym.Treeview",
        background=[("selected", ACCENT)],
        foreground=[("selected", "white")],
    )

    style.map(
        "Gym.Treeview.Heading",
        background=[("active", SURFACE_3)],
    )

    style.configure(
        "Gym.Vertical.TScrollbar",
        background=SURFACE_2,
        troughcolor=SURFACE,
        bordercolor=SURFACE,
        arrowcolor=MUTED,
    )

    # -------------------------
    # TABLE
    # -------------------------

    table = ttk.Treeview(
        frame,
        columns=columns,
        show="headings",
        selectmode="browse",
        style="Gym.Treeview",
    )

    for i, column in enumerate(columns):
        table.heading(column, text=column, anchor="center")

        table.column(
            column,
            width=(widths[i] if widths else 140),
            anchor="center",
            minwidth=70,
        )

    # -------------------------
    # SCROLLBAR
    # -------------------------

    scrollbar = ttk.Scrollbar(
        frame,
        orient="vertical",
        command=table.yview,
        style=("Gym.Vertical.TScrollbar"),
    )

    table.configure(yscrollcommand=scrollbar.set)

    table.pack(side="left", fill="both", expand=True, padx=(1, 0), pady=1)

    scrollbar.pack(side="right", fill="y", pady=1)

    return table


def fill_table(table, rows):
    """
    First value of every row
    is used as row id.
    """

    table.delete(*table.get_children())

    for row in rows:
        table.insert("", "end", iid=str(row[0]), values=row)


def selected_id(table):

    selection = table.selection()

    return selection[0] if selection else None


# =========================
# DIALOGS
# =========================


def open_dialog(parent, title, size):

    window = ctk.CTkToplevel(parent)

    window.title(title)

    window.geometry(size)

    window.configure(fg_color=BG)

    window.transient(parent.winfo_toplevel())

    window.after(200, lambda: _grab(window))

    return window


def _grab(window):

    try:
        window.grab_set()

        window.focus()

    except Exception:
        pass


def dialog_title(window, text):

    ctk.CTkLabel(
        window,
        text=text,
        font=ctk.CTkFont(family=FONT, size=24, weight="bold"),
        text_color=TEXT,
    ).pack(pady=(25, 3))

    ctk.CTkLabel(
        window,
        text="Fill in the details below",
        font=ctk.CTkFont(family=FONT, size=11),
        text_color=MUTED,
    ).pack(pady=(0, 14))


# =========================
# ENTRY
# =========================


def add_entry(window, label, default=""):

    ctk.CTkLabel(
        window,
        text=label,
        font=ctk.CTkFont(family=FONT, size=12, weight="bold"),
        text_color=TEXT_2,
    ).pack(anchor="w", padx=40, pady=(8, 5))

    entry = ctk.CTkEntry(
        window,
        width=360,
        height=42,
        corner_radius=10,
        fg_color=SURFACE,
        border_color=BORDER,
        text_color=TEXT,
        placeholder_text_color=MUTED,
    )

    entry.pack(padx=40)

    if default:
        entry.insert(0, default)

    return entry


# =========================
# COMBO BOX
# =========================


def add_combo(window, label, values, default=None, command=None):

    ctk.CTkLabel(
        window,
        text=label,
        font=ctk.CTkFont(family=FONT, size=12, weight="bold"),
        text_color=TEXT_2,
    ).pack(anchor="w", padx=40, pady=(8, 5))

    combo = ctk.CTkComboBox(
        window,
        values=values,
        width=360,
        height=42,
        corner_radius=10,
        state="readonly",
        command=command,
        fg_color=SURFACE,
        border_color=BORDER,
        button_color=ACCENT,
        button_hover_color=ACCENT_HOVER,
        text_color=TEXT,
        dropdown_fg_color=SURFACE_2,
        dropdown_hover_color=SURFACE_3,
        dropdown_text_color=TEXT,
    )

    combo.pack(padx=40)

    if default is not None:
        combo.set(default)

    elif values:
        combo.set(values[0])

    return combo


# =========================
# SAVE BUTTON
# =========================


def add_save_button(window, text, command):

    ctk.CTkButton(
        window,
        text=text,
        width=360,
        height=44,
        command=command,
        corner_radius=10,
        fg_color=ACCENT,
        hover_color=ACCENT_HOVER,
        font=ctk.CTkFont(family=FONT, size=13, weight="bold"),
    ).pack(pady=25)


# =========================
# COMBOBOX CHOICES
# =========================


def member_choices():

    return [
        f"{member['member_id']} - {member['name']}"
        for member in storage.load("members")
    ]


def trainer_choices():

    return ["Unassigned"] + [
        f"{trainer['trainer_id']} - {trainer['name']}"
        for trainer in storage.load("trainers")
    ]


def trainer_choice_for(trainer_id):

    trainer = storage.get_trainer(trainer_id)

    return f"{trainer['trainer_id']} - {trainer['name']}" if trainer else "Unassigned"


def plan_choices():

    return [f"{plan} - €{info['price']:.0f}" for plan, info in storage.PLANS.items()]


def choice_id(choice):
    """
    Example:

    M001 - Ahmed Ali
    ->
    M001
    """

    if not choice or choice == "Unassigned":
        return ""

    return choice.split(" - ")[0]
