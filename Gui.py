from tkinter import *
from tkinter import ttk
from datetime import datetime
import pandas as pd
import customers
import drugs

# Przechowywanie informacji o aktualnym użytkowniku
default_user = {'ID': None, 'NAME': None, 'ROLE': None}
current_user = default_user.copy()

# Funkcja placeholder
def set_placeholder(entry_widget, placeholder_text, is_password=False):
    entry_widget.insert(0, placeholder_text)
    entry_widget.config(fg='gray')
    def on_focus_in(event):
        if entry_widget.get() == placeholder_text:
            entry_widget.delete(0, 'end')
            entry_widget.config(fg='black')
            if is_password:
                entry_widget.config(show='*')
    def on_focus_out(event):
        if not entry_widget.get():
            entry_widget.insert(0, placeholder_text)
            entry_widget.config(fg='gray')
            if is_password:
                entry_widget.config(show='')
    entry_widget.bind('<FocusIn>', on_focus_in)
    entry_widget.bind('<FocusOut>', on_focus_out)

# Rejestracja użytkownika
def registration_window(main_window):
    for widget in main_window.winfo_children():
        widget.destroy()
    main_window.title("Rejestracja")
    registration_frame = Frame(main_window)
    registration_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    first_name_var = StringVar()
    last_name_var = StringVar()
    email_var = StringVar()
    phone_var = StringVar()
    password_var = StringVar()

    Label(registration_frame, text="Imię").grid(row=0, column=0, padx=10, pady=5)
    first_name_entry = Entry(registration_frame, textvariable=first_name_var)
    first_name_entry.grid(row=0, column=1, padx=10, pady=5)
    set_placeholder(first_name_entry, "Wpisz imię")

    Label(registration_frame, text="Nazwisko").grid(row=1, column=0, padx=10, pady=5)
    last_name_entry = Entry(registration_frame, textvariable=last_name_var)
    last_name_entry.grid(row=1, column=1, padx=10, pady=5)
    set_placeholder(last_name_entry, "Wpisz nazwisko")

    Label(registration_frame, text="E-mail").grid(row=2, column=0, padx=10, pady=5)
    email_entry = Entry(registration_frame, textvariable=email_var)
    email_entry.grid(row=2, column=1, padx=10, pady=5)
    set_placeholder(email_entry, "Wpisz e-mail")

    Label(registration_frame, text="Telefon").grid(row=3, column=0, padx=10, pady=5)
    phone_entry = Entry(registration_frame, textvariable=phone_var)
    phone_entry.grid(row=3, column=1, padx=10, pady=5)
    set_placeholder(phone_entry, "Wpisz numer telefonu")

    Label(registration_frame, text="Hasło").grid(row=4, column=0, padx=10, pady=5)
    password_entry = Entry(registration_frame, textvariable=password_var)
    password_entry.grid(row=4, column=1, padx=10, pady=5)
    set_placeholder(password_entry, "Wpisz hasło", is_password=True)

    def register_user():
        # dodajemy klienta do bazy
        full_name = f"{first_name_var.get()} {last_name_var.get()}"
        try:
            customers.addCustomer(customers.customersDf, customers.addressDf,
                                  full_name, email=email_var.get(), phone=phone_var.get())
        except Exception as e:
            print(f"Błąd rejestracji: {e}")
            return
        login_window(main_window)

    Button(registration_frame, text="Rejestruj", command=register_user).grid(row=5, column=0, columnspan=2, pady=10)
    Button(registration_frame, text="Powrót", command=lambda: login_window(main_window)).grid(row=6, column=0, columnspan=2)

# Okno logowania
def login_window(main_window):
    for widget in main_window.winfo_children():
        widget.destroy()
    main_window.title("Logowanie")
    login_frame = Frame(main_window)
    login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    title_label = Label(login_frame, text="Logowanie", font=("Arial", 18, "bold"))
    title_label.grid(row=0, column=0, columnspan=2, pady=(0, 20))

    Label(login_frame, text="Login", font=("Arial", 12)).grid(row=1, column=0, padx=10, pady=5, sticky=E)
    email_entry = Entry(login_frame, font=("Arial", 12), width=20)
    email_entry.grid(row=1, column=1, padx=10, pady=5)
    set_placeholder(email_entry, "Wpisz login")

    Label(login_frame, text="Hasło", font=("Arial", 12)).grid(row=2, column=0, padx=10, pady=5, sticky=E)
    password_entry = Entry(login_frame, font=("Arial", 12), width=20)
    password_entry.grid(row=2, column=1, padx=10, pady=5)
    set_placeholder(password_entry, "Wpisz hasło", is_password=True)

    def attempt_login():
        entered_email = email_entry.get()
        entered_password = password_entry.get()
        # Admin
        if entered_email == 'admin' and entered_password == 'admin':
            current_user.update({'ID': None, 'NAME': 'Admin', 'ROLE': 'admin'})
            admin_window(main_window)
        else:
            # zwykły użytkownik: logowanie przez email i hasło = ID
            customers_df = customers.customersDf
            user_record = customers_df[customers_df['E-MAIL'] == entered_email]
            if not user_record.empty:
                retrieved_id = user_record.iloc[0]['ID']
                if entered_password == str(retrieved_id):
                    current_user.update({'ID': retrieved_id, 'NAME': user_record.iloc[0]['NAME'], 'ROLE': 'user'})
                    user_window(main_window)
                    return
            print("Błędne dane logowania")

    Button(login_frame, text="Logowanie", command=attempt_login)\
        .grid(row=3, column=0, columnspan=2, pady=(15, 5), ipadx=10, ipady=2)
    Button(login_frame, text="Rejestracja", command=lambda: registration_window(main_window))\
        .grid(row=4, column=0, columnspan=2, pady=(0, 10), ipadx=10, ipady=2)

# Okno użytkownika
def user_window(main_window):
    for widget in main_window.winfo_children():
        widget.destroy()
    user_frame = Frame(main_window, padx=20, pady=20)
    user_frame.pack(fill=BOTH, expand=True)

    Label(user_frame, text=f"Witaj, {current_user['NAME']}!", font=("Arial", 16)).grid(row=0, column=0, sticky=W)
    Button(user_frame, text="Wyloguj", width=12, command=lambda: logout(main_window)).grid(row=0, column=1, sticky=E,
                                                                                           padx=10)
    user_frame.grid_columnconfigure(0, weight=1)
    user_frame.grid_columnconfigure(1, weight=1)

    Button(user_frame, text="Kup leki", font=("Arial", 14), relief=RAISED, bd=3, padx=10, pady=5,
           command=lambda: user_purchase_window()).grid(row=1, column=0, columnspan=2, pady=(30, 0))


# Okno zakupów użytkownika
def user_purchase_window():
    purchase_win = Toplevel()
    purchase_win.title('Zakup leków')
    purchase_win.geometry('800x500')

    # Górny panel: wyszukiwanie
    search_frame = Frame(purchase_win)
    search_frame.pack(fill=X, padx=10, pady=10)
    Label(search_frame, text='Wyszukaj lek (nazwa):').pack(side=LEFT)
    search_var = StringVar()
    search_entry = Entry(search_frame, textvariable=search_var)
    search_entry.pack(side=LEFT, padx=5)
    Button(search_frame, text='Szukaj', command=lambda: populate(filter_drugs())).pack(side=LEFT, padx=5)
    Button(search_frame, text='Zamknij', command=purchase_win.destroy).pack(side=RIGHT)

    ttk.Separator(purchase_win, orient='horizontal').pack(fill=X, padx=10, pady=5)

    # Lista leków
    list_frame = Frame(purchase_win)
    list_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
    display_cols = ['DRUG', 'ON_RECEPT']
    tree_user = ttk.Treeview(list_frame, columns=display_cols, show='headings')
    for col in display_cols:
        tree_user.heading(col, text=col)
        tree_user.column(col, width=200, anchor=W)
    vsb_user = Scrollbar(list_frame, orient=VERTICAL, command=tree_user.yview)
    tree_user.configure(yscrollcommand=vsb_user.set)
    vsb_user.pack(side=RIGHT, fill=Y)
    tree_user.pack(fill=BOTH, expand=True)

    # Panel kupowania
    action_frame = Frame(purchase_win)
    action_frame.pack(fill=X, padx=10, pady=10)
    Label(action_frame, text='Ilość do kupienia:').pack(side=LEFT)
    quantity_var = StringVar()
    Entry(action_frame, textvariable=quantity_var, width=5).pack(side=LEFT, padx=5)
    Button(action_frame, text='Kup', command=lambda: buy_drug()).pack(side=LEFT, padx=5)

    # Funkcje pomocnicze
    def parse_drugs_df():
        raw_df = drugs.drugsDf.copy()
        first_col = raw_df.columns[0]
        df = raw_df[first_col].str.split(',', expand=True)
        df.columns = ['ID','DRUG','ON_RECEPT','NO_PACKAGES_AVAILABLE','DATE']
        return df

    def filter_drugs():
        df = parse_drugs_df()
        term = search_var.get().strip().lower()
        if term:
            df = df[df['DRUG'].str.lower().str.contains(term)]
        return df

    def populate(df=None):
        df = df if df is not None else parse_drugs_df()
        for item in tree_user.get_children():
            tree_user.delete(item)
        for _, row in df.iterrows():
            tree_user.insert('', END, values=(row['DRUG'], row['ON_RECEPT']))

    def buy_drug():
        sel = tree_user.focus()
        if not sel:
            return
        drug_name, on_recept = tree_user.item(sel)['values']
        qty = int(quantity_var.get()) if quantity_var.get().isdigit() else 0
        df = parse_drugs_df()
        match = df[(df['DRUG']==drug_name) & (df['ON_RECEPT']==on_recept)]
        if match.empty:
            return
        available = int(match.iloc[0]['NO_PACKAGES_AVAILABLE'])
        if qty <= 0 or qty > available:
            return
        # Aktualizacja magazynu
        df.loc[(df['DRUG']==drug_name) & (df['ON_RECEPT']==on_recept), 'NO_PACKAGES_AVAILABLE'] = available - qty
        # Zapisz zmiany w drugs.drugsDf
        new_list = df.apply(lambda r: ','.join([str(r[c]) for c in ['ID','DRUG','ON_RECEPT','NO_PACKAGES_AVAILABLE','DATE']]), axis=1)
        drugs.drugsDf[drugs.drugsDf.columns[0]] = new_list
        populate(df)

    populate()


# Panel admina
def admin_window(main_window):
    for widget in main_window.winfo_children():
        widget.destroy()
    admin_top_frame = Frame(main_window)
    admin_top_frame.pack(fill='x', padx=10, pady=10)
    Label(admin_top_frame, text=f"Witaj, {current_user['NAME']}!", font=("Arial",14)).pack(side=LEFT)
    Button(admin_top_frame, text="Wyloguj", command=lambda: logout(main_window), width=10, bg="lightgray").pack(side=RIGHT)

    separator = Frame(main_window, height=2, bg="gray")
    separator.pack(fill='x', padx=10, pady=(0,20))

    admin_main_frame = Frame(main_window)
    admin_main_frame.pack(expand=True)
    Button(admin_main_frame, text="Sprawdź wszystkich użytkowników", width=30, bg="#4CAF50", fg="white",
           font=("Arial",12), command=lambda: admin_users_window(main_window)).pack(pady=5)
    Button(admin_main_frame, text="Zakup leków", width=30, bg="#2196F3", fg="white",
           font=("Arial",12), command=lambda: purchase_window(main_window)).pack(pady=5)

# Wylogowanie
def logout(main_window):
    global current_user
    current_user = default_user.copy()
    login_window(main_window)

# Panel administracyjny użytkowników
def admin_users_window(main_window):
    main_window.title('Panel administracyjny użytkowników')
    main_window.geometry('900x600')
    for widget in main_window.winfo_children():
        widget.destroy()

    users_top_frame = Frame(main_window)
    users_top_frame.pack(fill=X, padx=10, pady=10)
    Label(users_top_frame, text='Szukaj użytkownika (ID, Imię/Nazwisko):').grid(row=0, column=0, sticky=W)
    search_var = StringVar()
    search_entry = Entry(users_top_frame, textvariable=search_var)
    search_entry.grid(row=0, column=1, padx=(5,20))
    set_placeholder(search_entry, 'Wpisz ID lub nazwę...')

    def on_search():
        term = search_var.get().strip()
        df = customers.customersDf.copy()
        if term and term != 'Wpisz ID lub nazwę...':
            # wyszukiwanie po ID lub NAME
            mask = df['ID'].eq(term) | df['NAME'].str.contains(term, case=False, na=False)
            df = df[mask]
        populate(df)

    Button(users_top_frame, text='Szukaj', command=on_search).grid(row=0, column=2, padx=5)
    Button(users_top_frame, text='Dodaj', command=lambda: popup('add')).grid(row=0, column=3, padx=5)
    Button(users_top_frame, text='Edytuj', command=lambda: popup('edit')).grid(row=0, column=4, padx=5)
    Button(users_top_frame, text='Usuń', command=lambda: delete_user()).grid(row=0, column=5, padx=5)
    Button(users_top_frame, text='Powrót', command=lambda: admin_window(main_window)).grid(row=0, column=6, sticky=E)

    ttk.Separator(main_window, orient='horizontal').pack(fill=X, padx=10, pady=5)
    users_bottom_frame = Frame(main_window)
    users_bottom_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
    cols = ['ID','NAME','E-MAIL','PHONE','CREATED','UPDATED']
    user_tree = ttk.Treeview(users_bottom_frame, columns=cols, show='headings')
    for col in cols:
        user_tree.heading(col, text=col)
        user_tree.column(col, width=130, anchor=W)
    vsb = Scrollbar(users_bottom_frame, orient=VERTICAL, command=user_tree.yview)
    user_tree.configure(yscrollcommand=vsb.set)
    vsb.pack(side=RIGHT, fill=Y)
    user_tree.pack(fill=BOTH, expand=True)

    def populate(df):
        user_tree.delete(*user_tree.get_children())
        for _, row in df.iterrows():
            user_tree.insert('', END, values=(
                row['ID'], row['NAME'], row['E-MAIL'], row['PHONE'], row['CREATED'], row['UPDATED']
            ))

    def popup(mode):
        sel = user_tree.focus()
        data = user_tree.item(sel)['values'] if sel else None
        win = Toplevel(main_window)
        win.title('Edycja użytkownika' if mode=='edit' else 'Dodawanie użytkownika')
        win.geometry('400x350')
        fields = ['NAME','E-MAIL','PHONE','STREET','CITY','COUNTRY']
        vars_ = {f: StringVar() for f in fields}

        # jeśli edycja, wczytaj dane z customers i address
        if mode=='edit' and data:
            user_id = data[0]
            # wczytaj podstawowe dane
            record = customers.customersDf[customers.customersDf['ID']==user_id].iloc[0]
            for f in ['NAME','E-MAIL','PHONE']:
                vars_[f].set(record[f])
            # wczytaj adres
            addr = customers.findAddress(customers.addressDf, user_id)
            for f in ['STREET','CITY','COUNTRY']:
                vars_[f].set(addr.get(f, ''))

        for f in fields:
            Label(win, text=f).pack(pady=5)
            Entry(win, textvariable=vars_[f]).pack(pady=5)

        def save():
            if mode=='add':
                customers.addCustomer(
                    customers.customersDf,
                    customers.addressDf,
                    vars_['NAME'].get(),
                    email=vars_['E-MAIL'].get(),
                    phone=vars_['PHONE'].get(),
                    street=vars_['STREET'].get(),
                    city=vars_['CITY'].get(),
                    country=vars_['COUNTRY'].get()
                )
            else:
                customers.updateCustomer(
                    customers.customersDf,
                    customers.addressDf,
                    identifier=user_id,
                    NAME=vars_['NAME'].get(),
                    email=vars_['E-MAIL'].get(),
                    phone=vars_['PHONE'].get(),
                    street=vars_['STREET'].get(),
                    city=vars_['CITY'].get(),
                    country=vars_['COUNTRY'].get()
                )
            populate(customers.customersDf)
            win.destroy()

        Button(win, text='Zapisz', command=save).pack(pady=10)

    def delete_user():
        sel = user_tree.focus()
        if sel:
            uid = user_tree.item(sel)['values'][0]
            customers.removeCustomer(customers.customersDf, customers.addressDf, identifier=uid)
            populate(customers.customersDf)

    populate(customers.customersDf.copy())

# Panel zakupów leków
def purchase_window(main_window):
    main_window.title('Zakup leków')
    main_window.geometry('800x500')
    for widget in main_window.winfo_children():
        widget.destroy()
    purchase_top_frame = Frame(main_window)
    purchase_top_frame.pack(fill=X, padx=10, pady=10)
    Button(purchase_top_frame, text='Powrót', command=lambda: admin_window(main_window) if current_user['ROLE']=='admin' else user_window(main_window), width=10).pack(side=RIGHT)
    Label(purchase_top_frame, text='Dostępne leki:', font=('Arial',12,'bold')).pack(side=LEFT)
    add_drug_btn = Button(purchase_top_frame, text='Dodaj nowy lek', command=lambda: add_drug())
    add_drug_btn.pack(side=LEFT, padx=5)
    delete_drug_btn = Button(purchase_top_frame, text='Usuń lek', command=lambda: del_drug())
    delete_drug_btn.pack(side=LEFT, padx=5)

    ttk.Separator(main_window, orient='horizontal').pack(fill=X, padx=10, pady=5)
    purchase_bottom_frame = Frame(main_window)
    purchase_bottom_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
    cols = ['ID','DRUG','ON_RECEPT','NO_PACKAGES_AVAILABLE','DATE']
    drug_tree = ttk.Treeview(purchase_bottom_frame, columns=cols, show='headings')
    for column in cols:
        drug_tree.heading(column, text=column);
        drug_tree.column(column, width=140, anchor=W)
    vsb_drug = Scrollbar(purchase_bottom_frame, orient=VERTICAL, command=drug_tree.yview)
    drug_tree.configure(yscrollcommand=vsb_drug.set);
    vsb_drug.pack(side=RIGHT, fill=Y);
    drug_tree.pack(fill=BOTH, expand=True)

    def parse_drugs_df():
        raw_df = drugs.drugsDf.copy()
        first_col = raw_df.columns[0]
        parsed_df = raw_df[first_col].str.split(',', expand=True)
        parsed_df.columns = ['ID','DRUG','ON_RECEPT','NO_PACKAGES_AVAILABLE','DATE']
        return parsed_df

    def populate_drugs(parsed_df=None):
        df = parsed_df or parse_drugs_df()
        for item in drug_tree.get_children():
            drug_tree.delete(item)
        for _, row in df.iterrows():
            drug_tree.insert('', END, values=(row['ID'],row['DRUG'],row['ON_RECEPT'],row['NO_PACKAGES_AVAILABLE'],row['DATE']))

    def add_drug():
        add_drug_window = Toplevel(main_window)
        add_drug_window.title('Dodaj lek')
        add_drug_window.geometry('300x350')
        drug_name_var = StringVar()
        prescription_required_var = BooleanVar(value=False)
        quantity_var = StringVar()
        date_var = StringVar()

        Label(add_drug_window, text='Nazwa leku').pack(pady=5)
        Entry(add_drug_window, textvariable=drug_name_var).pack(pady=5)
        Label(add_drug_window, text='Na receptę').pack(pady=5)
        prescription_frame = Frame(add_drug_window)
        prescription_frame.pack(pady=5)
        Radiobutton(prescription_frame, text='Tak', variable=prescription_required_var, value=True).pack(side=LEFT, padx=5)
        Radiobutton(prescription_frame, text='Nie', variable=prescription_required_var, value=False).pack(side=LEFT, padx=5)
        Label(add_drug_window, text='Dostępne opakowania').pack(pady=5)
        Entry(add_drug_window, textvariable=quantity_var).pack(pady=5)
        Label(add_drug_window, text='Data (YYYY-MM-DD)').pack(pady=5)
        Entry(add_drug_window, textvariable=date_var).pack(pady=5)
        date_var.set(datetime.now().strftime('%Y-%m-%d'))

        def save_new_drug():
            on_recept_val = str(prescription_required_var.get())
            qty_val = int(quantity_var.get())
            drugs.addDrug(drugs.drugsDf, drug_name_var.get(), on_recept_val, qty_val)
            populate_drugs()
            add_drug_window.destroy()
        Button(add_drug_window, text='Zapisz', command=save_new_drug).pack(pady=10)

    def del_drug():
        selected_item = drug_tree.focus()
        if selected_item:
            delete_id = drug_tree.item(selected_item)['values'][0]
            drugs.removeDrug(drugs.drugsDf, identifier=delete_id)
            populate_drugs()

    populate_drugs()

# Uruchomienie aplikacji
window = Tk()
window.title("Aplikacja")
window.geometry("400x300")
login_window(window)
window.mainloop()
