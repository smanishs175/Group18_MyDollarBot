import os
import json
from mock import patch
from telebot import types
from main import profile

dateFormat = '%d-%b-%Y'
timeFormat = '%H:%M'
monthFormat = '%b-%Y'

def create_message(text):
    params = {'messagebody': text}
    chat = types.User(11, False, 'test')
    return types.Message(1, None, None, chat, 'text', params, "")

@patch('telebot.telebot')
def test_run(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("hello from test run!")
    profile.run(message, mc)


@patch('telebot.telebot')
def test_post_email_input(mock_telebot, mocker):

    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    profile.add_group.validate_email_input.return_value = True
    profile.helper.read_json.return_value = {}
    message = create_message("pbrr@gmail.com")
    message.text = "pbrr@gmail.com"
    profile.helper.write_json.return_value = True
    profile.post_email_input(message, mc)

    # call exceptions
    message.text = None
    profile.post_email_input(message, mc)



