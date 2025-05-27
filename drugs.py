"""
drugs.py

Provides core drug inventory functionality:
- Add new medications
- Remove medications by name or ID
- Look up medications by name
- Append prescription usage to customer logs

Drug data is stored in an Excel sheet and handled as flat strings.
"""

import pandas as pd
from datetime import date

dateToday = date.today().strftime("%Y-%m-%d")


def addDrug(ddf, drug, rx, qty):
    """
    Adds a drug entry to the inventory.

    Args:
        ddf (pd.DataFrame): Drug data as flat string rows.
        drug (str): Drug name.
        rx (str): 'TAK' if prescription required, else 'NIE'.
        qty (int or str): Package count available.
    """
    lastRow = ddf.iloc[-1][ddf.columns[0]]
    lastID = int(str(lastRow).split(',')[0])
    val = f'{lastID+1},{drug},{rx},{qty},{dateToday}'
    ddf.loc[len(ddf)] = [val]


def removeDrug(ddf, drug=None, identifier=None):
    """
    Removes a drug entry by name or ID.

    Args:
        ddf (pd.DataFrame): Drug data.
        drug (str): Name of drug to remove.
        identifier (str or int): ID of drug to remove.

    Raises:
        Exception: If neither ID nor drug name is provided.
    """
    if identifier:
        identifier = str(identifier)
    elif drug:
        drug = drug.upper()
    else:
        raise Exception("Either identifier or drug name is required.")

    for index, row in enumerate(ddf[ddf.columns[0]].str.split(',')):
        if drug and row[1] == drug:
            ddf.drop(index, inplace=True)
        elif identifier and row[0] == identifier:
            ddf.drop(index, inplace=True)


def findDrug(ddf, drug):
    """
    Finds a drug's row index by name.

    Args:
        ddf (pd.DataFrame): Drug data.
        drug (str): Drug name to search for.

    Returns:
        int or None: Row index if found, else None.
    """
    for index, row in enumerate(ddf[ddf.columns[0]].str.split(',')):
        if row[1] == drug.upper():
            return index
    return None


def addRecept(customerID, drug, receptNumber):
    """
    Appends a prescription drug log to a customer's file.

    Args:
        customerID (str): Customer ID (file name).
        drug (str): Drug name.
        receptNumber (str): Prescription number.
    """
    with open(f'{customerID}.txt', 'a') as f:
        f.write(f'{drug.upper()}, TAK, NIE, {receptNumber}\n')
