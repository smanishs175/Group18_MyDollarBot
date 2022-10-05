# -*- coding: utf-8 -*-
"""

@author: Palash
"""

import matplotlib.pyplot as plt
import pandas as pd
import helper




dateFormat = '%d-%b-%Y'
timeFormat = '%H:%M'
monthFormat = '%b-%Y'

month_dict = {1 : 'Jan', 2 : 'Feb', 3 : 'Mar',
              4 : 'Mar', 5 : 'Apr', 6 : 'Jun',
              7 : 'Jul', 8 : 'Aug', 9 : 'Sep',
              10: 'Oct', 11: 'Nov', 12: 'Dec'}

def label_amount(y):
    for ind,val in enumerate(y):
        plt.text(ind, val , str(round(val,2)),ha='center', va='bottom' )

def get_amount_df(chat_id,type="overall"):
    ### plot overall expenses
    individual_expenses, shared_expenses = [] ,[]
    if type not in ["shared"]:
        for i in final_dict[chat_id]['data']:
            individual_expenses.append(i.split(','))
    for j in final_dict[chat_id]['transactions']:
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
    plt.title("Total Expenses (for the Dates Selected)")
    plt.ylabel('Amount ($)')
    plt.xlabel('Category')
    plt.xticks(rotation=45)
    label_amount(sum_df['Amount'])
    plt.bar(sum_df['Category'],sum_df['Amount'],color='rgbymck')
    #plt.savefig('expenditure.png', bbox_inches='tight')
    
    
def categorical_plot(chat_id, start_date, end_date,selected_cat):  
    total_expenses_df = get_amount_df(chat_id,type="overall")
    total_expenses_df = total_expenses_df[total_expenses_df['Date'] >= start_date]
    total_expenses_df = total_expenses_df[total_expenses_df['Date'] <= end_date]
    total_expenses_df = total_expenses_df[total_expenses_df['Category'].isin([selected_cat])]
    total_expenses_df['Month'] = total_expenses_df['Date'].apply(lambda x: month_dict[x.month])
    sum_df = total_expenses_df[['Month','Amount']].groupby(['Month'],as_index = False).sum()
    
    plt.title("Expenses (for the Dates Selected)")
    plt.ylabel('Amount ($)')
    plt.xlabel('Month')
    #plt.xticks(rotation=45)
    label_amount(sum_df['Amount'])
    plt.bar(sum_df['Month'],sum_df['Amount'],color='rgbymck')
    #plt.savefig('expenditure.png', bbox_inches='tight')