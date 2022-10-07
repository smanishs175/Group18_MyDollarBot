from main import helper


def run(message, bot):
    user_list = helper.read_json(helper.getUserExpensesFile())
    if str(chat_id) in user_list:
        helper.write_json(deleteHistory(chat_id), helper.getUserExpensesFile())
        delete_history_text = "History has been deleted!"
    else:
        delete_history_text = "No records there to be deleted. Start adding your expenses to keep track of your " \
                              "spendings! "
    bot.send_message(chat_id, delete_history_text)


# function to delete a record
def deleteHistory(chat_id):
    if str(chat_id) in user_list:
        del user_list[str(chat_id)]
    return user_list
