import os
import json
from mock import patch
from telebot import types
from main import display
from main import helper
from main import plots

decision=['Yes', 'No']

def create_message(text):
    params = {'text': text}
    chat = types.User(11, False, 'test')
    return types.Message(1, None, None, chat, 'text', params, "")

@patch('telebot.telebot')
def test_run(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    message = create_message("hello from test run!")
    display.run(message, mc)
    assert mc.send_message.called


@patch('telebot.telebot')
def test_show_categories(mock_telebot,mocker):
    message = create_message("Yes")
    opt=message.text

    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mc.reply_to.return_value = True
    display.helper.getSpendCategories.return_value = decision
    history=True

    display.show_categories(message,mc)
    assert mc.send_message.called

@patch('telebot.telebot')
def test_date_selections(mock_telebot,mocker):
    message = create_message("hello from test run!")
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True
    mc = mock_telebot.return_value
    mc.send_message.return_value = True
    mc.reply_to.return_value = True

    display.date_selections(message, mc)
    assert mc.send_message.called

























#
# @patch('telebot.telebot')
# def test_run(mock_telebot, mocker):
#     mc = mock_telebot.return_value
#     mc.reply_to.return_value = True
#     message = create_message("hello from test run!")
#     display.run(message, mc)
#     assert mc.send_message.called


# @patch('telebot.telebot')
# def test_no_data_available(mock_telebot, mocker):
#     mc = mock_telebot.return_value
#     mc.reply_to.return_value = True
#     message = create_message("/spendings")
#     display.run(message, mc)
#     assert mc.send_message.called
#
#
# @patch('telebot.telebot')
# def test_invalid_format(mock_telebot, mocker):
#     mc = mock_telebot.return_value
#     mc.reply_to.return_value = True
#     message = create_message("luster")
#     try:
#         display.display_total(message, mc)
#         assert False
#     except Exception:
#         assert True
#
#
# @patch('telebot.telebot')
# def test_valid_format(mock_telebot, mocker):
#     mc = mock_telebot.return_value
#     mc.reply_to.return_value = True
#     message = create_message("Month")
#     try:
#         display.display_total(message, mc)
#         assert True
#     except Exception:
#         assert False
#
#
# @patch('telebot.telebot')
# def test_valid_format_day(mock_telebot, mocker):
#     mc = mock_telebot.return_value
#     mc.reply_to.return_value = True
#     message = create_message("Day")
#     try:
#         display.display_total(message, mc)
#         assert True
#     except Exception:
#         assert False
#
#
# @patch('telebot.telebot')
# def test_spending_run_working(mock_telebot, mocker):
#
#     MOCK_USER_DATA = test_read_json()
#     mocker.patch.object(display, 'helper')
#     display.helper.getUserHistory.return_value = MOCK_USER_DATA["894127939"]
#     display.helper.getSpendDisplayOptions.return_value = [
#         "Day", "Month"]
#     display.helper.getDateFormat.return_value = '%d-%b-%Y'
#     display.helper.getMonthFormat.return_value = '%b-%Y'
#     mc = mock_telebot.return_value
#     mc.reply_to.return_value = True
#     message = create_message("Day")
#     message.text = "Day"
#     display.run(message, mc)
#     # assert not mc.send_message.called
#
#
# @patch('telebot.telebot')
# def test_spending_display_working(mock_telebot, mocker):
#
#     MOCK_USER_DATA = test_read_json()
#     mocker.patch.object(display, 'helper')
#     display.helper.getUserHistory.return_value = MOCK_USER_DATA["894127939"]
#     display.helper.getSpendDisplayOptions.return_value = [
#         "Day", "Month"]
#     display.helper.getDateFormat.return_value = '%d-%b-%Y'
#     display.helper.getMonthFormat.return_value = '%b-%Y'
#     mc = mock_telebot.return_value
#     mc.reply_to.return_value = True
#     message = create_message("Day")
#     message.text = "Day"
#     display.display_total(message, mc)
#     # assert mc.send_message.called
#
#
# @patch('telebot.telebot')
# def test_spending_display_month(mock_telebot, mocker):
#
#     MOCK_USER_DATA = test_read_json()
#     mocker.patch.object(display, 'helper')
#     display.helper.getUserHistory.return_value = MOCK_USER_DATA["894127939"]
#     display.helper.getSpendDisplayOptions.return_value = [
#         "Day", "Month"]
#     display.helper.getDateFormat.return_value = '%d-%b-%Y'
#     display.helper.getMonthFormat.return_value = '%b-%Y'
#     mc = mock_telebot.return_value
#     mc.reply_to.return_value = True
#     message = create_message("Month")
#     message.text = "Month"
#     display.display_total(message, mc)
#     # assert mc.send_message.called
#
#
# def create_message(text):
#     params = {'messagebody': text}
#     chat = types.User(11, False, 'test')
#     return types.Message(894127939, None, None, chat, 'text', params, "")
#
#
# def test_read_json():
#     try:
#         if not os.path.exists('./test/dummy_expense_record.json'):
#             with open('./test/dummy_expense_record.json', 'w') as json_file:
#                 json_file.write('{}')
#             return json.dumps('{}')
#         elif os.stat('./test/dummy_expense_record.json').st_size != 0:
#             with open('./test/dummy_expense_record.json') as expense_record:
#                 expense_record_data = json.load(expense_record)
#             return expense_record_data
#
#     except FileNotFoundError:
#         print("---------NO RECORDS FOUND---------")