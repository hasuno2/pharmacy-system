import pandas as pd
from datetime import date
import globals

dateToday = date.today().strftime("%Y-%m-%d")  # TODO: maybe make that a function to call
drugsDf = pd.read_excel(globals.DRUGS_DB, dtype=str)
# print(drugsDf[drugsDf.columns[0]].str.split(','))
# print(drugsDf.iloc[-1][drugsDf.columns[0]].split(',')[0])
# print(drugsDf.to_string())
def addDrug(ddf, drug, rx, qty):
    # TODO: verify arguments
    lastID = int(ddf.iloc[-1][ddf.columns[0]].split(',')[0])
    val = f'{lastID+1},{drug},{rx},{qty},{dateToday}'
    ddf.loc[len(ddf)] = [val]
# addDrug('ASPIRIN', 'NO', 439)
# print(drugsDf.to_string())
def removeDrug(ddf, drug=None, identifier=None):
    if identifier:
        identifier = str(identifier)
    elif drug:
        drug = drug.upper()
    else:
        raise Exception
    for index, row in enumerate(ddf[ddf.columns[0]].str.split(',')):
        if drug:
            if row[1] == drug:
                ddf.drop(index, inplace=True)
        else:
            if row[0] == identifier:
                ddf.drop(index, inplace=True)
def findDrug(ddf, drug):
    for index, row in enumerate(ddf[ddf.columns[0]].str.split(',')):
        if row[1] == drug.upper():
            return index
    return None
def addRecept(customerID, drug, receptNumber):
    with open(f'{customerID}.txt', 'a') as f:
        f.write(f'{drug.upper()}, TAK, NIE, {receptNumber}')
