"""
main.py

This is the main module that launches the GUI for managing the pharmacy system.
It provides login functionality and an interface for viewing and editing customer records.

Functions:
    __main__(): Entry point for the application.
    runLoginWindow(): Displays the login screen (currently no auth logic).
    runMainWindow(): Displays the main pharmacy administration window.
    listCustomers(cdf): Returns a list of customer data dictionaries.
    login(usernameEntry, passwordEntry, loginWindow): Handles login button logic.
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

drugsDf = pd.read_excel(globals.DRUGS_DB, dtype=str)
customersDf = pd.read_csv(globals.CUSTOMERS_DB, dtype=str)
addressDf = pd.read_csv(globals.ADDRESS_DB, dtype=str)
currentEntryValues = {'ID': None, 'NAME': None, 'E-MAIL': None, 'PHONE': None, 'STREET': None, 'CITY': None, 'COUNTRY': None}

FONT = ('calibre', 10)
def login(usernameEntry, passwordEntry, loginWindow):
    username = usernameEntry.get()
    password = passwordEntry.get()
    ## TODO: check credentials, disabled for testing
    loginWindow.destroy()
    runMainWindow()
def listCustomers(cdf):
    customersList = []
    for index, row in cdf.iterrows():
        # print(row)
        customersList.append({'ID': row['ID'], 'Name': row['NAME'], 'E-Mail': row['E-MAIL'], 'Phone': row['PHONE']})
    return customersList

def runMainWindow():
    def updateFrameSize(event, frame=None):
        windowHeight = mainWindow.winfo_height()
        windowWidth = mainWindow.winfo_width()
        frame.configure(width=windowWidth // 2, height=windowHeight)
        frame.place(x=windowWidth // 2, y=0)
    def onTreeSelect(event):
        global currentEntryValues
        selectedItem = customersListTree.selection()
        if selectedItem:
            item_id = selectedItem[0]
            values = customersListTree.item(item_id, "values")
            ## Filling entry values for selected customer
            address = customers.findAddress(addressDf, values[0])
            for j, k in enumerate(list(currentEntryValues.keys())[:3]):
                currentEntryValues[k] = values[j]
            currentEntryValues |= address
            for j in range(7):
                entries[j].delete(0, END)
                entries[j].insert(0, str(list(currentEntryValues.values())[j]))
    def saveCustomer():
        global currentEntryValues
        customers.updateCustomer(customersDf, addressDf,
            identifier = currentEntryValues['ID'],
            name = currentEntryValues['NAME'],
            email = currentEntryValues['E-MAIL'],
            phone = currentEntryValues['PHONE'],
            street = currentEntryValues['STREET'],
            city = currentEntryValues['CITY'],
            country = currentEntryValues['COUNTRY']
        )
        print(customersDf)
        print(addressDf)
    mainWindow = Tk()
    mainWindow.geometry('1024x768')


    #### Customers Tree List
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

    #### Customers Edit Buttons
    cButtonsFrame = Frame(mainWindow)
    cButtonsFrame.grid(row=1, column=0, pady=10)
    btnAdd = Button(cButtonsFrame, text='Dodaj')
    btnEdit = Button(cButtonsFrame, text='Edytuj', command=saveCustomer)
    btnDelete = Button(cButtonsFrame, text='Usun')
    btnAdd.pack(side='left', padx=5)
    btnEdit.pack(side='left', padx=5)
    btnDelete.pack(side='left', padx=5)

    #### Customers Data Editing
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

    # mainWindow.bind('<Configure>', updateFrameSize(frame=mainFrame))
    customersListTree.bind("<<TreeviewSelect>>", onTreeSelect)
    mainWindow.mainloop()

def runLoginWindow():
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
    runLoginWindow()

if __name__ == '__main__':
    __main__()
