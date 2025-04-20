'''file: loadData.py'''

import csv

def load_data():
    ''' Purpose: Load data from a file
    Returns: None'''
    print("Loading data from file...")
    #this loads the data needed for get_top_by_age.py 
    with open("Data/teamproject22-23FINAL_updatedpls.csv", "r") as file:
        reader=csv.DictReader(file)
        data = list(reader)
        return data

