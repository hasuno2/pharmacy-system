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
    login_var = StringVar()
    password_var = StringVar()

    Label(registration_frame, text="Imię").grid(row=0, column=0, padx=10, pady=5)
    first_name_entry = Entry(registration_frame, textvariable=first_name_var)
    first_name_entry.grid(row=0, column=1, padx=10, pady=5)
    set_placeholder(first_name_entry, "Wpisz imię")

    Label(registration_frame, text="Nazwisko").grid(row=1, column=0, padx=10, pady=5)
    last_name_entry = Entry(registration_frame, textvariable=last_name_var)
    last_name_entry.grid(row=1, column=1, padx=10, pady=5)
    set_placeholder(last_name_entry, "Wpisz nazwisko")

    Label(registration_frame, text="Login").grid(row=2, column=0, padx=10, pady=5)
    login_entry = Entry(registration_frame, textvariable=login_var)
    login_entry.grid(row=2, column=1, padx=10, pady=5)
    set_placeholder(login_entry, "Wpisz login")

    Label(registration_frame, text="Hasło").grid(row=3, column=0, padx=10, pady=5)
    password_entry = Entry(registration_frame, textvariable=password_var)
    password_entry.grid(row=3, column=1, padx=10, pady=5)
    set_placeholder(password_entry, "Wpisz hasło", is_password=True)

    def register_user():
        login_window(main_window)

    Button(registration_frame, text="Rejestruj", command=register_user).grid(row=4, column=0, columnspan=2, pady=10)
    Button(registration_frame, text="Powrót", command=lambda: login_window(main_window)).grid(row=5, column=0, columnspan=2)

# Okno logowania
def login_window(main_window):
    for widget in main_window.winfo_children():
        widget.destroy()
    main_window.title("Logowanie")
    login_frame = Frame(main_window)
    login_frame.place(relx=0.5, rely=0.5, anchor=CENTER)

    Label(login_frame, text="Login").grid(row=0, column=0, padx=10, pady=5)
    email_entry = Entry(login_frame)
    email_entry.grid(row=0, column=1, padx=10, pady=5)
    set_placeholder(email_entry, "Wpisz login")

    Label(login_frame, text="Hasło").grid(row=1, column=0, padx=10, pady=5)
    password_entry = Entry(login_frame)
    password_entry.grid(row=1, column=1, padx=10, pady=5)
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

    Button(login_frame, text="Logowanie", command=attempt_login).grid(row=2, column=0, columnspan=2, pady=5)
    Button(login_frame, text="Rejestracja", command=lambda: registration_window(main_window)).grid(row=3, column=0, columnspan=2)

# Okno użytkownika
def user_window(main_window):
    for widget in main_window.winfo_children():
        widget.destroy()
    user_frame = Frame(main_window, padx=20, pady=20)
    user_frame.pack(fill=BOTH, expand=True)

    Label(user_frame, text=f"Witaj, {current_user['NAME']}!", font=("Arial",16)).grid(row=0, column=0, sticky=W)
    Button(user_frame, text="Wyloguj", width=12, command=lambda: logout(main_window)).grid(row=0, column=1, sticky=E, padx=10)
    user_frame.grid_columnconfigure(0, weight=1)
    user_frame.grid_columnconfigure(1, weight=1)

    Button(user_frame, text="Zakup leków →", font=("Arial",14), relief=RAISED, bd=3, padx=10, pady=5,
           command=lambda: purchase_window(main_window)).grid(row=1, column=0, columnspan=2, pady=(30,0))

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
    Label(users_top_frame, text='Szukaj użytkownika (Imię/Nazwisko):').grid(row=0, column=1, sticky=W)
    search_entry = Entry(users_top_frame)
    search_entry.grid(row=0, column=2, padx=(5,20))
    set_placeholder(search_entry, 'Wpisz nazwę...')
    def on_search():
        search_term = search_entry.get().strip()
        df_copy = customers.customersDf.copy()
        if search_term and search_term!='Wpisz nazwę...':
            df_copy = df_copy[df_copy['NAME'].str.contains(search_term, case=False, na=False)]
        populate(df_copy)
    Button(users_top_frame, text='Szukaj', command=on_search).grid(row=0, column=3, padx=5)
    Button(users_top_frame, text='Dodaj', command=lambda: popup('add')).grid(row=0, column=4, padx=5)
    Button(users_top_frame, text='Edytuj', command=lambda: popup('edit')).grid(row=0, column=5, padx=5)
    Button(users_top_frame, text='Usuń', command=lambda: delete_user()).grid(row=0, column=6, padx=5)
    Button(users_top_frame, text='Powrót', command=lambda: admin_window(main_window)).grid(row=0, column=7, sticky=E)

    ttk.Separator(main_window, orient='horizontal').pack(fill=X, padx=10, pady=5)
    users_bottom_frame = Frame(main_window)
    users_bottom_frame.pack(fill=BOTH, expand=True, padx=10, pady=5)
    cols = ['ID','NAME','E-MAIL','PHONE','CREATED','UPDATED']
    user_tree = ttk.Treeview(users_bottom_frame, columns=cols, show='headings')
    for col in cols:
        user_tree.heading(col, text=col);
        user_tree.column(col, width=130, anchor=W)
    vsb = Scrollbar(users_bottom_frame, orient=VERTICAL, command=user_tree.yview)
    user_tree.configure(yscrollcommand=vsb.set);
    vsb.pack(side=RIGHT, fill=Y);
    user_tree.pack(fill=BOTH, expand=True)

    def populate(df):
        for item in user_tree.get_children():
            user_tree.delete(item)
        for _, row in df.iterrows():
            user_tree.insert('', END, values=(row['ID'],row['NAME'],row['E-MAIL'],row['PHONE'],row['CREATED'],row['UPDATED']))

    def popup(mode):
        selection = user_tree.focus()
        values = user_tree.item(selection)['values'] if selection else None
        popup_window = Toplevel(main_window)
        popup_window.title('Edycja' if mode=='edit' else 'Dodaj użytkownika')
        popup_window.geometry('400x300')
        fields = ['NAME','E-MAIL','PHONE']
        vars_dict = {f: StringVar() for f in fields}
        for field in fields:
            Label(popup_window, text=field).pack(pady=5)
            Entry(popup_window, textvariable=vars_dict[field]).pack(pady=5)
            if mode=='edit' and values:
                vars_dict[field].set(values[cols.index(field)])
        def save_user():
            if mode=='add':
                customers.addCustomer(customers.customersDf, customers.addressDf,
                                      vars_dict['NAME'].get(), email=vars_dict['E-MAIL'].get(), phone=vars_dict['PHONE'].get())
            else:
                customers.updateCustomer(customers.customersDf, customers.addressDf,
                                         identifier=values[0], name=vars_dict['NAME'].get(),
                                         email=vars_dict['E-MAIL'].get(), phone=vars_dict['PHONE'].get())
            populate(customers.customersDf)
            popup_window.destroy()
        Button(popup_window, text='Zapisz', command=save_user).pack(pady=10)

    def delete_user():
        selected = user_tree.focus()
        if selected:
            delete_id = user_tree.item(selected)['values'][0]
            customers.removeCustomer(customers.customersDf, customers.addressDf, identifier=delete_id)
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
