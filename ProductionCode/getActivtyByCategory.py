import argparse
import csv
from shared_logic import get_the_subcategories

#Future: including more categories and subcategories to work with
#Future: organize loading functions into a separate file

#Finding the general types of activities of a certain category
#Usage: python3 cl.py --category <valid category> 
#       python3 cl.py --category <"Personal Care Activities" or "Household Activities">
#Returns the subcategories of the category given

#Finding the activities of a certain valid subcategory
#Usage: python3 cl.py --category <valid category> --subcategory <valid subcategory> 
#       python3 cl.py --category <"Personal Care Activities"> --subcategory <"Sleeping">
#Returns a list of activities of the subcategory given

def load_category_data():
    '''Purpose: loads the general categories data from the file
    Args: None
    Returns: a list of dicitionaries containing the categories data from the file'''
    with open("Data/Categories_Data_test.csv", "r") as file:

        reader=csv.DictReader(file)
        data = list(reader)
        return data

def load_subcategory_data():
    '''Purpose: loads the subcategories data from the file
    Args: None
    Returns: a list of dicitionaries containing the subcategories data from the file'''
    with open("Data/SubCategories_data.csv", "r") as file:

        reader=csv.DictReader(file)
        data = list(reader)

        return data
    
def load_activity_data():
    '''Purpose: loads the activities data from the file
    Args: None
    Returns: a list of dicitionaries containing the activities data from the file'''
    with open("Data/Activities_data.csv", "r") as file:

        reader=csv.DictReader(file)
        data = list(reader)

        return data

def get_category_from_data(category):
    '''Purpose: gets the category ID from the selected category
    Args: category: the category to get the ID for
    Returns: the ID of the category'''
    data = load_category_data()
    for row in data:
        # checks to see if the category is in the row
        if row['Category'] == category:
            # if it is, it returns the ID stored in the row
            return row['Activity_ID']
    print("No data available found for category {category}, try Personal Care Activities or Household Activities")
    return None

def get_subcategory_from_data(subcategory):
    '''Purpose: gets the ID of the selected subcategory
    Args: subcategory: the subcategory to get the ID for
    Returns: the ID of the subcategory'''
    data = load_subcategory_data()
    for row in data:
        # checks to see if the subcategory is in the row
        if row['Activity_Name'] == subcategory:
            # if it is, it returns the ID stored in the row
            return row['Activity_ID']
    print("Usage: python3 cl.py --category <valid category> --subcategory " \
        "<valid subcategory> \n reference python3 cl.py --category for valid subcategory inputs")
    return None

def get_list_of_subcategories(category):
    '''Purpose: gets the list of subcategories from the selected category
    Args: category: the category to get the subcategories for
    Returns: a list of subcategories in the category'''
    # gets the ID of the category
    category_ID = get_category_from_data(category)
    # the array will store the subcategories
    subcategories = []
    data = load_subcategory_data()
    for row in data:
        # checks to see if the last two numbers of the current row's ID, match the ID of the category
        if (row['Activity_ID'][:-2] == category_ID):
            # if it does, the subcategory is added to the array
            subcategories.append(row['Activity_Name'])

    return subcategories

def get_activities_from_subcategory(category, subcategory):
    '''Purpose: gets the list of activities from the selected subcategory
    Args: category: the category to get the activities for
          subcategory: the subcategory to get the activities for
    Returns: a list of activities in the subcategory'''
    #gets the ID of the subcategory
    subcategory_ID = get_subcategory_from_data(subcategory)
    #gets the list of subcategories
    subcategories = get_list_of_subcategories(category)
    # the array will store the activities belonging to the subcategory
    activities = []
    data = load_activity_data()
    for row in data:
        # checks to see if the first five numbers (including the 'T') of the current row's ID, match the ID of the subcategory
        if (row['Activity_ID'][:5] == subcategory_ID):
            # if it does, the activity is added to the array
            activities.append(row['Activity_Name'])

    return activities
 