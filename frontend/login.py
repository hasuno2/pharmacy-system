"""
login.py

Provides the login window for the pharmacy system GUI.
Includes placeholder handling and a redirect to the registration window.
"""

from tkinter import *
from frontend import registration

def set_placeholder(entry, placeholder_text, is_password=False):
    """
    Adds placeholder behavior to an Entry widget.

    Args:
        entry (tk.Entry): Entry widget to modify.
        placeholder_text (str): Text to display as placeholder.
        is_password (bool): If True, masks input after focus.
    """
    entry.insert(0, placeholder_text)
    entry.config(fg='gray')
    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, 'end')
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

def logowanie_placehold(user, password):
    """
    Placeholder login function for testing.

    Args:
        user (str): Username input.
        password (str): Password input.
    """
    print("logowanie")

def login_window(window):
    """
    Creates and displays the login GUI window.

    Args:
        window (tk.Tk): Root Tkinter window.
    """
    for widget in window.winfo_children():
        widget.destroy()

    frame_login = Frame(window)
    frame_login.place(relx=0.5, rely=0.5, anchor=CENTER)

    login = StringVar()
    haslo = StringVar()

    Label(frame_login, text="Login").grid(row=0, column=0, padx=10, pady=5)
    entry_login = Entry(frame_login, textvariable=login)
    entry_login.grid(row=0, column=1, padx=10, pady=5)
    set_placeholder(entry_login, "Wpisz login")

    Label(frame_login, text="Hasło").grid(row=1, column=0, padx=10, pady=5)
    entry_haslo = Entry(frame_login, textvariable=haslo)
    entry_haslo.grid(row=1, column=1, padx=10, pady=5)
    set_placeholder(entry_haslo, "Wpisz hasło", is_password=True)

    Button(frame_login, text="Logowanie", command=lambda: logowanie_placehold(login.get(), haslo.get)).grid(row=2, column=0, columnspan=2, pady=10)
    Button(frame_login, text="Rejestracja", command=lambda: registration.registration_window(window, login_window)).grid(row=3, column=0, columnspan=2)

# Main execution
window = Tk()
window.title("Aplikacja")
window.geometry("400x300")
login_window(window)
window.mainloop()
