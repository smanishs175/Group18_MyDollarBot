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

def check_data_present(chat_id):
   ## checking if chat id has any data
   '''
   1 : data not present in both individual data and shared transactions
   2 : data present in individual data but not in shared transactions
   3 : data present in shared transaction but not in individual data
   4 : data present in both individual data and shared transactions
   '''
   #data_present, transaction_present = 99 , 99 
   if chat_id not in expense_dict.keys():
       # chat_id is not present in expense_dict
       return 1
   elif expense_dict[chat_id]['personal_expenses'] == []:
       #data_present = 0
       if 'group_expenses' not in expense_dict[chat_id].keys():
           #transaction_present = 0
           return 1
       elif expense_dict[chat_id]['group_expenses'] == []:
           #transaction_present = 0
           return 1
       else:
           #transaction_present = 1
           return 3
   else:
       #data_present = 1
       if 'group_expenses' not in expense_dict[chat_id].keys():
           #transaction_present = 0
           return 2
       elif expense_dict[chat_id]['group_expenses'] == []:
           #transaction_present = 0
           return 2
       else:
           #transaction_present = 1
           return 4


def overall_plot(chat_id, start_date, end_date): 
    check_data_val = check_data_present(chat_id) 
    if check_data_val == 1:
        return 1
    else:
        total_expenses_df = get_amount_df(chat_id, check_data_val, type="overall" )
        total_expenses_df = total_expenses_df[total_expenses_df['Date'] >= start_date]
        total_expenses_df = total_expenses_df[total_expenses_df['Date'] <= end_date]
        sum_df = total_expenses_df[['Category','Amount']].groupby(['Category'],as_index = False).sum()
        ## check if df is blank
        if sum_df.shape[0] == 0:
            return 5 ## 5 means "No expense data for selected dates"
        else:
            rand_val = np.random.randint(1,5000)
            plt.figure(rand_val)
            plt.title("Total Expenses (for the Dates Selected)")
            plt.ylabel('Amount ($)')
            plt.xlabel('Category')
            plt.xticks(rotation=45)
            label_amount(sum_df['Amount'])
            plt.bar(sum_df['Category'],sum_df['Amount'],color=['r', 'g', 'b', 'y', 'm', 'c', 'k'])
            plt.savefig('overall_expenses.png', bbox_inches='tight')
            return 7