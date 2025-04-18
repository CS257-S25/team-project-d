'''
The eventual location for the command line interface (CLI) for the project.
This will be the entry point for the project when run from the command line.
'''

import argparse
import sys

# idk if all this is supposed to go here or if we are supposed to make a different file but yeah
def load_data():
    ''' Purpose: Load data from a file
    Returns: None'''
    file_name = open("dummy_data.csv", "r")
    print("Loading data from file...")

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

def get_most_common_top_activity():
    ''' figures out which top activity is the most common in the list
    returns: the name of the most common top activity (future: list of top names ex top 5) '''
    pass

# python3 cl.py -- category "exercise" 
# get a list of activities within a category
