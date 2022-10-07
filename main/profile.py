from main import helper
import logging
from telebot import types
from datetime import datetime
from email_validator import validate_email, EmailNotValidError
import random
from main import add_group


def run(message, bot):
    msg = bot.reply_to(message, 'Please enter your email')
    bot.register_next_step_handler(msg, post_email_input, bot)


def post_email_input(message, bot):
    chat_id = str(message.chat.id)
    try:
        email = message.text
        if not add_group.validate_email_input([email]):
            raise Exception(f"Sorry the email format is not correct: {email}")

        user_email_file = helper.getUserProfileFile()
        data = helper.read_json(user_email_file)
        data[chat_id] = email
        helper.write_json(data, user_email_file)

        message = bot.send_message(chat_id,
                                   'Successfully added your email! \n')
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
