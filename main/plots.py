# -*- coding: utf-8 -*-
"""

@author: Palash
"""

import matplotlib.pyplot as plt
import pandas as pd
import helper
import numpy as np
 

dateFormat = '%d-%b-%Y'
timeFormat = '%H:%M'
monthFormat = '%b-%Y'
expenseFile = "expense_record.json"
transactionFile = "transaction_record.json"
month_dict = {1 : 'Jan', 2 : 'Feb', 3 : 'Mar',
              4 : 'Mar', 5 : 'Apr', 6 : 'Jun',
              7 : 'Jul', 8 : 'Aug', 9 : 'Sep',
              10: 'Oct', 11: 'Nov', 12: 'Dec'}

user_key = {"5718815807": "palash_jhamb@outlook.com",
                "5745784966": "nihar.rao@gmail.com",
                "5706237421": "shruti.v@gmail.com",
                '5713840988': "saksham.pandey@gmail.com"}

## getting json files
expense_dict = helper.read_json(expenseFile)
transaction_dict = helper.read_json(transactionFile)

def label_amount(y):
    for ind,val in enumerate(y):
        plt.text(ind, val , str(round(val,2)),ha='center', va='bottom' )

def get_amount_df(chat_id,type="overall"):
    ### plot overall expenses
    individual_expenses, shared_expenses = [] ,[]
    if type not in ["shared"]:
        for i in expense_dict[chat_id]['data']:
            individual_expenses.append(i.split(','))
    print("get amount expense dict run")
    for j in expense_dict[chat_id]['transactions']:
        temp_dict = transaction_dict[j]
        shared_expenses.append([temp_dict['created_at'], temp_dict['category'],temp_dict['members'][chat_id]])       
    total_expenses = individual_expenses + shared_expenses
    total_expenses_df = pd.DataFrame(total_expenses,columns = ['Date','Category','Amount'])
    total_expenses_df['Amount'] = total_expenses_df['Amount'].astype(float)
    total_expenses_df['Date'] = pd.to_datetime(total_expenses_df['Date'], format=dateFormat + ' ' + timeFormat)
    return total_expenses_df
    
def overall_plot(chat_id, start_date, end_date):  
    total_expenses_df = get_amount_df(chat_id,type="overall")
    total_expenses_df = total_expenses_df[total_expenses_df['Date'] >= start_date]
    total_expenses_df = total_expenses_df[total_expenses_df['Date'] <= end_date]
    sum_df = total_expenses_df[['Category','Amount']].groupby(['Category'],as_index = False).sum()
    rand_val = np.random.randint(1,5000)
    plt.figure(rand_val)
    plt.title("Total Expenses (for the Dates Selected)")
    plt.ylabel('Amount ($)')
    plt.xlabel('Category')
    plt.xticks(rotation=45)
    label_amount(sum_df['Amount'])
    plt.bar(sum_df['Category'],sum_df['Amount'],color=['r', 'g', 'b', 'y', 'm', 'c', 'k'])
    plt.savefig('overall_expenses.png', bbox_inches='tight')
    
    
def categorical_plot(chat_id, start_date, end_date,selected_cat):
    total_expenses_df = get_amount_df(chat_id,type="overall")
    total_expenses_df = total_expenses_df[total_expenses_df['Date'] >= start_date]
    total_expenses_df = total_expenses_df[total_expenses_df['Date'] <= end_date]
    total_expenses_df = total_expenses_df[total_expenses_df['Category'].isin([selected_cat])]
    total_expenses_df['Month'] = total_expenses_df['Date'].apply(lambda x: month_dict[x.month])
    sum_df = total_expenses_df[['Month','Amount']].groupby(['Month'],as_index = False).sum()
    rand_val = np.random.randint(5001,10000)
    plt.figure(rand_val)
    plt.title("Expenses (for the Dates Selected)")
    plt.ylabel('Amount ($)')
    plt.xlabel('Month')
    #plt.xticks(rotation=45)
    label_amount(sum_df['Amount'])
    plt.bar(sum_df['Month'],sum_df['Amount'],color=['r', 'g', 'b', 'y', 'm', 'c', 'k'])
    plt.savefig('categorical_expenses.png', bbox_inches='tight')
    helper.date_range=[]




def owe(chat_id):
    all_ids = []
    for j in expense_dict[chat_id]['transactions']:
        all_ids+= transaction_dict[j]['members'].keys()
        all_ids = list(set(all_ids))
        all_ids.remove(chat_id)
    
    owe_dict = {}
    for m in all_ids:
        owe_dict[m] = []    
    for j in expense_dict[chat_id]['transactions']:
        temp_dict = transaction_dict[j]
        creator_id = temp_dict['created_by']
        if chat_id == creator_id:
            for c_id in temp_dict['members'].keys():
                if c_id != chat_id:
                    owe_dict[c_id] = owe_dict[c_id] + [temp_dict['members'][c_id]]
        else:
            owe_dict[creator_id] = owe_dict[creator_id] + [-1 * (temp_dict['members'][chat_id] )]
    
    x,y= [] , [] 
    for k in owe_dict.keys():
        val = owe_dict[k] 
        if val != []:
            x.append(user_key[k])
            y.append(sum(val)*-1)# what I owe will be positive on plot

    rand_val = np.random.randint(10001,15000)
    plt.figure(rand_val)            
    plt.title("What I owe")
    plt.ylabel('Amount ($)')
    plt.xlabel('User')
    #plt.xticks(rotation=45)
    label_amount(y)
    plt.bar(x,y,color=['r', 'g', 'b', 'y', 'm', 'c', 'k'])
    plt.savefig('owe.png', bbox_inches='tight')
    
    

