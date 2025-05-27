"""
Gui.py

Provides a standalone demo GUI for:
- Login
- Registration
- Admin dashboard
- Customer viewing

Uses placeholder data and simulates logic flow, designed for rapid frontend iteration.
"""

from tkinter import *
from tkinter import ttk
import pandas as pd


def set_placeholder(entry, placeholder_text, is_password=False):
    """
    Adds placeholder behavior to Entry widget.

    Args:
        entry (tk.Entry): Input field.
        placeholder_text (str): Placeholder string to show.
        is_password (bool): Whether input should be hidden on focus.
    """
    entry.insert(0, placeholder_text)
    entry.config(fg='gray')

    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, END)
            entry.config(fg='black')
            if is_password:
                entry.config(show="*")

    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder_text)
            entry.config(fg='gray')
            if is_password:
                entry.config(show="")

    entry.bind("<FocusIn>", on_focus_in)
    entry.bind("<FocusOut>", on_focus_out)


def get_data(search_term=None):
    """
    Returns demo customer data as a DataFrame.

    Args:
        search_term (str, optional): Filter by name.

    Returns:
        pd.DataFrame: Filtered or full demo dataset.
    """
    data = [
        {'ID': 1, 'NAME': 'Alice', 'E-MAIL': 'alice@example.com', 'PHONE': '555-1234'},
        {'ID': 2, 'NAME': 'Bob',   'E-MAIL': 'bob@example.com',   'PHONE': '555-5678'},
        {'ID': 3, 'NAME': 'Carol', 'E-MAIL': 'carol@example.com', 'PHONE': '555-9012'}
    ]
    df = pd.DataFrame(data)
    if search_term:
        return df[df['NAME'].str.contains(search_term, case=False, na=False)]
    return df


def logowanie(login, password):
    """
    Placeholder login routing logic.

    Args:
        login (str): Username.
        password (str): Password.
    """
    if login == "admin":
        admin_window(window)
    else:
        user_window(window, login)


def login_window(window):
    """
    Loads login interface into the main window.

    Args:
        window (tk.Tk): App root window.
    """
    for widget in window.winfo_children():
        widget.destroy()

    frame_login = Frame(window)
    frame_login.place(relx=0.5, rely=0.5, anchor=CENTER)

    login = StringVar()
    haslo = StringVar()

    Label(frame_login, text="Login").grid(row=0, column=0)
    entry_login = Entry(frame_login, textvariable=login)
    entry_login.grid(row=0, column=1)
    set_placeholder(entry_login, "Enter login")

    Label(frame_login, text="Password").grid(row=1, column=0)
    entry_haslo = Entry(frame_login, textvariable=haslo)
    entry_haslo.grid(row=1, column=1)
    set_placeholder(entry_haslo, "Enter password", is_password=True)

    Button(frame_login, text="Login", command=lambda: logowanie(login.get(), haslo.get())).grid(row=2, column=0, columnspan=2)
    Button(frame_login, text="Register", command=lambda: registration_window(window)).grid(row=3, column=0, columnspan=2)


def rejestracja_placehold(imie, nazwisko, user, password):
    """
    Placeholder registration backend logic.

    Args:
        imie (str): First name.
        nazwisko (str): Last name.
        user (str): Email.
        password (str): Password.
    """
    print("Registered:", imie, nazwisko, user)


def registration_window(window):
    """
    Renders registration form interface.

    Args:
        window (tk.Tk): App root window.
    """
    for widget in window.winfo_children():
        widget.destroy()

    frame = Frame(window)
    frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    fields = {
        "First Name": StringVar(),
        "Last Name": StringVar(),
        "Email": StringVar(),
        "Password": StringVar()
    }

    for i, (label, var) in enumerate(fields.items()):
        Label(frame, text=label).grid(row=i, column=0)
        entry = Entry(frame, textvariable=var)
        entry.grid(row=i, column=1)
        set_placeholder(entry, f"Enter {label.lower()}", is_password=(label == "Password"))

    Button(frame, text="Register", command=lambda: rejestracja_placehold(
        fields["First Name"].get(),
        fields["Last Name"].get(),
        fields["Email"].get(),
        fields["Password"].get()
    )).grid(row=4, column=0, columnspan=2)

    Button(frame, text="Back to Login", command=lambda: login_window(window)).grid(row=5, column=0, columnspan=2)


def get_admin_name():
    """Returns hardcoded admin display name."""
    return "Admin"


def admin_window(window):
    """
    Displays basic admin dashboard with customer and drug views.

    Args:
        window (tk.Tk): App root window.
    """
    for w in window.winfo_children():
        w.destroy()

    Label(window, text=f"Welcome, {get_admin_name()}", font=("Helvetica", 14)).pack(pady=10)

    Button(window, text="View Customers", command=lambda: admin_users_window(window)).pack(pady=5)
    Button(window, text="View Medicines", command=lambda: purchase_window(window)).pack(pady=5)
    Button(window, text="Logout", command=lambda: login_window(window)).pack(pady=5)


def admin_users_window(window):
    """
    Shows customer data in admin view.

    Args:
        window (tk.Tk): App root window.
    """
    for widget in window.winfo_children():
        widget.destroy()

    data = get_data()
    tree = ttk.Treeview(window, columns=data.columns.tolist(), show="headings")
    for col in data.columns:
        tree.heading(col, text=col)
        tree.column(col, width=150)
    for _, row in data.iterrows():
        tree.insert('', END, values=row.tolist())
    tree.pack(expand=True, fill='both')

    Button(window, text="Back", command=lambda: admin_window(window)).pack(pady=5)


def purchase_window(window):
    """
    Displays placeholder drug purchase screen.

    Args:
        window (tk.Tk): App root window.
    """
    for widget in window.winfo_children():
        widget.destroy()

    Label(window, text="Medicine Shop (Coming Soon)").pack(pady=20)
    Button(window, text="Back", command=lambda: admin_window(window)).pack(pady=5)


def user_window(window, username):
    """
    Displays basic user screen after login.

    Args:
        window (tk.Tk): App root window.
        username (str): Username for welcome.
    """
    for widget in window.winfo_children():
        widget.destroy()

    Label(window, text=f"Hello, {username}", font=("Helvetica", 14)).pack(pady=10)
    Button(window, text="Buy Medicine", command=lambda: open_medicine_shop(window)).pack(pady=5)
    Button(window, text="Logout", command=lambda: login_window(window)).pack(pady=5)


def open_medicine_shop(window):
    """
    Placeholder for future user-side medicine shop.

    Args:
        window (tk.Tk): App root window.
    """
    for widget in window.winfo_children():
        widget.destroy()

    Label(window, text="Medicine Shop (Coming Soon)").pack(pady=20)
    Button(window, text="Back", command=lambda: user_window(window, "User")).pack(pady=5)


# Launch GUI
window = Tk()
window.title("Pharmacy GUI")
window.geometry("400x300")
login_window(window)
window.mainloop()
