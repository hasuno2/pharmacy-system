"""
drugs.py

This module handles drug database operations such as adding, removing,
and searching drugs, as well as recording prescription-based purchases.

Data is loaded from an Excel sheet specified in `globals.DRUGS_DB`.

Functions:
    addDrug(ddf, drug, rx, qty)
    removeDrug(ddf, drug=None, identifier=None)
    findDrug(ddf, drug)
    addRecept(customerID, drug, receptNumber)
"""

import pandas as pd
from datetime import date
import globals

dateToday = date.today().strftime("%Y-%m-%d")
drugsDf = pd.read_excel(globals.DRUGS_DB, dtype=str)


def addDrug(ddf, drug, rx, qty):
    """
    Adds a new drug entry to the drug DataFrame.

    Args:
        ddf (pd.DataFrame): The drug DataFrame.
        drug (str): The name of the drug.
        rx (str): Whether the drug requires a prescription ("TAK" or "NIE").
        qty (int or str): Quantity available.

    Raises:
        ValueError: If input values are invalid.
    """
    if not isinstance(qty, (int, str)):
        raise ValueError("Quantity must be int or str.")
    if rx not in ['TAK', 'NIE']:
        raise ValueError("rx must be either 'TAK' or 'NIE'.")

    lastRow = ddf.iloc[-1][ddf.columns[0]]
    lastID = int(str(lastRow).split(',')[0])
    val = f'{lastID+1},{drug},{rx},{qty},{dateToday}'
    ddf.loc[len(ddf)] = [val]


def removeDrug(ddf, drug=None, identifier=None):
    """
    Removes a drug from the DataFrame by its name or ID.

    Args:
        ddf (pd.DataFrame): The drug DataFrame.
        drug (str, optional): Name of the drug to remove.
        identifier (str or int, optional): ID of the drug to remove.

    Raises:
        Exception: If neither drug name nor ID is provided.
    """
    if identifier:
        identifier = str(identifier)
    elif drug:
        drug = drug.upper()
    else:
        raise Exception("Either drug name or ID must be provided.")

    for index, row in enumerate(ddf[ddf.columns[0]].str.split(',')):
        if drug and row[1] == drug:
            ddf.drop(index, inplace=True)
        elif identifier and row[0] == identifier:
            ddf.drop(index, inplace=True)


def findDrug(ddf, drug):
    """
    Finds a drug in the DataFrame by name.

    Args:
        ddf (pd.DataFrame): The drug DataFrame.
        drug (str): Name of the drug to find.

    Returns:
        int or None: Index of the drug in the DataFrame if found, else None.
    """
    for index, row in enumerate(ddf[ddf.columns[0]].str.split(',')):
        if row[1] == drug.upper():
            return index
    return None


def addRecept(customerID, drug, receptNumber):
    """
    Appends a new prescription entry to the customer’s personal file.

    Args:
        customerID (str): The customer’s unique ID.
        drug (str): Name of the drug.
        receptNumber (str): Prescription number.

    Side Effects:
        Appends a line to <customerID>.txt containing the drug, flags, and prescription number.

    Raises:
        IOError: If the customer file cannot be opened.
    """
    try:
        with open(f'{customerID}.txt', 'a') as f:
            f.write(f'{drug.upper()}, TAK, NIE, {receptNumber}\n')
    except IOError as e:
        print(f"Error writing to file for customer {customerID}: {e}")
