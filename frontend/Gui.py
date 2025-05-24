from tkinter import *
from tkinter import ttk
import pandas as pd
from datetime import datetime

# Wspólna funkcja placeholder
def set_placeholder(entry, placeholder_text, is_password=False):
    entry.insert(0, placeholder_text)
    entry.config(fg='gray')
    def on_focus_in(event):
        if entry.get() == placeholder_text:
            entry.delete(0, 'end')
            entry.config(fg='black')
            if is_password:
                entry.config(show='*')
    def on_focus_out(event):
        if not entry.get():
            entry.insert(0, placeholder_text)
            entry.config(fg='gray')
            if is_password:
                entry.config(show='')
    entry.bind('<FocusIn>', on_focus_in)
    entry.bind('<FocusOut>', on_focus_out)

# Dane przykładowe
def get_data(search_term=None):
    data = [
        {'ID': 1, 'NAME': 'Alice', 'E-MAIL': 'alice@example.com', 'PHONE': '555-1234', 'CREATED': '2024-01-01', 'UPDATED': '2024-06-01'},
        {'ID': 2, 'NAME': 'Bob',   'E-MAIL': 'bob@example.com',   'PHONE': '555-5678', 'CREATED': '2024-02-15', 'UPDATED': '2024-06-03'},
        {'ID': 3, 'NAME': 'Carol', 'E-MAIL': 'carol@example.com', 'PHONE': '555-9012', 'CREATED': '2024-03-20', 'UPDATED': '2024-06-05'}
    ]
    df = pd.DataFrame(data)
    if search_term:
        return df[df['NAME'].str.contains(search_term, case=False, na=False)]
    return df

# Ekran logowania
def logowanie(login, password):
    # Tymczasowy warunek wyboru roli
    tymczasowa = True
    if not tymczasowa:
        user_window(window, login)
    else:
        admin_window(window)

def login_window(window):
    for widget in window.winfo_children(): widget.destroy()
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

    Button(frame_login, text="Logowanie", command=lambda: logowanie(login.get(), haslo.get())).grid(row=2, column=0, columnspan=2, pady=10)
    Button(frame_login, text="Rejestracja", command=lambda: registration_window(window)).grid(row=3, column=0, columnspan=2)

# Ekran rejestracji
def rejestracja_placehold(imie, nazwisko, user, password):
    print(f"Rejestracja: {imie}, {nazwisko}, {user}, {password}")

def registration_window(window):
    for widget in window.winfo_children(): widget.destroy()
    frame_registration = Frame(window)
    frame_registration.place(relx=0.5, rely=0.5, anchor=CENTER)

    imie = StringVar()
    nazwisko = StringVar()
    email = StringVar()
    haslo = StringVar()

    Label(frame_registration, text="Rejestracja", font=("Helvetica", 20, "bold")).grid(row=0, column=0, columnspan=2, pady=(0,20))
    Label(frame_registration, text="Imię").grid(row=1, column=0, padx=10, pady=5)
    entry_imie = Entry(frame_registration, textvariable=imie)
    entry_imie.grid(row=1, column=1, padx=10, pady=5)
    set_placeholder(entry_imie, "Wpisz imię")

    Label(frame_registration, text="Nazwisko").grid(row=2, column=0, padx=10, pady=5)
    entry_nazwisko = Entry(frame_registration, textvariable=nazwisko)
    entry_nazwisko.grid(row=2, column=1, padx=10, pady=5)
    set_placeholder(entry_nazwisko, "Wpisz nazwisko")

    Label(frame_registration, text="Email").grid(row=3, column=0, padx=10, pady=5)
    entry_email = Entry(frame_registration, textvariable=email)
    entry_email.grid(row=3, column=1, padx=10, pady=5)
    set_placeholder(entry_email, "Wpisz Email")

    Label(frame_registration, text="Hasło").grid(row=4, column=0, padx=10, pady=5)
    entry_haslo = Entry(frame_registration, textvariable=haslo)
    entry_haslo.grid(row=4, column=1, padx=10, pady=5)
    set_placeholder(entry_haslo, "Wpisz hasło", is_password=True)

    Button(frame_registration, text="Rejestracja", command=lambda: rejestracja_placehold(imie.get(), nazwisko.get(), email.get(), haslo.get())).grid(row=5, column=0, columnspan=2, pady=10)
    Button(frame_registration, text="Logowanie", command=lambda: login_window(window)).grid(row=6, column=0, columnspan=2)

# Panel admina
def get_admin_name(): return "Jan"

def admin_window(window):
    for w in window.winfo_children(): w.destroy()
    frame_top = Frame(window)
    frame_top.pack(fill="x", padx=10, pady=10)

    Label(frame_top, text=f"Witaj, {get_admin_name()}!", font=("Arial",14)).pack(side=LEFT)
    Button(frame_top, text="Wyloguj", command=lambda: login_window(window), width=10, bg="lightgray").pack(side=RIGHT)

    separator = Frame(window, height=2, bg="gray")
    separator.pack(fill="x", padx=10, pady=(0,20))

    frame_main = Frame(window)
    frame_main.pack(expand=True)

    Button(frame_main, text="Sprawdź wszystkich użytkowników", width=30, bg="#4CAF50", fg="white", command=lambda: admin_users_window(window)).pack(pady=5)
    Button(frame_main, text="Zakup leków", width=30, bg="#2196F3", fg="white").pack(pady=5)
    Button(frame_main, text="Dodaj nowe leki", width=30, bg="#FF9800", fg="white").pack(pady=5)

# Panel administracji użytkowników

def admin_users_window(window):
    for widget in window.winfo_children(): widget.destroy()
    window.title('Panel administracyjny użytkowników')
    window.geometry('900x600')

    top_frame = Frame(window)
    top_frame.pack(fill=X, padx=10, pady=10)

    Label(top_frame, text='Szukaj użytkownika (ID/Nazwa):').grid(row=0, column=1, sticky=W)
    ent_search = Entry(top_frame)
    ent_search.grid(row=0, column=2, padx=(5,20))
    set_placeholder(ent_search, 'Wpisz nazwę...', False)

    def on_search():
        term = ent_search.get().strip()
        df = get_data(None if term=='' or term=='Wpisz nazwę...' else term)
        populate_tree(df)
    Button(top_frame, text='Szukaj', command=on_search).grid(row=0, column=3, padx=5)
    Button(top_frame, text='Dodaj', command=lambda: popup_form('add')).grid(row=0, column=4, padx=5)
    Button(top_frame, text='Edytuj', command=lambda: popup_form('edit', tree.item(tree.focus())['values'] if tree.focus() else None)).grid(row=0, column=5, padx=5)
    Button(top_frame, text='Usuń', command=lambda: tree.delete(tree.focus())).grid(row=0, column=6, padx=5)
    Button(top_frame, text='Powrót', command=lambda: admin_window(window)).grid(row=0, column=7, sticky=E)

    ttk.Separator(window, orient='horizontal').pack(fill=X, padx=10, pady=5)
    bottom = Frame(window)
    bottom.pack(fill=BOTH, expand=True, padx=10, pady=5)
    cols = ['ID','NAME','E-MAIL','PHONE','CREATED','UPDATED']
    tree = ttk.Treeview(bottom, columns=cols, show='headings')
    for c in cols: tree.heading(c, text=c); tree.column(c, width=130, anchor=W)
    vsb = Scrollbar(bottom, orient=VERTICAL, command=tree.yview)
    tree.configure(yscrollcommand=vsb.set); vsb.pack(side=RIGHT, fill=Y); tree.pack(fill=BOTH, expand=True)

    def populate_tree(df):
        for i in tree.get_children(): tree.delete(i)
        for _,r in df.iterrows(): tree.insert('', END, values=tuple(r[c] for c in cols))

    def popup_form(mode, vals=None):
        p = Toplevel(window); p.title('Edycja użytkownika' if mode=='edit' else 'Dodaj użytkownika'); p.geometry('400x300')
        n,e,ph = StringVar(),StringVar(),StringVar()
        Label(p, text='Imię i nazwisko').pack(pady=5); Entry(p, textvariable=n).pack(pady=5)
        Label(p, text='Email').pack(pady=5); Entry(p, textvariable=e).pack(pady=5)
        Label(p, text='Telefon').pack(pady=5); Entry(p, textvariable=ph).pack(pady=5)
        if mode=='edit' and vals: n.set(vals[1]); e.set(vals[2]); ph.set(vals[3])
        def save():
            now=datetime.now().strftime('%Y-%m-%d')
            if mode=='add': nid=len(tree.get_children())+1; tree.insert('', END, values=(nid,n.get(),e.get(),ph.get(),now,now))
            else: s=tree.focus(); tree.item(s, values=(vals[0],n.get(),e.get(),ph.get(),vals[4],now))
            p.destroy()
        Button(p, text='Zapisz', command=save).pack(pady=10)

    populate_tree(get_data())

# Panel użytkownika

def open_medicine_shop(window):
    pass

def user_window(window, username):
    for widget in window.winfo_children(): widget.destroy()
    frame_user = Frame(window, padx=20, pady=20); frame_user.pack(fill=BOTH, expand=True)
    Label(frame_user, text=f"Witaj, {username}!", font=("Arial",16)).grid(row=0, column=0, sticky=W)
    Button(frame_user, text="Wyloguj", width=12, command=lambda: login_window(window)).grid(row=0, column=1, sticky=E, padx=10)
    frame_user.grid_columnconfigure(0, weight=1); frame_user.grid_columnconfigure(1, weight=1)
    Button(frame_user, text="Zakup leków →", font=("Arial",14), relief=RAISED, bd=3, padx=10, pady=5, command=lambda: open_medicine_shop(window)).grid(row=1, column=0, columnspan=2, pady=(30,0))

# Uruchomienie aplikacji
window = Tk()
window.title("Aplikacja")
window.geometry("400x300")
login_window(window)
window.mainloop()
