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
    global customersDf, addressDf
    def updateFrameSize(event, frame=None):
        windowHeight = mainWindow.winfo_height()
        windowWidth = mainWindow.winfo_width()
        frame.configure(width=windowWidth // 2, height=windowHeight)
        frame.place(x=windowWidth // 2, y=0)
    def onTreeSelect(event):
        global currentEntryValues
        global customersDf, addressDf
        selectedItem = customersListTree.selection()
        if selectedItem:
            item_id = selectedItem[0]
            values = customersListTree.item(item_id, "values")
            ## Filling entry values for selected customer
            address = customers.findAddress(addressDf, values[0])
            for j, k in enumerate(list(currentEntryValues.keys())[:4]):
                currentEntryValues[k] = values[j]
            currentEntryValues |= address
            for j in range(7):
                entries[j].delete(0, END)
                entries[j].insert(0, str(list(currentEntryValues.values())[j]))
    def clearSelection(event=None):
        customersListTree.selection_remove(customersListTree.selection())
        customersListTree.focus('')
        for e in entries:
            e.delete(0, END)
        refreshInputDict()
    def refreshTree():
        global customersDf, addressDf
        for row in customersListTree.get_children():
            customersListTree.delete(row)
        for customer in listCustomers(customersDf):
            customersListTree.insert('', 'end', values=[customer[column] for column in customersTreeColumns])
    def refreshInputDict():
        global currentEntryValues
        for i, key in enumerate(list(currentEntryValues.keys())):
            currentEntryValues[key] = entries[i].get()
    def saveCustomer(addNew=False):
        global currentEntryValues
        global customersDf
        global addressDf
        ## TODO: Select the customer back
        refreshInputDict()
        if not addNew:
            #customersDf, addressDf = (
            customers.updateCustomer(customersDf, addressDf,
                identifier = currentEntryValues['ID'],
                name = currentEntryValues['NAME'],
                email = currentEntryValues['E-MAIL'],
                phone = currentEntryValues['PHONE'],
                street = currentEntryValues['STREET'],
                city = currentEntryValues['CITY'],
                country = currentEntryValues['COUNTRY']
            )
        else:
            customers.addCustomer(customersDf, addressDf,
                identifier = currentEntryValues['ID'],
                name=currentEntryValues['NAME'],
                email=currentEntryValues['E-MAIL'],
                phone=currentEntryValues['PHONE'],
                street=currentEntryValues['STREET'],
                city=currentEntryValues['CITY'],
                country=currentEntryValues['COUNTRY']
            )
            print(addressDf)
        refreshTree()
    def removeSelectedCustomer():
        global customersDf, addressDf
        global currentEntryValues
        refreshInputDict()
        customers.removeCustomer(customersDf, addressDf, identifier=currentEntryValues['ID'])
        refreshTree()

    mainWindow = Tk()
    mainWindow.geometry('1024x768')


    #### Customers Tree List
    customersTreeColumns = ['ID', 'Name', 'E-Mail', 'Phone']
    customersListTree = ttk.Treeview(mainWindow, columns=customersTreeColumns, show='headings', height=5)
    for col in customersTreeColumns:
        customersListTree.heading(col, text=col)
        customersListTree.column(col, anchor='center', width=200)
    refreshTree()
    customersTreeScroll = ttk.Scrollbar(mainWindow, orient='vertical', command=customersListTree.yview)
    customersListTree.configure(yscrollcommand=customersTreeScroll.set)
    customersListTree.grid(row=0, column=0, sticky='nsew')
    customersTreeScroll.grid(row=0, column=1, sticky='ns')

    #### Customers Edit Buttons
    cButtonsFrame = Frame(mainWindow)
    cButtonsFrame.grid(row=1, column=0, pady=10)
    btnAdd = Button(cButtonsFrame, text='Dodaj', command=lambda: saveCustomer(addNew=True))
    btnEdit = Button(cButtonsFrame, text='Edytuj', command=saveCustomer)
    btnDelete = Button(cButtonsFrame, text='Usun', command=removeSelectedCustomer)
    btnAdd.pack(side='left', padx=5)
    btnEdit.pack(side='left', padx=5)
    btnDelete.pack(side='left', padx=5)

    #### Customers Data Editing
    entryFrame = Frame(mainWindow)
    entryFrame.grid(row=2, column=0, pady=10)
    entries = []
    ## TODO: Maybe add a hovering tooltip to remind that ID is ignored when registering a new user
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
    customersListTree.bind("<Button-3>", clearSelection)
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
