'''file: load_data.py'''
import csv

def load_data():
    ''' Purpose: Load data from a file
    Returns: None'''
    print("Loading data from file...")
    with open("Data/teamproject22-23FINAL_updatedpls.csv", "r", encoding='utf-8') as file:
        reader=csv.DictReader(file)
        data = list(reader)
        return data
    
def load_categories():
    '''Purpose: loads category IDs and their category
    Returns: None
    '''
    with open("Data/Categories_Data.csv", "r") as file:
        reader = csv.DictReader(file)
        data = list(reader)
        return data
