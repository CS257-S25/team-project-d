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
    with open("Data/SubCategories_Data_test.csv", "r") as file:

        reader=csv.DictReader(file)
        data = list(reader)

        return data

def get_category_from_data(category):
    '''return category ID from the category data'''
    data = load_category_data()
    #print(data)
    #print("Type of data:", type(data))
    #print(data[0]['Category'])
    for row in data:
        #print("row: "+row)
        #print("category: "+category)
        #print("IM HERE")
        #print("row['Activity_Name']: "+row['Activity_Name'])
        #print("category: "+category)
        #category = "Household Activities"
        #print("Row get: "+row.get('Activity_Name'))
        if row['Category'] == category:
            print("supposed category ID: "+row['Activity_ID'])
            return row['Activity_ID']
    print("Category not found")
    return None

def get_list_of_subcategories(category):
    '''return a list of the subcategories in the category'''
    category_ID = get_category_from_data(category)
    subcategories = []
    data = load_subcategory_data()
    for row in data:
        #print("row['Activity_ID'][:-4]: "+row['Activity_ID'][:-4])
        #print("category_ID: "+category_ID)
        if (row['Activity_ID'][:-4] == category_ID):
            subcategories.append(row['Activity_Name'])
            print("got appended to the subcategories list: "+row['Activity_Name'])

    return subcategories

#def get_activities_from_subcategory(category, subcategory):
 
 #   '''return a list of activities in the subcategory'''
  #  pass