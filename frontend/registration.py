from tkinter import *

def set_placeholder(entry, placeholder_text, is_password=False):
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

def rejestracja_placehold(user,password):
    print("Rejestracja")

def registration_window(window, back_function):
    for widget in window.winfo_children():
        widget.destroy()
    frame_registration = Frame(window)
    frame_registration.place(relx=0.5, rely=0.5, anchor=CENTER)

    email = StringVar()
    haslo = StringVar()

    Label(frame_registration, text="Email").grid(row=0, column=0, padx=10, pady=5)
    entry_registration = Entry(frame_registration, textvariable=email)
    entry_registration.grid(row=0, column=1, padx=10, pady=5)
    set_placeholder(entry_registration, "Wpisz Email")

    Label(frame_registration, text="Hasło").grid(row=1, column=0, padx=10, pady=5)
    entry_haslo = Entry(frame_registration, textvariable=haslo)
    entry_haslo.grid(row=1, column=1, padx=10, pady=5)
    set_placeholder(entry_haslo, "Wpisz hasło", is_password=True)


    Button(frame_registration, text="Rejestracja", command=lambda: rejestracja_placehold(email.get(),haslo.get())).grid(row=2,column=0,columnspan=2,pady=10)

    Button(frame_registration, text="Logowanie", command=lambda: back_function(window)).grid(row=3, column=0, columnspan=2)

