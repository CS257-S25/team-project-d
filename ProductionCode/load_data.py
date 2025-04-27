'''file: load_data.py'''
import csv

def load_data(filepath):
    ''' Purpose: Load data from a file
    Returns: None'''
    print("Loading data from file...")
    with open(str(filepath), "r", encoding='utf-8') as file:
        reader=csv.DictReader(file)
        data = list(reader)
        return data
