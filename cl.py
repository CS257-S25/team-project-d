'''
The eventual location for the command line interface (CLI) for the project.
This will be the entry point for the project when run from the command line.
'''

import argparse
import sys
from loadData import load_data

# python3 cl.py -- age 20 -- top 1 
# get the top activity for people of age 20 

# python3 cl.py -- category "exercise" 
# get a list of activities within a category

def get_parsed_arguments():
    '''parse the command line arguments
    returns: the parsed arguments (argparse.Namespace)'''
    parser = argparse.ArgumentParser(description="Get the most common activity for a given age group")
    parser.add_argument("--age", type=int, help="the age group to get the most common activity for")
    parser.add_argument("--top", type=int, help="the number of activities to get")
    args = parser.parse_args()
    
    parser2 = argparse.ArgumentParser(description="Get a list of activities within a category")
    parser2.add_argument("--category", type=str, help="the category to get the activities for")
    args2 = parser2.parse_args()
    return args
