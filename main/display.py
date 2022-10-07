"""

@author: Shruti
"""
import plots
import time
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from datetime import datetime
from telebot import types
from main import helper
import os

def run(message,bot):
    helper.date_range=[]
    date_selections(message,bot)
    markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
    markup.row_width = 2
    for opt in helper.decision:
        markup.add(opt)
    msg = bot.reply_to(message, 'Do you want to see the expense charts?', reply_markup=markup)
    bot.register_next_step_handler(msg, show_categories,bot)

def date_selections(message,bot):
    print("date_selections")
    now = datetime.now()
    bot.send_message(
        message.chat.id,
        "Select start date",
        reply_markup=helper.calendar.create_calendar(
            name=helper.calendar_1_callback.prefix,
            year=now.year,
            month=now.month,  # Specify the NAME of your calendar
        ),
    )
    bot.send_message(
        message.chat.id,
        "Select end date",
        reply_markup=helper.calendar.create_calendar(
            name=helper.calendar_1_callback.prefix,
            year=now.year,
            month=now.month,  # Specify the NAME of your calendar
        ),
    )

def show_categories(message,bot):
    try:
        chat_id = message.chat.id
        opt = message.text
        if not opt in helper.decision:
            raise Exception("Sorry wrong option\"{}\"!".format(choice))

        if opt == 'Yes':
            helper.read_json(helper.getUserExpensesFile())
            chat_id = message.chat.id
            history = helper.getUserHistory
            if history == None:
                bot.send_message(chat_id, "Oops! Looks like you do not have any spending records!")
            else:
                markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
                markup.row_width = 2
                for mode in helper.spend_display_option:
                    markup.add(mode)
                msg = bot.reply_to(message, 'Please select a category to see the total expense', reply_markup=markup)
                bot.register_next_step_handler(msg, display_total,bot)
        else:
            bot.reply_to(message, "Okay, you selected No hence there is no chart displayed")


    except Exception as e:
        bot.reply_to(message, str(e))


def expense_category(message,bot):
    try:
        start_date=helper.date_range[0]
        end_date=helper.date_range[1]
        print(start_date)
        print(end_date)
        chat_id = message.chat.id
        choice_category = message.text
        if not choice_category in helper.spend_categories:
            raise Exception("Sorry I can't show spendings for \"{}\"!".format(choice_category))

        check=plots.categorical_plot(str(chat_id), start_date, end_date, choice_category)
        #print(check)
        if check!=7:
            plotmsg = helper.dataAvailabilityMsg[check]
            bot.reply_to(message, plotmsg)
        else:
            print("executed")
            bot.send_photo(chat_id, photo=open('categorical_expenses.png', 'rb'))
            os.remove('categorical_expenses.png')

    except Exception as e:
        bot.reply_to(message, str(e))

def display_total(message,bot):
    try:

        chat_id = message.chat.id
        choice = message.text
        start_date = helper.date_range[0]
        end_date = helper.date_range[1]

        if not choice in helper.spend_display_option:
            raise Exception("Sorry I can't show spendings for \"{}\"!".format(choice))

        history = helper.getUserHistory(chat_id)
        if history is None:
            raise Exception("Oops! Looks like you do not have any spending records!")


        bot.send_chat_action(chat_id, 'typing')  # show the bot "typing" (max. 5 secs)
        time.sleep(0.5)

        total_text = ""

        if choice == 'All Expenses':
            check=plots.overall_plot(str(chat_id), start_date, end_date)
            if check != 7:
                plotmsg = helper.dataAvailabilityMsg[check]
                bot.reply_to(message, plotmsg)
            else:
                bot.send_photo(chat_id, photo=open('overall_expenses.png', 'rb'))
                os.remove('overall_expenses.png')

        elif choice == 'Category Wise':
            # helper.read_json()
            chat_id = message.chat.id
            # helper.option.pop(chat_id, None)  # remove temp choice
            markup = types.ReplyKeyboardMarkup(one_time_keyboard=True)
            markup.row_width = 2
            for c in helper.spend_categories:
                markup.add(c)
            msg = bot.reply_to(message, 'Select Category', reply_markup=markup)
            bot.register_next_step_handler(msg, expense_category,bot)


        elif choice=='Shared Expense':
            check=plots.owe(str(chat_id))
            if check != 7:
                plotmsg = helper.dataAvailabilityMsg[check]
                bot.reply_to(message, plotmsg)
            else:
                bot.send_photo(chat_id, photo=open('owe.png', 'rb'))
                os.remove('owe.png')

    except Exception as e:
         bot.reply_to(message, str(e))


