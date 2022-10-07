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


def test_read_json():
    filename = "test_user_expenses.json" 
    filepath = os.path.join("data","testdata",filename)
    try:
        if os.stat(filepath).st_size != 0:
            with open(filepath) as expense_record:
                expense_record_data = json.load(expense_record)
            return expense_record_data

    except FileNotFoundError:
        print("---------NO RECORDS FOUND---------")
        
def check_individual_present_shared_absent():
    test_dict = test_read_json()
    ret_val = plots.check_data_present("5457678456",test_dict)
    assert rat_val == 2
    
def check_individual_absent_shared_present():
    test_dict = test_read_json()
    ret_val = plots.check_data_present("5898398328",test_dict)
    assert rat_val == 3
    
def check_individual_absent_shared_absent():
    test_dict = test_read_json()
    ret_val = plots.check_data_present("5555511111",test_dict)
    assert rat_val == 1  
    
def check_individual_present_shared_present():
    test_dict = test_read_json()
    ret_val = plots.check_data_present("4583959357",test_dict)
    assert rat_val == 4 