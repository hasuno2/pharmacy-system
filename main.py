import csv
import pandas as pd
import os
import drugs
import customers
import globals
from tkinter import *
from tkinter import ttk
from tkinter import END
from tkinter import messagebox

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
def listDrugs(ddf):
    drugsList = []
    for index, row in enumerate(ddf[ddf.columns[0]].str.split(',')):
        drugsList.append({'ID': row[0], 'Drug': row[1], 'On Recept': row[2], 'Packages Available': row[3]})
    return drugsList

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
            values = customersListTree.item(item_id, 'values')
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
    def refreshDTree():
        global drugsDf
        for row in drugsListTree.get_children():
            drugsListTree.delete(row)
        for drug in listDrugs(drugsDf):
            drugsListTree.insert('', 'end', values=[drug[column] for column in drugsTreeColumns])
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
        if currentEntryValues['NAME'] != '':
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
        else:
            messagebox.showerror('Error', 'Proszę podać poprawne dane klienta.')
        refreshTree()
    def removeSelectedCustomer():
        global customersDf, addressDf
        global currentEntryValues
        refreshInputDict()
        customers.removeCustomer(customersDf, addressDf, identifier=currentEntryValues['ID'])
        refreshTree()
    def onReceptClicked(choice):
        rSelected.set(choice)
        if choice == "YES":
            btnYes.config(relief='sunken')
            btnNo.config(relief='raised')
        else:
            btnYes.config(relief='raised')
            btnNo.config(relief='sunken')
    def addNewDrug():
        global drugsDf
        ## TODO: Sanitize inputs???
        drugName = entries2[0].get().upper()
        if drugName == '':
            messagebox.showerror('Error', 'Proszę podać właściwą nazwę leku.')
        drugBool = rSelected.get()
        try:
            drugQty = str(int(entries2[1].get()))
            if drugName != '':
                drugs.addDrug(drugsDf, drugName, drugBool, drugQty)
        except ValueError:
            messagebox.showerror('Error', 'Proszę podać właściwą ilość leku na stanie.')
        refreshDTree()
    def removeDrug():
        ## TODO: exception handling when removing sometimes and adding after removing all
        global drugsDf
        selectedDrug = drugsListTree.selection()[0]
        selectedDrugID = drugsListTree.item(selectedDrug, 'values')[0]
        drugs.removeDrug(drugsDf, identifier=int(selectedDrugID))
        refreshDTree()
    def removeByParam(drug=False):
        global customersDf, addressDf
        topWindow = Toplevel(mainWindow)
        topWindow.title('Usuwanie po parametrze')
        topWindow.geometry('300x200')

        Label(topWindow, text='ID:').pack(pady=10)
        entry1 = Entry(topWindow)
        entry1.pack()

        Label(topWindow, text='Imie / Nazwa').pack(pady=10)
        entry2 = Entry(topWindow)
        entry2.pack()
        def submit():
            try:
                value1 = int(entry1.get())
                value2 = entry2.get()
                if value1 == '':
                    customers.removeCustomer(customersDf, addressDf, name=value2)
                elif value2 == '':
                    customers.removeCustomer(customersDf, addressDf, identifier=value1)
                else:
                    messagebox.showerror('Error', 'Wypełnij jedno z dwóch pól.')
            except ValueError:
                messagebox.showerror('Error', 'Nie znaleziono klienta.')
            refreshTree()
            topWindow.destroy()
        Button(topWindow, text="Ok", command=submit).pack(pady=20)
    mainWindow = Tk()
    mainWindow.geometry('1024x768')


    #### Customers Tree List
    customersTreeColumns = ['ID', 'Name', 'E-Mail', 'Phone']
    customersListTree = ttk.Treeview(mainWindow, columns=customersTreeColumns, show='headings', height=8)
    for col in customersTreeColumns:
        customersListTree.heading(col, text=col)
        customersListTree.column(col, anchor='center', width=200)
    refreshTree()
    customersTreeScroll = ttk.Scrollbar(mainWindow, orient='vertical', command=customersListTree.yview)
    customersListTree.configure(yscrollcommand=customersTreeScroll.set)
    customersListTree.grid(row=0, column=0, sticky='nsew')
    customersTreeScroll.grid(row=0, column=1, sticky='ns')

    #### Customers Data Editing
    entryFrame = Frame(mainWindow)
    entryFrame.grid(row=1, column=0, pady=10)
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

    #### Customers Edit Buttons
    cButtonsFrame = Frame(mainWindow)
    cButtonsFrame.grid(row=2, column=0, pady=10)
    btnAdd = Button(cButtonsFrame, text='Dodaj', command=lambda: saveCustomer(addNew=True))
    btnEdit = Button(cButtonsFrame, text='Edytuj', command=saveCustomer)
    btnDelete = Button(cButtonsFrame, text='Usuń', command=removeSelectedCustomer)
    btnDeleteByParam = Button(cButtonsFrame, text='Usuń po parametrze', command=removeByParam)
    btnAdd.pack(side='left', padx=5)
    btnEdit.pack(side='left', padx=5)
    btnDelete.pack(side='left', padx=5)
    btnDeleteByParam.pack(side='left', padx=5)

    #### Drug Tree
    drugsTreeColumns = ['ID', 'Drug', 'On Recept', 'Packages Available']
    drugsListTree = ttk.Treeview(mainWindow, columns=drugsTreeColumns, show='headings', height=8)
    for col in drugsTreeColumns:
        drugsListTree.heading(col, text=col)
        drugsListTree.column(col, anchor='center', width=200)
    refreshDTree()
    drugsTreeScroll = ttk.Scrollbar(mainWindow, orient='vertical', command=drugsListTree.yview)
    drugsListTree.configure(yscrollcommand=drugsTreeScroll.set)
    drugsListTree.grid(row=3, column=0, pady=5, sticky='nsew')
    drugsTreeScroll.grid(row=3, column=1, pady=5, sticky='ns')

    #### Drug Data Entry
    entryFrame2 = Frame(mainWindow)
    entryFrame2.grid(row=4, column=0, ipady=10)
    entries2 = []
    entryNames2 = ['Drug', 'On Recept', 'Packages Available']
    rSelected = StringVar(value='NO')

    for name in entryNames2:
        subframe = ttk.Frame(entryFrame2)
        subframe.pack(side='left', padx=5)

        label = ttk.Label(subframe, text=f'{name}')
        label.pack()

        if name == 'On Recept':
            # Create a frame to hold the two buttons side by side
            buttonFrame = ttk.Frame(subframe)
            buttonFrame.pack()

            btnYes = Button(buttonFrame, text="Tak", command=lambda: onReceptClicked('YES'))
            btnNo = Button(buttonFrame, text="Nie", command=lambda: onReceptClicked('NO'))
            btnYes.pack(side='left', padx=4)
            btnNo.pack(side='left', padx=4)

            btnYes.config(relief='raised')
            btnNo.config(relief='sunken')
        else:
            entry = ttk.Entry(subframe, width=16)
            entry.pack()
            entries2.append(entry)

    #### Drug Edit Buttons
    ## TODO: Add drug qty editing
    dButtonsFrame = Frame(mainWindow)
    dButtonsFrame.grid(row=5, column=0)
    btnAdd2 = Button(dButtonsFrame, text='Dodaj', command=addNewDrug)
    btnDelete2 = Button(dButtonsFrame, text='Usuń', command=removeDrug)
    btnDeleteByParam2 = Button(dButtonsFrame, text='Usuń po parametrze', command=lambda: removeByParam(True))
    btnAdd2.pack(side='left', padx=5)
    btnDelete2.pack(side='left', padx=5)
    btnDeleteByParam2.pack(side='left', padx=5)

    # mainWindow.bind('<Configure>', updateFrameSize(frame=mainFrame))
    customersListTree.bind('<<TreeviewSelect>>', onTreeSelect)
    customersListTree.bind('<Button-3>', clearSelection)
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
