# -*- coding: utf-8 -*-
"""
Created on Thu Oct  6 17:19:18 2022

@author: DELL
"""

## test cases

import os
import json
from main import plots
from main import helper
import datetime

def test_read_expense_json():
    filename = "test_user_expenses.json" 
    filepath = os.path.join("data","testdata",filename)
    try:
        if os.stat(filepath).st_size != 0:
            with open(filepath) as expense_record:
                expense_record_data = json.load(expense_record)
            return expense_record_data

    except FileNotFoundError:
        print("---------NO RECORDS FOUND---------")
        
        
def test_read_transaction_json():
    filename = "test_group_expenses.json" 
    filepath = os.path.join("data","testdata",filename)
    try:
        if os.stat(filepath).st_size != 0:
            with open(filepath) as expense_record:
                expense_record_data = json.load(expense_record)
            return expense_record_data

    except FileNotFoundError:
        print("---------NO RECORDS FOUND---------")
        
def check_individual_present_shared_absent():
    test_dict = test_read_expense_json()
    ret_val = plots.check_data_present("5457678456",test_dict)
    assert ret_val == 2
    
def check_individual_absent_shared_present():
    test_dict = test_read_expense_json()
    ret_val = plots.check_data_present("5898398328",test_dict)
    assert ret_val == 3
    
def check_individual_absent_shared_absent():
    test_dict = test_read_expense_json()
    ret_val = plots.check_data_present("5555511111",test_dict)
    assert ret_val == 1  
    
def check_individual_present_shared_present():
    test_dict = test_read_expense_json()
    ret_val = plots.check_data_present("4583959357",test_dict)
    assert ret_val == 4 
    
def check_overall_plot_noData():
    test_dict = test_read_expense_json()
    trans_dict = test_read_transaction_json()
    start_date = datetime.datetime(2021,12,12)
    end_date = datetime.datetime(2022,1,12)
    ret_val = plots.overall_plot("5555511111", start_date, end_date,test_dict,trans_dict)
    assert ret_val == 1 
    
    
def check_overall_plot_noDataforDates():
    test_dict = test_read_expense_json()
    trans_dict = test_read_transaction_json()
    start_date = datetime.datetime(2021,12,12)
    end_date = datetime.datetime(2022,1,12)
    ret_val = plots.overall_plot("4583959357", start_date, end_date,test_dict,trans_dict)
    assert ret_val == 5 
    
    
def check_categorical_plot_noDataforDatesAndCat():
    test_dict = test_read_expense_json()
    trans_dict = test_read_transaction_json()
    start_date = datetime.datetime(2021,12,12)
    end_date = datetime.datetime(2022,1,12)
    ret_val = plots.categorical_plot("4583959357", start_date, end_date, "Food",test_dict,trans_dict)
    assert ret_val == 6 
    
def check_categorical_plot_noData():
    test_dict = test_read_expense_json()
    trans_dict = test_read_transaction_json()
    start_date = datetime.datetime(2021,12,12)
    end_date = datetime.datetime(2022,1,12)
    ret_val = plots.categorical_plot("5555511111", start_date, end_date, "Food",test_dict,trans_dict)
    assert ret_val == 1
    
    
def check_owe_plot_noData():
    test_dict = test_read_expense_json()
    trans_dict = test_read_transaction_json()
    ret_val = plots.owe("5555511111",test_dict,trans_dict)
    assert ret_val == 1    
    
    
def check_owe_plot_noSharedData():
    test_dict = test_read_expense_json()
    trans_dict = test_read_transaction_json()
    ret_val = plots.owe("5457678456",test_dict,trans_dict)
    assert ret_val == 2    