import re
import json
import os
from datetime import datetime
from telebot_calendar import Calendar, CallbackData, ENGLISH_LANGUAGE
from telebot.types import ReplyKeyboardRemove, CallbackQuery

#calender initialized
calendar = Calendar(language=ENGLISH_LANGUAGE)
calendar_1_callback = CallbackData("calendar_1", "action", "year", "month", "day")

#categories and options
date_range=[]
spend_display_option = ['All Expenses','Category Wise','Shared Expense']
decision=['Yes','No']
spend_categories = ['Food', 'Groceries', 'Utilities', 'Transport', 'Shopping', 'Miscellaneous']
option = {}

update_options = {
    'continue': 'Continue',
    'exit': 'Exit'
}


data_format = {
    'data': [],
    'budget': {
        'overall': None,
        'category': None
    }
}

# set of implemented commands and their description
# commands = {
#     'menu': 'Display this menu',
#     'add': 'Record/Add a new spending',
#     'display': 'Show sum of expenditure for the current day/month',
#     'estimate': 'Show an estimate of expenditure for the next day/month',
#     'history': 'Display spending history',
#     'delete': 'Clear/Erase all your records',
#     'edit': 'Edit/Change spending details',
#     'budget': 'Add/Update/View/Delete budget'
# }

commands = {
    'menu': 'Display this menu',
    'add': 'Record/Add a new spending',
    'addGroup': 'Add a group expense',
    'display': 'Show sum of expenditure for the current day/month',
    'history': 'Display spending history',
    'reset': 'Clear/Erase all your records',
    'edit': 'Edit/Change spending details'
}

dateFormat = '%d-%b-%Y'
timeFormat = '%H:%M'
monthFormat = '%b-%Y'
expenseFile = "expense_record.json"
groupExpenseFile = "group_expenses.json"


# function to load .json expense record data
def read_json(filename=expenseFile):
    try:
        if not os.path.exists(filename):
            with open(filename, 'w') as json_file:
                json_file.write('{}')
            return json.dumps('{}')
        elif os.stat(filename).st_size != 0:
            with open(filename) as expense_record:
                expense_record_data = json.load(expense_record)
            return expense_record_data

    except FileNotFoundError:
        print("---------NO RECORDS FOUND---------")


def write_json(user_list, filename=expenseFile):
    try:
        with open(filename, 'w') as json_file:
            json.dump(user_list, json_file, ensure_ascii=False, indent=4)
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
    data = getUserData(chat_id)
    if data is not None:
        return data['data']
    return None


def getUserData(chat_id):
    user_list = read_json()
    if user_list is None:
        return None
    if (str(chat_id) in user_list):
        return user_list[str(chat_id)]
    return None


def throw_exception(e, message, bot, logging):
    logging.exception(str(e))
    bot.reply_to(message, 'Oh no! ' + str(e))


def createNewUserRecord():
    return data_format


def getOverallBudget(chatId):
    data = getUserData(chatId)
    if data is None:
        return None
    return data['budget']['overall']


def getCategoryBudget(chatId):
    data = getUserData(chatId)
    if data is None:
        return None
    return data['budget']['category']


def getCategoryBudgetByCategory(chatId, cat):
    if not isCategoryBudgetByCategoryAvailable(chatId, cat):
        return None
    data = getCategoryBudget(chatId)
    return data[cat]


def canAddBudget(chatId):
    return (getOverallBudget(chatId) is None) and (getCategoryBudget(chatId) is None)


def isOverallBudgetAvailable(chatId):
    return getOverallBudget(chatId) is not None


def isCategoryBudgetAvailable(chatId):
    return getCategoryBudget(chatId) is not None


def isCategoryBudgetByCategoryAvailable(chatId, cat):
    data = getCategoryBudget(chatId)
    if data is None:
        return False
    return cat in data.keys()


def display_remaining_budget(message, bot, cat):
    chat_id = message.chat.id
    if isOverallBudgetAvailable(chat_id):
        display_remaining_overall_budget(message, bot)
    elif isCategoryBudgetByCategoryAvailable(chat_id, cat):
        display_remaining_category_budget(message, bot, cat)


def display_remaining_overall_budget(message, bot):
    print('here')
    chat_id = message.chat.id
    remaining_budget = calculateRemainingOverallBudget(chat_id)
    print("here", remaining_budget)
    if remaining_budget >= 0:
        msg = '\nRemaining Overall Budget is $' + str(remaining_budget)
    else:
        msg = '\nBudget Exceded!\nExpenditure exceeds the budget by $' + str(remaining_budget)[1:]
    bot.send_message(chat_id, msg)


def calculateRemainingOverallBudget(chat_id):
    budget = getOverallBudget(chat_id)
    history = getUserHistory(chat_id)
    query = datetime.now().today().strftime(getMonthFormat())
    queryResult = [value for index, value in enumerate(history) if str(query) in value]

    return float(budget) - calculate_total_spendings(queryResult)


def calculate_total_spendings(queryResult):
    total = 0

    for row in queryResult:
        s = row.split(',')
        total = total + float(s[2])
    return total


def display_remaining_category_budget(message, bot, cat):
    chat_id = message.chat.id
    remaining_budget = calculateRemainingCategoryBudget(chat_id, cat)
    if remaining_budget >= 0:
        msg = '\nRemaining Budget for ' + cat + ' is $' + str(remaining_budget)
    else:
        msg = '\nBudget for ' + cat + ' Exceded!\nExpenditure exceeds the budget by $' + str(abs(remaining_budget))
    bot.send_message(chat_id, msg)


def calculateRemainingCategoryBudget(chat_id, cat):
    budget = getCategoryBudgetByCategory(chat_id, cat)
    history = getUserHistory(chat_id)
    query = datetime.now().today().strftime(getMonthFormat())
    queryResult = [value for index, value in enumerate(history) if str(query) in value]

    return float(budget) - calculate_total_spendings_for_category(queryResult, cat)


def calculate_total_spendings_for_category(queryResult, cat):
    total = 0

    for row in queryResult:
        s = row.split(',')
        if cat == s[1]:
            total = total + float(s[2])
    return total


def getSpendCategories():
    return spend_categories


def getSpendDisplayOptions():
    return spend_display_option


def getSpendEstimateOptions():
    return spend_estimate_option


def getCommands():
    return commands


def getDateFormat():
    return dateFormat


def getTimeFormat():
    return timeFormat


def getMonthFormat():
    return monthFormat


def getChoices():
    return choices


def getBudgetOptions():
    return budget_options


def getBudgetTypes():
    return budget_types


def getUpdateOptions():
    return update_options
