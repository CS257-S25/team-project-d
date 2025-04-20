import argparse
import csv
from loadData import load_data
from cl import args, args2

# python3 cl.py -- category "exercise" 
# get a list of activities within a category


def get_parsed_arguments():
    '''return the user's parsed arguments'''
    if (args2)
    category = args2.category
    pass

def get_list_of_subcategories(category):
    '''return a list of the subcategories in the category'''
    pass










def something():
    sub_categories_list = get_list_of_activities_from_category()
    sub_sub_categories_list = get_sub_categories_list
    pass

def get_category():
    '''return name of category given in cl'''
    #args2.category
    category = args2.category
    return category

def get_list_of_activities_from_category():
    '''returns a list of activities from the specified category'''
    category_name = get_category()
    data = load_data()
    mock_data = ["Personal Care Activities", ]
    list_of_activities = []
    for activity in data:
        if category_name == mock_data[activity]:
            list_of_activities.append(activity)
    return list_of_activities

def get_sub_categories_list():
    pass
def display_list_of_activities():
    '''prints the list of activities from the specified category'''
    pass
'''**TO get a list of activities in a category, we first create an empty list and iterate through all of the data to find activities in the category and add them to the list.**
def get_activity_from_category(activity_category)
List_of_activities = []
For activity in data:
		If category == activity_category
			Add activity to List_of_activities
Return list_of_activities in activity_category #example: running, basketball, etc. 

**TO print everything in a specific category group, we print all of the activities in the category that the user specifies**
def display_list_of_activities()
Print get_activity_from_category(cl args)


User cl : – activity category “exercise”'''



# python3 cl.py -- category "exercise" 
# get a list of activities within a category
def get_category():
    ''''return: a list of activities within the category given in cl'''
    pass

# python3 cl.py -- age 20 -- top 1 
# get the top activity for people of age 20 
def get_age():
    ''''return: a list of rows/people with the age given in cl'''
    pass

def get_top_activity():
    ''''checks each row for the activity with the most hours
    returns: the name of the activity with the most hours for each row 
    and puts it in a list or something
    then we will see how many times each activity is in the list so we can see which one is the most'''
    pass