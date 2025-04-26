'''file: load_data.py'''
import csv

def load_data(dataset):
    ''' Purpose: Load data from a file
    Returns: None'''
    print("Loading data from file...")
    with open(str(dataset), "r", encoding='utf-8') as file:
        reader=csv.DictReader(file)
        data = list(reader)
        return data
