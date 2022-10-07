import os
import json
from mock import patch
from telebot import types
from main import add_group
from main import helper

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
    add_group.run(message, mc)
    assert mc.send_message


@patch('telebot.telebot')
def test_post_amount_input_nonworking(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mc.reply_to.return_value = True
    mocker.patch.object(add_group, 'helper')
    add_group.helper.validate_entered_amount.return_value = 0
    message = create_message("hello from testing!")
    add_group.post_amount_input(message, mc, 'Food', {})
    assert (mc.reply_to.called)


@patch('telebot.telebot')
def test_post_amount_input_working_withdata_chatid(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(add_group, 'helper')
    add_group.helper.validate_entered_amount.return_value = 10
    add_group.helper.write_json.return_value = True
    add_group.helper.getDateFormat.return_value = dateFormat
    add_group.helper.getTimeFormat.return_value = timeFormat

    mocker.patch.object(add_group, 'option')
    add_group.option = {11, "here"}
    test_option = {}
    test_option[11] = "here"
    add_group.option = test_option

    message = create_message("hello from testing!")
    add_group.post_amount_input(message, mc, 'Food', {})
    assert (mc.send_message.called)
    assert (mc.send_message.called_with(11, "ANY"))


def test_validate_email_input():
    assert add_group.validate_email_input(["niharsrao@gmail.com"])

    # failure
    try:
        add_group.validate_email_input(["niharsraogmail.com"])
    except Exception as e:
        print(e)


def test_generate_transaction_id():
    assert add_group.generate_transaction_id()


def test_get_emails_ids_mapping():
    assert add_group.get_emails_ids_mapping([]) == {}


def test_add_transaction_record(mocker):
    mocker.patch.object(add_group, 'helper')
    add_group.helper.read_json.return_value = {}
    assert add_group.add_transaction_record({})


def test_add_transactions_to_user(mocker):
    mocker.patch.object(add_group, 'helper')
    add_group.helper.read_json.return_value = {"122": {"email": "pbrr", "transactions": []}}
    add_group.get_emails_ids_mapping.return_value = {"pbrr": 122}

    assert add_group.add_transactions_to_user(122, ["pbrr"])


@patch('telebot.telebot')
def test_take_all_users_input(mock_telebot, mocker):
    mocker.patch.object(add_group, 'helper')
    add_group.helper.read_json.return_value = {"11": {"email": "pbrr@gmail.com", "transactions": []}}
    add_group.get_emails_ids_mapping.return_value = {"pbrr@gmail.com": 122}
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("hello from test run!")
    message.text = "pbrr@gmail.com"
    add_group.take_all_users_input(message, mc, "Groceries")
    add_group.helper.read_json.return_value = {"11": {"email": "pbrr", "transactions": []}}
    add_group.take_all_users_input(message, mc, "Groceries")
