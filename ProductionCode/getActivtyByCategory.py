import argparse
import csv
#from loadData import load_data
from shared_logic import get_list_of_activities

# python3 cl.py -- category "exercise" 
# get a list of activities within a category

'''file: loadData.py'''

def load_category_data():
    '''loads the general categories data from the file'''

    #print("Loading category data from file...")
    with open("Data/Categories_Data_test.csv", "r") as file:

        reader=csv.DictReader(file)
        data = list(reader)
        #print("Data loaded successfully")
        return data

def load_subcategory_data():
    '''loads the subcategories data from the file'''
    #print("Loading subcategory data from file...")
    with open("Data/SubCategories_data.csv", "r") as file:

        reader=csv.DictReader(file)
        data = list(reader)

        return data
def load_activity_data():
    '''loads the activities data from the file'''
    #print("Loading activity data from file...")
    with open("Data/Activities_data.csv", "r") as file:

        reader=csv.DictReader(file)
        data = list(reader)

        return data

def get_category_from_data(category):
    '''return category ID from the category data'''
    data = load_category_data()
    for row in data:
        if row['Category'] == category:
            return row['Activity_ID']
    print("Category not found")
    return None

def get_subcategory_from_data(subcategory):
    '''return subcategory ID from the subcategory data'''
    data = load_subcategory_data()
    for row in data:
        if row['Activity_Name'] == subcategory:
            return row['Activity_ID']
    print("Subcategory not found")
    return None

def get_list_of_subcategories(category):
    '''return a list of the subcategories in the category'''
    category_ID = get_category_from_data(category)
    subcategories = []
    data = load_subcategory_data()
    for row in data:
        #print("row['Activity_ID'][:-2]: "+row['Activity_ID'][:-2])
        #print("category_ID: "+category_ID)
        if (row['Activity_ID'][:-2] == category_ID):
            subcategories.append(row['Activity_Name'])
            #print("got appended to the subcategories list: "+row['Activity_Name'])

    return subcategories

def get_activities_from_subcategory(category, subcategory):
    '''return a list of activities in the subcategory'''

    category_ID = get_subcategory_from_data(subcategory)
    subcategories = get_list_of_subcategories(category)
    activities = []
    data = load_activity_data()
    for row in data:
        print("row['Activity_ID'][:4]: "+row['Activity_ID'])
        print("ROW HERE")
        print(row)
        #print("category_ID: "+category_ID)
        print(category_ID)
        if (row['Activity_ID'][:5] == category_ID and row['Activity_Name'] == subcategory):
            activities.append(row['Activity_Name'])
            print("got appended to the activities list: "+row['Activity_Name'])

    return activities
 #   '''return a list of activities in the subcategory'''
  #  pass