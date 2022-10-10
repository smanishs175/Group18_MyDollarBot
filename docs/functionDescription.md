start_and_menu_command(m)
- Function that defines how the /start and /help commands have to be handled/processed

command_add(message)
- Function that defines how the /add command has to be handled/processed

command_addgroup(message)
- Function that defines how the /addGroup command has to be handled/processed

command_history(message)
- Function that defines how the /history command has to be handled/processed

command_profile(message)
- Function that defines how the /profile command has to be handled/processed 

command_display(message)
- Function that defines how the /display command has to be handled/processed

command_erase(message)
- Function that defines how the /erase command has to be handled/processed
 
post_category_selection(message)
- Function that processes the entered category, and accepts amount as input accordingly

post_amount_input(message)
- Function that writes the entered amount into the user's json file once the amount is validated 

expense_category_input(message) 
- Function that processes the entered category, and requests the participant emails

take_all_users_input(message, category)
- Function that accepts the emails and validates them

add_transactions_to_user(transaction_id, chat_ids)
- Function that adds the created transaction to each participating user

deleteHistory(chat_id)
- Function to delete previous expenditure history of the user

getUserHistory(chat_id):
- Function to fetch user history and display it in the bot window

display_total(message)
- Function to retrieve spending data per category from user history and return total expense

post_email_input(message)
- Function to allow the user to update his/her email ID for profile

date_selections(message)
- Function to allow the user to select the start and end date for the display feature

show_categories(message)
- Function to allow the user to choose a decision on viewing charts

display_total(message, individual expenses, group expenses)
- Function to display the expense charts based on user's selection of filtering expenses

expense_category(message, individual expenses, group expenses)
- Function to allow the user to view expenses for a specific category

loadConfig()
- Function to load the config file

