import pandas as pd
import globals
from datetime import date
import random

customersDf = pd.read_csv(globals.CUSTOMERS_DB, dtype=str)
addressDf = pd.read_csv(globals.ADDRESS_DB, dtype=str)
# print(customersDf.to_string())
# print(addressDf.to_string())
columnMap = {
    'ID': 'ID',
    'name': 'NAME',
    'email': 'E-MAIL',
    'phone': 'PHONE',
    'street': 'STREET',
    'city': 'CITY',
    'country': 'COUNTRY',
}
dateToday = date.today().strftime("%Y-%m-%d")  # TODO: maybe make that a function to call


def addCustomer(cdf, adf, name, **kwargs):
    # TODO: add exceptions for wrong string lengths etc.
    # TODO: reform kwargs handling
    email = kwargs.get('email')
    phone = kwargs.get('phone')
    if len(str(phone)) > 9:
        raise ValueError('Error: Phone number is too long.')
    street = kwargs.get('street')
    city = kwargs.get('city')
    country = kwargs.get('country')
    identifier = str(random.randint(1000, 9999))
    while identifier in cdf['ID'].values:
        identifier = str(random.randint(1000, 9999))
    if not phone: phone = 'NaN' # it's set that way in the example file, and it's the only number there, so ig it makes sense?
    cdf.loc[len(cdf)] = [identifier, name, email, phone, dateToday, dateToday]
    adf.loc[len(adf)] = [identifier, street, city, country]
    # TODO: exception if file exists
    with open(f'{globals.DB_PATH}{identifier}.txt', 'x') as f:
        f.write('NAME, ON_RECEPT, BOUGHT, RECEPT_NR')
        f.close()


def findCustomer(cdf, adf, **kwargs):
    for arg, value in kwargs.items():
        try:
            column = columnMap[arg]
            if column in cdf.columns:
                return cdf.loc[cdf[column] == value]['ID'].values[0]
            elif column in adf.columns:
                return adf.loc[adf[column] == value]['ID'].values[0]
        except (KeyError, IndexError): return None
    return None


def removeCustomer(cdf, adf, identifier='', name=''):
    # finding dataframe id of the person
    if identifier != '':
        i = cdf[cdf.ID == str(identifier)].index
    elif name != '':
        i = cdf[cdf.NAME == name].index
    else:
        # no id or name to delete
        raise Exception
    if i.size == 0:
        print('No customer found')
    else:
        cdf.drop(i, inplace=True)
        adf.drop(i, inplace=True)


def updateCustomer(cdf, adf, identifier, **kwargs):
    for arg, value in kwargs.items():
        column = columnMap[arg] # possible exception
        if column:
            if column in cdf.columns:
                cdf.loc[cdf['ID'] == str(identifier), column] = value
            elif column in addressDf.columns:
                adf.loc[adf['ID'] == str(identifier), column] = value
            else:
                # not possible I think
                raise Exception
        else:
            print(f'Warning: Column name "{arg}" is not present in {globals.CUSTOMERS_DB} or {globals.ADDRESS_DB}.')
    cdf.loc[cdf['ID'] == str(identifier), 'UPDATED'] = dateToday
    # return cdf, adf

def findAddress(adf, identifier):
    result = {}
    for column in adf.columns[1:]:
        result[column] = adf.loc[adf.ID == str(identifier), column].values[0]
    return result