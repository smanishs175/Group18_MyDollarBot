#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import logging
import telebot
import time
import helper
import update
import pastrecord
import show
import calculate
import remove
import addup
import add_group
import overallBudget
from datetime import datetime
from jproperties import Properties

configs = Properties()

with open('user.properties', 'rb') as read_prop:
    configs.load(read_prop)

api_token = str(configs.get('api_token').data)

bot = telebot.TeleBot(api_token)

telebot.logger.setLevel(logging.INFO)

option = {}


# Define listener for requests by user
def listener(user_requests):
    for req in user_requests:
        if(req.content_type == 'text'):
            # print(req)
            print("{} name:{} chat_id:{} \nmessage: {}\n".format(str(datetime.now()), str(req.chat.first_name), str(req.chat.id), str(req.text)))


bot.set_update_listener(listener)


# defines how the /start and /help commands have to be handled/processed
@bot.message_handler(commands=['start', 'menu'])
def start_and_menu_command(m):
    helper.read_json()
    global user_list
    chat_id = m.chat.id

    text_intro = "Welcome to TrackMyDollar - a simple solution to track your expenses! \nHere is a list of available commands, please enter a command of your choice so that I can assist you further: \n\n"
    commands = helper.getCommands()
    for c in commands:  # generate help text out of the commands dictionary defined at the top
        text_intro += "/" + c + ": "
        text_intro += commands[c] + "\n\n"
    bot.send_message(chat_id, text_intro)
    return True


# defines how the /new command has to be handled/processed
@bot.message_handler(commands=['add'])
def command_addup(message):
    addup.run(message, bot)


# defines how the /new command has to be handled/processed
@bot.message_handler(commands=['addGroup'])
def command_addup(message):
    add_group.run(message, bot)

# function to fetch expenditure pastrecord of the user
@bot.message_handler(commands=['pastrecord'])
def command_pastrecord(message):
    pastrecord.run(message, bot)

# function to fetch expenditure history of the user
@bot.message_handler(commands=['history'])
def command_history(message):
    pastrecord.run(message, bot)


# function to edit date, category or cost of a transaction
@bot.message_handler(commands=['edit'])
def command_edit(message):
    update.run(message, bot)


# function to display total expenditure
@bot.message_handler(commands=['display'])
def command_display(message):
    show.run(message, bot)


# function to estimate future expenditure
@bot.message_handler(commands=['estimate'])
def command_estimate(message):
    calculate.run(message, bot)

# handles "/delete" command
@bot.message_handler(commands=['delete'])
def command_delete(message):
    remove.run(message, bot)


@bot.message_handler(commands=['budget'])
def command_budget(message):
   overallBudget.run(message, bot)

@bot.message_handler(commands=['category'])
def command_category(message):
    overallBudget.run(message, bot)


# function to update date, category or cost of a transaction
@bot.message_handler(commands=['update'])
def command_update(message):
    update.run(message, bot)


# function to show total expenditure
@bot.message_handler(commands=['show'])
def command_show(message):
    show.run(message, bot)


# function to calculate future expenditure
@bot.message_handler(commands=['calculate'])
def command_calculate(message):
    calculate.run(message, bot)


# handles "/remove" command
@bot.message_handler(commands=['remove'])
def command_remove(message):
    remove.run(message, bot)


@bot.message_handler(commands=['overallBudget'])
def command_overallBudget(message):
    overallBudget.run(message, bot)


# not used
def addUserHistory(chat_id, user_record):
    global user_list
    if(not(str(chat_id) in user_list)):
        user_list[str(chat_id)] = []
    user_list[str(chat_id)].append(user_record)
    return user_list


def main():
    try:
        bot.polling(none_stop=True)
    except Exception as e:
        logging.exception(str(e))
        time.sleep(3)
        print("Connection Timeout")


if __name__ == '__main__':
    main()
