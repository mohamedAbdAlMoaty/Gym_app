"""Shared UI helpers used by all views."""

import customtkinter as ctk
from tkinter import ttk

import storage


def clear(parent):
    for widget in parent.winfo_children():
        widget.destroy()


def page_title(parent, text):
    title = ctk.CTkLabel(parent, text=text, font=ctk.CTkFont(size=28, weight="bold"))
    title.pack(anchor="w", padx=30, pady=(30, 20))


def toolbar(parent):
    bar = ctk.CTkFrame(parent, fg_color="transparent")
    bar.pack(fill="x", padx=30, pady=10)
    return bar


# =========================
# TABLES
# =========================

def create_table(parent, columns, widths=None):
    frame = ctk.CTkFrame(parent)
    frame.pack(fill="both", expand=True, padx=30, pady=10)

    table = ttk.Treeview(frame, columns=columns, show="headings", selectmode="browse")
    for i, column in enumerate(columns):
        table.heading(column, text=column, anchor="center")
        table.column(column, width=widths[i] if widths else 140, anchor="center")

    scrollbar = ttk.Scrollbar(frame, orient="vertical", command=table.yview)
    table.configure(yscrollcommand=scrollbar.set)
    table.pack(side="left", fill="both", expand=True)
    scrollbar.pack(side="right", fill="y")
    return table


def fill_table(table, rows):
    """First value of every row is used as the row id (iid), so lookups never depend on
    the displayed text (Treeview would turn '01712345678' into a number)."""
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
    ctk.CTkLabel(window, text=text, font=ctk.CTkFont(size=24, weight="bold")).pack(pady=(25, 15))


def add_entry(window, label, default=""):
    ctk.CTkLabel(window, text=label).pack(anchor="w", padx=40, pady=(8, 3))
    entry = ctk.CTkEntry(window, width=360)
    entry.pack(padx=40)
    if default:
        entry.insert(0, default)
    return entry


def add_combo(window, label, values, default=None, command=None):
    ctk.CTkLabel(window, text=label).pack(anchor="w", padx=40, pady=(8, 3))
    combo = ctk.CTkComboBox(window, values=values, width=360, state="readonly", command=command)
    combo.pack(padx=40)
    if default is not None:
        combo.set(default)
    elif values:
        combo.set(values[0])
    return combo


def add_save_button(window, text, command):
    ctk.CTkButton(window, text=text, width=360, height=40, command=command).pack(pady=25)


# =========================
# COMBOBOX CHOICES  ("M001 - Ahmed Ali")
# =========================

def member_choices():
    return [f"{m['member_id']} - {m['name']}" for m in storage.load("members")]


def trainer_choices():
    return ["Unassigned"] + [f"{t['trainer_id']} - {t['name']}" for t in storage.load("trainers")]


def trainer_choice_for(trainer_id):
    trainer = storage.get_trainer(trainer_id)
    return f"{trainer['trainer_id']} - {trainer['name']}" if trainer else "Unassigned"


def plan_choices():
    return [f"{plan} - €{info['price']:.0f}" for plan, info in storage.PLANS.items()]


def choice_id(choice):
    """'M001 - Ahmed Ali' -> 'M001'; 'Unassigned' -> ''."""
    if not choice or choice == "Unassigned":
        return ""
    return choice.split(" - ")[0]
