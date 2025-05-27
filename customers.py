"""
customers.py

Handles customer-related operations including:
- Adding new customers and addresses
- Searching, updating, and removing customer records
- Extracting addresses for display

Data is managed via pandas DataFrames and written to CSVs.
"""

import pandas as pd
import globals
from datetime import date
import random

# Load current data
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

dateToday = date.today().strftime("%Y-%m-%d")  # TODO: maybe make that a function


def addCustomer(cdf, adf, name, **kwargs):
    """
    Adds a new customer to the customer and address DataFrames.

    Args:
        cdf (pd.DataFrame): Customer data.
        adf (pd.DataFrame): Address data.
        name (str): Full name of the customer.
        **kwargs: Optional fields - email, phone, street, city, country.

    Raises:
        ValueError: If phone number is too long.
        FileExistsError: If customer file already exists.
    """
    email = kwargs.get('email')
    phone = kwargs.get('phone')
    if len(str(phone)) > 9:
        raise ValueError('Error: Phone number is too long.')
    if not phone:
        phone = 'NaN'

    street = kwargs.get('street')
    city = kwargs.get('city')
    country = kwargs.get('country')

    identifier = str(random.randint(1000, 9999))
    while identifier in cdf['ID'].values:
        identifier = str(random.randint(1000, 9999))

    cdf.loc[len(cdf)] = [identifier, name, email, phone, dateToday, dateToday]
    adf.loc[len(adf)] = [identifier, street, city, country]

    with open(f'{globals.DB_PATH}{identifier}.txt', 'x') as f:
        f.write('NAME, ON_RECEPT, BOUGHT, RECEPT_NR')


def findCustomer(cdf, adf, **kwargs):
    """
    Finds a customer ID based on search parameters.

    Args:
        cdf (pd.DataFrame): Customer data.
        adf (pd.DataFrame): Address data.
        **kwargs: Any searchable field (name, email, city, etc.).

    Returns:
        str or None: Matching customer ID or None.
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
    Removes a customer record.

    Args:
        cdf (pd.DataFrame): Customer data.
        adf (pd.DataFrame): Address data.
        identifier (str): ID of the customer.
        name (str): Name of the customer.

    Raises:
        Exception: If neither ID nor name is provided.
    """
    if identifier != '':
        i = cdf[cdf.ID == str(identifier)].index
    elif name != '':
        i = cdf[cdf.NAME == name].index
    else:
        raise Exception

    if i.size == 0:
        print('No customer found')
    else:
        cdf.drop(i, inplace=True)
        adf.drop(i, inplace=True)


def updateCustomer(cdf, adf, identifier, **kwargs):
    """
    Updates customer or address data by ID.

    Args:
        cdf (pd.DataFrame): Customer DataFrame.
        adf (pd.DataFrame): Address DataFrame.
        identifier (str): ID of the customer to update.
        **kwargs: Field-value pairs to update.

    Raises:
        Exception: If column name is invalid.
    """
    for arg, value in kwargs.items():
        column = columnMap[arg]
        if column:
            if column in cdf.columns:
                cdf.loc[cdf['ID'] == str(identifier), column] = value
            elif column in addressDf.columns:
                adf.loc[addressDf['ID'] == str(identifier), column] = value
            else:
                raise Exception
        else:
            print(f'Warning: Column name "{arg}" is not valid.')
    cdf.loc[cdf['ID'] == str(identifier), 'UPDATED'] = dateToday


def findAddress(adf, identifier):
    """
    Retrieves address fields for a given ID.

    Args:
        adf (pd.DataFrame): Address data.
        identifier (str): Customer ID.

    Returns:
        dict: Dictionary of address fields.
    """
    result = {}
    for column in adf.columns[1:]:
        result[column] = adf.loc[adf.ID == str(identifier), column].values[0]
    return result
