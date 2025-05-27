"""
main.py

Entry point for the pharmacy management GUI.

Displays:
- Login screen (placeholder logic)
- Main window with customer list
- Form to view and edit customer data

Customer and address data are loaded from CSV files.
"""

import csv
import pandas as pd
import os
import drugs
import customers
import globals
from tkinter import *
from tkinter import ttk
from tkinter import END

# Load data
drugsDf = pd.read_excel(globals.DRUGS_DB, dtype=str)
customersDf = pd.read_csv(globals.CUSTOMERS_DB, dtype=str)
addressDf = pd.read_csv(globals.ADDRESS_DB, dtype=str)

currentEntryValues = {
    'ID': None, 'NAME': None, 'E-MAIL': None, 'PHONE': None,
    'STREET': None, 'CITY': None, 'COUNTRY': None
}

FONT = ('calibre', 10)


def login(usernameEntry, passwordEntry, loginWindow):
    """
    Placeholder login function. Immediately launches main window.

    Args:
        usernameEntry (tk.Entry): Username field.
        passwordEntry (tk.Entry): Password field.
        loginWindow (tk.Tk): Login window to destroy.
    """
    username = usernameEntry.get()
    password = passwordEntry.get()
    loginWindow.destroy()
    runMainWindow()


def listCustomers(cdf):
    """
    Converts customer DataFrame into list of display dictionaries.

    Args:
        cdf (pd.DataFrame): Customer data.

    Returns:
        list[dict]: List of formatted customer entries.
    """
    customersList = []
    for index, row in cdf.iterrows():
        customersList.append({
            'ID': row['ID'],
            'Name': row['NAME'],
            'E-Mail': row['E-MAIL'],
            'Phone': row['PHONE']
        })
    return customersList


def runMainWindow():
    """
    Displays the main window with a customer table, editor form,
    and update button functionality.
    """
    def onTreeSelect(event):
        """
        Populates form fields from the selected row in the TreeView.
        """
        global currentEntryValues
        selectedItem = customersListTree.selection()
        if selectedItem:
            item_id = selectedItem[0]
            values = customersListTree.item(item_id, "values")
            address = customers.findAddress(addressDf, values[0])
            for j, k in enumerate(list(currentEntryValues.keys())[:3]):
                currentEntryValues[k] = values[j]
            currentEntryValues |= address
            for j in range(7):
                entries[j].delete(0, END)
                entries[j].insert(0, str(list(currentEntryValues.values())[j]))

    def saveCustomer():
        """
        Saves the currentEntryValues into both CSV dataframes.
        """
        global currentEntryValues
        customers.updateCustomer(customersDf, addressDf,
            identifier=currentEntryValues['ID'],
            name=currentEntryValues['NAME'],
            email=currentEntryValues['E-MAIL'],
            phone=currentEntryValues['PHONE'],
            street=currentEntryValues['STREET'],
            city=currentEntryValues['CITY'],
            country=currentEntryValues['COUNTRY']
        )
        print(customersDf)
        print(addressDf)

    mainWindow = Tk()
    mainWindow.geometry('1024x768')

    # --- Customer Tree List
    customersTreeColumns = ['ID', 'Name', 'E-Mail', 'Phone']
    customersListTree = ttk.Treeview(mainWindow, columns=customersTreeColumns, show='headings', height=5)
    for col in customersTreeColumns:
        customersListTree.heading(col, text=col)
        customersListTree.column(col, anchor='center', width=200)
    for item in listCustomers(customersDf):
        customersListTree.insert('', END, values=[item[col] for col in customersTreeColumns])
    customersTreeScroll = ttk.Scrollbar(mainWindow, orient='vertical', command=customersListTree.yview)
    customersListTree.configure(yscrollcommand=customersTreeScroll.set)
    customersListTree.grid(row=0, column=0, sticky='nsew')
    customersTreeScroll.grid(row=0, column=1, sticky='ns')

    # --- Customer Control Buttons
    cButtonsFrame = Frame(mainWindow)
    cButtonsFrame.grid(row=1, column=0, pady=10)
    btnAdd = Button(cButtonsFrame, text='Dodaj')
    btnEdit = Button(cButtonsFrame, text='Edytuj', command=saveCustomer)
    btnDelete = Button(cButtonsFrame, text='Usun')
    btnAdd.pack(side='left', padx=5)
    btnEdit.pack(side='left', padx=5)
    btnDelete.pack(side='left', padx=5)

    # --- Customer Data Fields
    entryFrame = Frame(mainWindow)
    entryFrame.grid(row=2, column=0, pady=10)
    entries = []
    entryNames = ['ID', 'Name', 'E-Mail', 'Phone', 'Street', 'City', 'Country']
    for name in entryNames:
        subframe = ttk.Frame(entryFrame)
        subframe.pack(side='left', padx=5)
        label = ttk.Label(subframe, text=f'{name}')
        label.pack()
        entry = ttk.Entry(subframe, width=16)
        entry.pack()
        entries.append(entry)

    customersListTree.bind("<<TreeviewSelect>>", onTreeSelect)
    mainWindow.mainloop()


def runLoginWindow():
    """
    Shows the login form with username/password and a login button.
    """
    loginWindow = Tk()
    loginWindow.geometry('300x300')
    usernameLabel = Label(loginWindow, text='Username', font=FONT)
    usernameEntry = Entry(loginWindow, font=FONT)
    passwordLabel = Label(loginWindow, text='Password', font=FONT)
    passwordEntry = Entry(loginWindow, font=FONT, show='*')
    submitButton = Button(loginWindow, text='Submit', font=FONT, command=lambda: login(usernameEntry, passwordEntry, loginWindow))
    usernameLabel.grid(row=0, column=0, padx=10, pady=10)
    usernameEntry.grid(row=1, column=0, padx=10, pady=10)
    passwordLabel.grid(row=2, column=0, padx=10, pady=10)
    passwordEntry.grid(row=3, column=0, padx=10, pady=10)
    submitButton.grid(row=4, column=0, padx=10, pady=10)
    loginWindow.mainloop()


def __main__():
    """Main function to boot the GUI app."""
    runLoginWindow()


if __name__ == '__main__':
    __main__()
