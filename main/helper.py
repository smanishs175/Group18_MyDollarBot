import re
import json
import os
from datetime import datetime
import configparser
from telebot_calendar import Calendar, CallbackData, ENGLISH_LANGUAGE
from telebot.types import ReplyKeyboardRemove, CallbackQuery

#calendar initialized
calendar = Calendar(language=ENGLISH_LANGUAGE)
calendar_1_callback = CallbackData("calendar_1", "action", "year", "month", "day")

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


# categories and options
date_range = []
spend_display_option = ['All Expenses', 'Category Wise', 'Shared Expense']
decision = ['Yes', 'No']
spend_categories = ['Food', 'Groceries', 'Utilities', 'Transport', 'Shopping', 'Miscellaneous']
dataAvailabilityMsg = {1: "No expense found for user", 2: "No shared expense found for user ",
                           5: "No expense data for selected dates",
                           6: "No expense data for selected dates and category"}

dateFormat = '%d-%b-%Y'
timeFormat = '%H:%M'
monthFormat = '%b-%Y'

config = configparser.ConfigParser()
configFileName = "config.ini"


def setConfig():
    config["files"] = {
        "UserExpenses": "user_expenses.json",
        "GroupExpenses": "group_expenses.json",
        "UserProfile": "user_emails.json"
    }
    config["settings"] = {
        "ApiToken": "",
        "ExpenseCategories": ['Food', 'Groceries', 'Utilities', 'Transport', 'Shopping', 'Miscellaneous'],
        "ExpenseChoices": ['Date', 'Category', 'Cost'],

    }


    with open(configFileName, 'w+') as configfile:
        config.write(configfile)


def loadConfig():
    config.read(configFileName)


def getUserExpensesFile():
    setConfig()
    filename = config['files']['UserExpenses']
    return os.path.join("data", filename)


def getGroupExpensesFile():
    filename = config['files']['GroupExpenses']
    return os.path.join("data", filename)


def getUserProfileFile():
    filename = config['files']['UserProfile']
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
    categories = config.get('settings', 'ExpenseCategories')
    categories = categories.split(",")
    return categories


def getSpendDisplayOptions():
    choices = config.get('settings', 'DisplayChoices')
    choices = choices.split(",")
    return choices


def getExpenseChoices():
    choices = config.get('settings', 'ExpenseChoices')
    choices = choices.split(",")
    return choices


def getCommands():
    return commands


def getDateFormat():
    return dateFormat


def getTimeFormat():
    return timeFormat


def getMonthFormat():
    return monthFormat


def getApiToken():
    return config['settings']['ApiToken']
