import re
import json
import os
from datetime import datetime

user_expenses_format = {
    "personal_expenses": [],
    "group_expenses": []
}

commands = {
    'menu': 'Display this menu',
    'add': 'Record/Add a new spending',
    'addGroup': 'Add a group expense',
    'display': 'Show sum of expenditure for the current day/month',
    'history': 'Display spending history',
    'erase': 'Clear/Erase all your records',
    'profile': 'Manage your user profile'
}

dateFormat = '%d-%b-%Y'
timeFormat = '%H:%M'
monthFormat = '%b-%Y'

config = configparser.ConfigParser()
configFileName = "config.ini"


def setConfig():
    config["Files"] = {
        "UserExpenses": "user_expenses.json",
        "GroupExpenses": "group_expenses.json",
        "UserProfile": "user_emails.json"
    }
    config["Settings"] = {
        "ApiToken": "",
        "ExpenseCategories": ['Food', 'Groceries', 'Utilities', 'Transport', 'Shopping', 'Miscellaneous'],
        "ExpenseChoices": ['Date', 'Category', 'Cost'],
        "DisplayChoices": ['Day', 'Month']
    }

    with open(configFileName, 'w+') as configfile:
        config.write(configfile)


def loadConfig():
    config.read(configFileName)


def getUserExpensesFile():
    filename = config['Files']['UserExpenses']
    return os.path.join("data", filename)


def getGroupExpensesFile():
    filename = config['Files']['GroupExpenses']
    return os.path.join("data", filename)


def getUserProfileFile():
    filename = config['Files']['UserProfile']
    return os.path.join("data", filename)


def read_json(filename):
    try:
        if not os.path.exists(filename):
            with open(filename, 'w') as json_file:
                json_file.write('{}')
            return json.dumps('{}')
        elif os.stat(filename).st_size != 0:
            with open(filename) as file:
                file_data = json.load(file)
            return file_data

    except FileNotFoundError:
        print("---------NO RECORDS FOUND---------")


def write_json(file_data, filename):
    try:
        with open(filename, 'w') as json_file:
            json.dump(file_data, json_file, ensure_ascii=False, indent=4)
    except FileNotFoundError:
        print('Sorry, the data file could not be found.')


def validate_entered_amount(amount_entered):
    if amount_entered is None:
        return 0
    if re.match("^[1-9][0-9]{0,14}\\.[0-9]*$", amount_entered) or re.match("^[1-9][0-9]{0,14}$", amount_entered):
        amount = round(float(amount_entered), 2)
        if amount > 0:
            return str(amount)
    return 0


def getUserHistory(chat_id):
    user_list = read_json(getUserExpensesFile())
    if user_list is None:
        return None
    chat_id = str(chat_id)
    if chat_id in user_list:
        return user_list[chat_id]
    return None


def createNewUserRecord():
    return user_expenses_format


def getSpendCategories():
    return config['Settings']['ExpenseCategories']


def getSpendDisplayOptions():
    return config['Settings']['DisplayChoices']


def getCommands():
    return commands


def getDateFormat():
    return dateFormat


def getTimeFormat():
    return timeFormat


def getMonthFormat():
    return monthFormat


def getChoices():
    return config['Settings']['ExpenseChoices']
