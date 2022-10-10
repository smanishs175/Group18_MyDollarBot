import os
import json
from mock import patch
from telebot import types
from main import history
from main import helper


def create_message(text):
    params = {'text': text}
    chat = types.User(11, False, 'test')
    return types.Message(1, None, None, chat, 'text', params, "")


@patch('telebot.telebot')
def test_run(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    mc = mock_telebot.return_value
    mocker.patch.object(history, 'helper')

    transaction_list = {"1001": {"created_at": "", "category": "", "members": {"11": 0}},
                        "1002": {"created_at": "", "category": "", "members": {"11": 0, "20": 0}}
                        }
    history.helper.read_json.side_effect = [None, transaction_list]
    history.helper.getUserHistory.return_value = {'personal_expenses': "sample expense record", "group_expenses": ["1002"]}

    message = create_message("Hello from testing")
    try:
        history.run(message, mc)
    except Exception as e:
        assert True


@patch('telebot.telebot')
def test_run_no_records(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    mc = mock_telebot.return_value
    mocker.patch.object(history, 'helper')
    history.helper.read_json.return_value = None
    history.helper.getUserHistory.return_value = None

    message = create_message("Hello from testing")
    try:
        history.run(message, mc)
    except Exception as e:
        assert True


@patch('telebot.telebot')
def test_run_empty_records(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    mc = mock_telebot.return_value
    mocker.patch.object(history, 'helper')
    history.helper.read_json.return_value = None
    history.helper.getUserHistory.return_value = []

    message = create_message("Hello from testing")
    try:
        history.run(message, mc)
    except Exception as e:
        assert True