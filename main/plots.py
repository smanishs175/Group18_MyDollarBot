import matplotlib.pyplot as plt
import pandas as pd
import helper
import numpy as np

month_dict = {1 : 'Jan', 2 : 'Feb', 3 : 'Mar',
              4 : 'Mar', 5 : 'Apr', 6 : 'Jun',
              7 : 'Jul', 8 : 'Aug', 9 : 'Sep',
              10: 'Oct', 11: 'Nov', 12: 'Dec'}


dateFormat = '%d-%b-%Y'
timeFormat = '%H:%M'
monthFormat = '%b-%Y'

## getting json files
user_key_filename = helper.getUserProfileFile()
user_key = helper.read_json(user_key_filename)

expenseFile = helper.getUserExpensesFile()
expense_dict = helper.read_json(expenseFile)

transactionFile = helper.getGroupExpensesFile()
transaction_dict = helper.read_json(transactionFile)

def label_amount(y):
    for ind,val in enumerate(y):
        plt.text(ind, val , str(round(val,2)),ha='center', va='bottom' )

def get_amount_df(chat_id, data_code , type="overall"):
    ### plot overall expenses
    individual_expenses, shared_expenses = [] ,[]
    if type not in ["shared"]:
        if data_code in [2,4]:
            for i in expense_dict[chat_id]['personal_expenses']:
                individual_expenses.append(i.split(','))
    #print("get amount expense dict run")
    if data_code in [3,4]:
        for j in expense_dict[chat_id]['group_expenses']:
            temp_dict = transaction_dict[j]
            shared_expenses.append([temp_dict['created_at'], temp_dict['category'],temp_dict['members'][chat_id]])       
    total_expenses = individual_expenses + shared_expenses
    total_expenses_df = pd.DataFrame(total_expenses,columns = ['Date','Category','Amount'])
    total_expenses_df['Amount'] = total_expenses_df['Amount'].astype(float)
    total_expenses_df['Date'] = pd.to_datetime(total_expenses_df['Date'], format=dateFormat + ' ' + timeFormat)
    return total_expenses_df

