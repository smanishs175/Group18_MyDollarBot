from code import overallBudget_update
from mock import ANY
from mock.mock import patch
from telebot import types


@patch('telebot.telebot')
def test_update_overall_budget_already_available_case(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(overallBudget_update, 'helper')
    overallBudget_update.helper.isOverallBudgetAvailable.return_value = True
    overallBudget_update.helper.getOverallBudget.return_value = 100

    overallBudget_update.update_overall_budget(120, mc)
    mc.send_message.assert_called_with(120, ANY)


@patch('telebot.telebot')
def test_update_overall_budget_new_budget_case(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(overallBudget_update, 'helper')
    overallBudget_update.helper.isOverallBudgetAvailable.return_value = True

    overallBudget_update.update_overall_budget(120, mc)
    mc.send_message.assert_called_with(120, ANY)


@patch('telebot.telebot')
def test_post_overall_amount_input_working(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(overallBudget_update, 'helper')
    overallBudget_update.helper.isOverallBudgetAvailable.return_value = True
    overallBudget_update.helper.validate_entered_amount.return_value = 150

    message = create_message("hello from testing")
    overallBudget_update.post_overall_amount_input(message, mc)

    mc.send_message.assert_called_with(11, ANY)


@patch('telebot.telebot')
def test_post_overall_amount_input_nonworking(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(overallBudget_update, 'helper')
    overallBudget_update.helper.isOverallBudgetAvailable.return_value = True
    overallBudget_update.helper.validate_entered_amount.return_value = 0
    overallBudget_update.helper.throw_exception.return_value = True

    message = create_message("hello from testing")
    overallBudget_update.post_overall_amount_input(message, mc)

    assert(overallBudget_update.helper.throw_exception.called)


@patch('telebot.telebot')
def test_update_category_budget(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True

    mocker.patch.object(overallBudget_update, 'helper')
    overallBudget_update.helper.getSpendCategories.return_value = ['Food', 'Groceries', 'Utilities', 'Transport', 'Shopping', 'Miscellaneous']

    message = create_message("hello from testing")
    overallBudget_update.update_category_budget(message, mc)

    mc.reply_to.assert_called_with(message, 'Select Category', reply_markup=ANY)


@patch('telebot.telebot')
def test_post_category_selection_category_not_found(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(overallBudget_update, 'helper')
    overallBudget_update.helper.getSpendCategories.return_value = []
    overallBudget_update.helper.throw_exception.return_value = True

    message = create_message("hello from testing")
    overallBudget_update.post_category_selection(message, mc)

    mc.send_message.assert_called_with(11, 'Invalid', reply_markup=ANY)
    assert(overallBudget_update.helper.throw_exception.called)


@patch('telebot.telebot')
def test_post_category_selection_category_wise_case(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(overallBudget_update, 'helper')
    overallBudget_update.helper.getSpendCategories.return_value = ['Food', 'Groceries', 'Utilities', 'Transport', 'Shopping', 'Miscellaneous']
    overallBudget_update.helper.getCategoryBudgetByCategory.return_value = 10
    overallBudget_update.helper.isCategoryBudgetByCategoryAvailable.return_value = True

    message = create_message("Food")
    overallBudget_update.post_category_selection(message, mc)

    mc.send_message.assert_called_with(11, ANY)
    assert(overallBudget_update.helper.getCategoryBudgetByCategory.called)


@patch('telebot.telebot')
def test_post_category_selection_overall_case(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(overallBudget_update, 'helper')
    overallBudget_update.helper.getSpendCategories.return_value = ['Food', 'Groceries', 'Utilities', 'Transport', 'Shopping', 'Miscellaneous']
    overallBudget_update.helper.isCategoryBudgetByCategoryAvailable.return_value = False

    message = create_message("Food")
    overallBudget_update.post_category_selection(message, mc)

    mc.send_message.assert_called_with(11, 'Enter monthly budget for Food\n(Enter numeric values only)')


@patch('telebot.telebot')
def test_post_category_amount_input_working(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(overallBudget_update, 'helper')
    overallBudget_update.helper.validate_entered_amount.return_value = 100

    message = create_message("Hello from testing")
    overallBudget_update.post_category_amount_input(message, mc, "Food")

    mc.send_message.assert_called_with(11, 'Budget for Food Created!')


@patch('telebot.telebot')
def test_post_category_amount_input_nonworking_case(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.send_message.return_value = True

    mocker.patch.object(overallBudget_update, 'helper')
    overallBudget_update.helper.validate_entered_amount.return_value = 0
    overallBudget_update.helper.throw_exception.return_value = True

    message = create_message("Hello from testing")
    overallBudget_update.post_category_amount_input(message, mc, "Food")

    assert(overallBudget_update.helper.throw_exception.called)


@patch('telebot.telebot')
def test_post_category_add(mock_telebot, mocker):
    mc = mock_telebot.return_value
    mc.reply_to.return_value = True

    message = create_message("hello from testing!")
    overallBudget_update.post_category_add(message, mc)

    mc.reply_to.assert_called_with(message, 'Select Option', reply_markup=ANY)


def create_message(text):
    params = {'messagebody': text}
    chat = types.User(11, False, 'test')
    message = types.Message(1, None, None, chat, 'text', params, "")
    message.text = text
    return message