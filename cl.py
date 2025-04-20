'''
File: cl.py
The eventual location for the command line interface (CLI) for the project.
This will be the entry point for the project when run from the command line.
'''

import argparse
import sys
from ProductionCode.loadData import load_data
#usually this: from ProductionCode.getAge import get_most_common_top_activity
from ProductionCode.getAge import get_most_common_top_activity


def get_parsed_arguments():
    '''parse the command line arguments
    returns: the parsed arguments (argparse.Namespace)'''
    # python3 cl.py -- age 20 -- top 1 
    # get the top activity for people of age 20 
    parser = argparse.ArgumentParser(description="Get the most common activity for a given age group")
    parser.add_argument("--age", "-a", type=int, help="the age group to get the most common activity for")
    parser.add_argument("--top", "-t", type=int, help="the number of activities to get (ex: n=5 for top 5)")
    args = parser.parse_args()
    
    ######figure out how to have this work with the category 
    # python3 cl.py -- category "exercise" 
    # get a list of activities within a category
    #parser = argparse.ArgumentParser(description="Get a list of activities within a category")
    #parser.add_argument("--category", type=str, help="the category to get the activities for")
    #args = parser.parse_args()
    return args

def main(): 
    args = get_parsed_arguments()
    data = load_data()

    #if user puts --age and --top then call getAge()
    if args.age is not None and args.top is not None:
            most_common_top_activity = get_most_common_top_activity(args.age, args.top)
            print(most_common_top_activity)
 
if __name__ == "__main__":
   main()
