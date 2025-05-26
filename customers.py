"""
customers.py

This module manages customer data and associated addresses for a pharmacy system.
It supports customer registration, removal, updates, and ID lookup across CSV files.

Functions:
    addCustomer(cdf, adf, name, **kwargs)
    findCustomer(cdf, adf, **kwargs)
    removeCustomer(cdf, adf, identifier='', name='')
    updateCustomer(cdf, adf, identifier, **kwargs)
    findAddress(adf, identifier)
"""

import pandas as pd
import globals
from datetime import date
import random

customersDf = pd.read_csv(globals.CUSTOMERS_DB, dtype=str)
addressDf = pd.read_csv(globals.ADDRESS_DB, dtype=str)

columnMap = {
    'ID': 'ID',
    'name': 'NAME',
    'email': 'E-MAIL',
    'phone': 'PHONE',
    'street': 'STREET',
    'city': 'CITY',
    'country': 'COUNTRY',
}

dateToday = date.today().strftime("%Y-%m-%d")


def addCustomer(cdf, adf, name, **kwargs):
    """
    Registers a new customer and creates an associated address entry and personal file.

    Args:
        cdf (pd.DataFrame): Customer DataFrame.
        adf (pd.DataFrame): Address DataFrame.
        name (str): Name of the customer.
        **kwargs: Optional fields such as email, phone, street, city, country.

    Raises:
        ValueError: If phone number is too long.
        FileExistsError: If customer file already exists.
    """
    email = kwargs.get('email')
    phone = kwargs.get('phone')
    if phone and len(str(phone)) > 9:
        raise ValueError('Error: Phone number is too long.')

    street = kwargs.get('street')
    city = kwargs.get('city')
    country = kwargs.get('country')

    identifier = str(random.randint(1000, 9999))
    while identifier in cdf['ID'].values:
        identifier = str(random.randint(1000, 9999))

    if not phone:
        phone = 'NaN'  # fallback used in source data

    cdf.loc[len(cdf)] = [identifier, name, email, phone, dateToday, dateToday]
    adf.loc[len(adf)] = [identifier, street, city, country]

    path = f'{globals.DB_PATH}{identifier}.txt'
    try:
        with open(path, 'x') as f:
            f.write('NAME, ON_RECEPT, BOUGHT, RECEPT_NR')
    except FileExistsError:
        raise FileExistsError(f"Customer file '{path}' already exists.")


def findCustomer(cdf, adf, **kwargs):
    """
    Finds a customer ID based on one or more search criteria.

    Args:
        cdf (pd.DataFrame): Customer DataFrame.
        adf (pd.DataFrame): Address DataFrame.
        **kwargs: Keyword arguments matching fields to search by.

    Returns:
        str or None: The customer ID if found, else None.
    """
    for arg, value in kwargs.items():
        try:
            column = columnMap[arg]
            if column in cdf.columns:
                return cdf.loc[cdf[column] == value]['ID'].values[0]
            elif column in adf.columns:
                return adf.loc[adf[column] == value]['ID'].values[0]
        except (KeyError, IndexError):
            return None
    return None


def removeCustomer(cdf, adf, identifier='', name=''):
    """
    Removes a customer entry based on ID or name.

    Args:
        cdf (pd.DataFrame): Customer DataFrame.
        adf (pd.DataFrame): Address DataFrame.
        identifier (str, optional): ID of the customer.
        name (str, optional): Name of the customer.

    Raises:
        ValueError: If neither ID nor name is provided.
    """
    if identifier:
        i = cdf[cdf.ID == str(identifier)].index
    elif name:
        i = cdf[cdf.NAME == name].index
    else:
        raise ValueError("Must provide either 'identifier' or 'name' to remove a customer.")

    if i.size == 0:
        print('No customer found')
    else:
        cdf.drop(i, inplace=True)
        adf.drop(i, inplace=True)


def updateCustomer(cdf, adf, identifier, **kwargs):
    """
    Updates an existing customer's contact or address information.

    Args:
        cdf (pd.DataFrame): Customer DataFrame.
        adf (pd.DataFrame): Address DataFrame.
        identifier (str): Unique customer ID.
        **kwargs: Fields to update.

    Raises:
        Exception: If the column name is invalid or unknown.
    """
    for arg, value in kwargs.items():
        column = columnMap.get(arg)
        if not column:
            print(f'Warning: Column name "{arg}" is not present in {globals.CUSTOMERS_DB} or {globals.ADDRESS_DB}.')
            continue

        if column in cdf.columns:
            cdf.loc[cdf['ID'] == str(identifier), column] = value
        elif column in addressDf.columns:
            adf.loc[addressDf['ID'] == str(identifier), column] = value
        else:
            raise Exception(f"Column {column} not found in either customer or address data.")

    cdf.loc[cdf['ID'] == str(identifier), 'UPDATED'] = dateToday


def findAddress(adf, identifier):
    """
    Retrieves the address data for a given customer ID.

    Args:
        adf (pd.DataFrame): Address DataFrame.
        identifier (str): Unique customer ID.

    Returns:
        dict: A dictionary of address fields.
    """
    result = {}
    for column in adf.columns[1:]:
        result[column] = adf.loc[adf.ID == str(identifier), column].values[0]
    return result
