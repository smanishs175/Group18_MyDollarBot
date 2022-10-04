# import helper
from main import helper
import logging
from telebot import types
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
import random

option = {}
group_expense_file = "group_expenses.json"
random.seed(2022)


def run(message, bot):
    helper.read_json(filename=group_expense_file)
    chat_id = message.chat.id
    option.pop(chat_id, None)  # remove temp choicex
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    for c in helper.getSpendCategories():
        markup.add(c)
    msg = bot.reply_to(message, 'Select Category', reply_markup=markup)
    bot.register_next_step_handler(msg, expense_category_input, bot)


def expense_category_input(message, bot):
    chat_id = message.chat.id
    try:
        selected_category = message.text
        if selected_category not in helper.getSpendCategories():
            bot.send_message(chat_id, 'Invalid', reply_markup=types.ReplyKeyboardRemove())
            raise Exception("Sorry I don't recognise this category \"{}\"!".format(selected_category))

        option[chat_id] = selected_category
        message = bot.send_message(chat_id,
                                   'Please enter comma separated email ids of all the users you want to add in the expense. \n')
        bot.register_next_step_handler(message, take_all_users_input, bot, selected_category)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, 'Oh no! ' + str(e))
        display_text = ""
        commands = helper.getCommands()
        for c in commands:  # generate help text out of the commands dictionary defined at the top
            display_text += "/" + c + ": "
            display_text += commands[c] + "\n"
        bot.send_message(chat_id, 'Please select a menu option from below:')
        bot.send_message(chat_id, display_text)


def take_all_users_input(message, bot, selected_category):
    chat_id = message.chat.id
    try:
        emails = message.text
        email_ids = set(emails.split(","))

        if not validate_email_input(email_ids):
            raise Exception(f"Sorry the email format is not correct: {emails}")

        emails_user_map = {}
        user_list = helper.read_json()

        for user in user_list:
            if 'email' in user_list[user]:
                emails_user_map[user_list[user]['email']] = user

        creator = user_list[str(chat_id)]['email']
        email_ids_present_in_expense = email_ids.intersection(set(emails_user_map.keys()))
        if len(email_ids_present_in_expense) != len(email_ids):
            invalid_emails = list(email_ids.difference(email_ids_present_in_expense))
            raise Exception(f"Sorry one or more of the email(s) are not registered with us: {invalid_emails}")

        email_ids_present_in_expense = list(email_ids_present_in_expense)
        email_ids_present_in_expense.insert(creator, 0)

        option[chat_id] = selected_category
        message = bot.send_message(chat_id, 'How much did you spend on {}? \n(Enter numeric values only)'.format(
            str(option[chat_id])))
        bot.register_next_step_handler(message, post_amount_input, bot, selected_category, email_ids_present_in_expense)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, 'Oh no! ' + str(e))
        display_text = ""
        commands = helper.getCommands()
        for c in commands:  # generate help text out of the commands dictionary defined at the top
            display_text += "/" + c + ": "
            display_text += commands[c] + "\n"
        bot.send_message(chat_id, 'Please select a menu option from below:')
        bot.send_message(chat_id, display_text)


def post_amount_input(message, bot, selected_category, email_ids_present_in_expense):
    chat_id = message.chat.id
    try:
        transaction_record = {}
        amount_entered = message.text
        amount_value = helper.validate_entered_amount(amount_entered)  # validate
        if amount_value == 0:  # cannot be $0 spending
            raise Exception("Spent amount has to be a non-zero number.")
        amount_value = float(amount_value)

        # TODO add group expenses handling
        num_members = len(email_ids_present_in_expense)
        member_share = amount_value / num_members
        transaction_record["total"] = amount_value
        transaction_record["category"] = str(selected_category)
        transaction_record["created_by"] = email_ids_present_in_expense[0]
        transaction_record["members"] = {}

        for email in email_ids_present_in_expense:
            transaction_record["members"].update({email: member_share})

        # add user_ids input
        date_of_entry = str(datetime.today().strftime(helper.getDateFormat() + ' ' + helper.getTimeFormat()))
        transaction_record["created_at"] = date_of_entry
        transaction_record["updated_at"] = None
        helper.write_json(add_transaction_record(transaction_record), filename=group_expense_file)

        bot.send_message(chat_id, 'The following expenditure has been recorded: You, and {} other members, '
                                  'have spent ${} for {} on {}'.format(str(num_members - 1), str(member_share),
                                                                       str(selected_category), date_of_entry))
        helper.display_remaining_budget(message, bot, selected_category)
    except Exception as e:
        logging.exception(str(e))
        bot.reply_to(message, 'Oh no. ' + str(e))
        display_text = ""
        commands = helper.getCommands()
        for c in commands:  # generate help text out of the commands dictionary defined at the top
            display_text += "/" + c + ": "
            display_text += commands[c] + "\n"
        bot.send_message(chat_id, 'Please select a menu option from below:')
        bot.send_message(chat_id, display_text)


def add_transaction_record(transaction_record):
    transaction_list = helper.read_json(filename=group_expense_file)
    transaction_id = str(generate_transaction_id())
    transaction_list[transaction_id] = transaction_record
    return transaction_list


def validate_email_input(email_ids):
    for email in email_ids:
        if not validate_email(email, check_deliverability=True):
            return False

    return True


def generate_transaction_id():
    return random.randint(4000000000, 9999999999)
