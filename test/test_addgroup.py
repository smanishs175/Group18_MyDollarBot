import os
import json
from mock import patch
from telebot import types
from main import add_group
from main import helper

dateFormat = '%d-%b-%Y'
timeFormat = '%H:%M'
monthFormat = '%b-%Y'
spendCategories = ['Food', 'Groceries', 'Utilities', 'Transport', 'Shopping', 'Miscellaneous']

helper.loadConfig()


def create_message(text):
    params = {'text': text}
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
def test_expense_category_input(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mc.reply_to.return_value = True
    mocker.patch.object(add_group, 'helper')
    add_group.helper.getSpendCategories.return_value = spendCategories

    message = create_message("Groceries")
    add_group.expense_category_input(message, mc)
    assert mc.send_message.called
    assert mc.send_message.called_with(11)


@patch('telebot.telebot')
def test_expense_category_input_invalid_category(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mc.reply_to.return_value = True
    mocker.patch.object(add_group, 'helper')
    add_group.helper.getSpendCategories.return_value = spendCategories

    message = create_message("blah")
    add_group.expense_category_input(message, mc)
    assert mc.send_message.called
    assert mc.send_message.called_with(11, 'Invalid')


@patch('telebot.telebot')
def test_take_all_users_input(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mc.reply_to.return_value = True
    mocker.patch.object(add_group, 'helper')
    add_group.helper.read_json.return_value = {"11": "hello@gmail.com", "20": "abcd@gmail.com", "21": "xyz@gmail.com"}

    message = create_message("abcd@gmail.com, xyz@gmail.com")
    add_group.take_all_users_input(message, mc, "Groceries")
    assert mc.send_message.called
    assert not mc.reply_to.called
    assert mc.send_message.called_with(11, 'How much did you spend on Groceries? \n(Enter numeric values only)')


@patch('telebot.telebot')
def test_take_all_users_input_invalid_email(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mc.reply_to.return_value = True
    mocker.patch.object(add_group, 'helper')
    # add_group.helper.read_json.return_value = {"11": "hello@gmail.com", "20": "abcd@gmail.com", "21": "xyz@gmail.com"}

    message = create_message("abcd-gmail.com")
    add_group.take_all_users_input(message, mc, "Groceries")
    assert mc.reply_to.called


@patch('telebot.telebot')
def test_take_all_users_input_creator_not_registered(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mc.reply_to.return_value = True
    mocker.patch.object(add_group, 'helper')
    add_group.helper.read_json.return_value = {"11": "hello@gmail.com", "20": "abcd@gmail.com", "21": "xyz@gmail.com"}

    message = create_message("world@gmail.com")
    add_group.take_all_users_input(message, mc, "Groceries")
    assert mc.reply_to.called


@patch('telebot.telebot')
def test_take_all_users_input_creator_unknown_user(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mc.reply_to.return_value = True
    mocker.patch.object(add_group, 'helper')
    add_group.helper.read_json.return_value = {"11": "hello@gmail.com", "20": "abcd@gmail.com", "21": "xyz@gmail.com"}

    message = create_message("efgh@gmail.com")
    add_group.take_all_users_input(message, mc, "Groceries")
    assert mc.reply_to.called


@patch('telebot.telebot')
def test_post_amount_input_nonworking(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mc.reply_to.return_value = True
    mocker.patch.object(add_group, 'helper')
    add_group.helper.validate_entered_amount.return_value = 0
    message = create_message("hello from testing!")
    add_group.post_amount_input(message, mc, 'Food', {})
    assert mc.reply_to.called


@patch('telebot.telebot')
def test_post_amount_input_working_withdata_chatid(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mocker.patch.object(add_group, 'helper')
    add_group.helper.validate_entered_amount.return_value = 10
    add_group.helper.write_json.return_value = True
    add_group.helper.getDateFormat.return_value = dateFormat
    add_group.helper.getTimeFormat.return_value = timeFormat
    mocker.patch.object(add_group, 'add_transaction_record')
    mocker.patch.object(add_group, 'add_transactions_to_user')
    add_group.add_transaction_record.return_value = 1001, ["sample transaction list"]
    add_group.add_transactions_to_user.return_value = ["sample updated user list"]

    add_group.transaction_record = {}
    message = create_message("10")
    add_group.post_amount_input(message, mc, 'Groceries', [11,20,21])
    assert not mc.reply_to.called
    assert mc.send_message.called


def test_validate_email_input():
    assert add_group.validate_email_input(["niharsrao@gmail.com"])


def test_validate_email_input_failure():
    try:
        add_group.validate_email_input(["niharsrao-gmail.com"])
    except Exception as e:
        assert True


def test_generate_transaction_id():
    assert add_group.generate_transaction_id()


def test_add_transaction_record(mocker):
    mocker.patch.object(add_group, 'helper')
    add_group.helper.read_json.return_value = {}
    assert add_group.add_transaction_record({})


def test_add_transactions_to_user(mocker):
    mocker.patch.object(add_group, 'helper')

    transaction_list = ["1001", "1002", "1003"]
    user_list = {"11": {}, "20": {}, "21": {}}

    add_group.helper.read_json.side_effect = [transaction_list, user_list]
    assert add_group.add_transactions_to_user("1002", ["20", "21"]) == \
           {"11": {}, "20": {'group_expenses': ["1002"]}, "21": {'group_expenses': ["1002"]}}


def test_add_transactions_to_user_invalid_transaction(mocker):
    mocker.patch.object(add_group, 'helper')

    transaction_list = ["1001", "1002", "1003"]
    user_list = {"11": {}, "20": {}, "21": {}}

    add_group.helper.read_json.side_effect = [transaction_list, user_list]
    try:
        _ = add_group.add_transactions_to_user("2002", ["20", "21"])
    except Exception as e:
        assert True



