import utils


def run(message, bot):
    global user_list
    chat_id = message.chat.id
    delete_history_text = ""
    user_list = utils.read_json()
    if (str(chat_id) in user_list):
        utils.write_json(deleteHistory(chat_id))
        delete_history_text = "History has been deleted!"
    else:
        delete_history_text = "No records there to be deleted. Start adding your expenses to keep track of your spendings!"
    bot.send_message(chat_id, delete_history_text)


# function to delete a record
def deleteHistory(chat_id):
    global user_list
    if (str(chat_id) in user_list):
        del user_list[str(chat_id)]
    return user_list