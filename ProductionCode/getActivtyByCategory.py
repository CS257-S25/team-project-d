import argparse
import csv
#from loadData import load_data
from cl import args, args2

# python3 cl.py -- category "exercise" 
# get a list of activities within a category

'''file: loadData.py'''

def load_category_data():

    print("Loading data from file...")
    with open("Data/Categories_Data - Hoja 1", "r") as file:

        reader=csv.DictReader(file)
        data = list(reader)

        return data

def load_subcategory_data():
    print("Loading data from file...")
    with open("Data/Subcategories_Data - Hoja 4 (1)", "r") as file:

        reader=csv.DictReader(file)
        data = list(reader)

        return data

def get_list_of_activities():
    '''return the list of activities from the subcategory of the category from the user's input'''
    list_of_activities = []
    if (args.category):
        category = args2.category
        get_list_of_subcategories(category)

    elif (args2.category and args2.subcategory):
        category = args2.category
        subcategory = args2.subcategory
        get_activities_from_subcategory(category, subcategory)

    else:
        print("no arguments provided")
    return list_of_activities

def get_category_from_data(category):
    '''return category ID from the data'''
    data = load_category_data()
    for row in data:
        if (category in row):
            return row[0]
    print("Category not found")
    return None

def get_list_of_subcategories(category):
    '''return a list of the subcategories in the category'''
    category_ID = get_category_from_data(category)
    subcategories = []
    data = load_subcategory_data()
    for row in data:
        if (row[0].startswith(category_ID)):
            subcategories.append(row[1])

    return subcategories

def get_activities_from_subcategory(category, subcategory):
    '''return a list of activities in the subcategory'''
    pass