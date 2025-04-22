'''
File: cl.py
The eventual location for the command line interface (CLI) for the project.
This will be the entry point for the project when run from the command line.
'''
import argparse
from ProductionCode.getActivtyByCategory import get_activities_from_subcategory
from ProductionCode.get_top_by_age import get_most_common_top_activity
from shared_logic import get_list_of_subcategories

def get_parsed_arguments():
    '''parse the command line arguments
    returns: the parsed arguments (argparse.Namespace)'''
    # python3 cl.py -- age 20 -- top
    # get the top activity for people of age 20
    parser = argparse.ArgumentParser(description="Get the top activity for a given age group")
    parser.add_argument("--age", "-a", type=int, help="the age group to get the top activity for")
    parser.add_argument("--top", "-t", action='store_true', help="the top activity")
    parser.add_argument("--category", type=str, help="the category to get the activities for")
    parser.add_argument("--subcategory", type=str, help="the subcategory to get the activities for")
    args = parser.parse_args()
    return args

def main():
    '''main function for the command line interface'''
    args = get_parsed_arguments()

    #if user puts --age and --top,
    # get the most common activity for that age group w/ get_most_common_top_activity
    if args.age is not None and args.top is not None:
        most_common_top_activity = get_most_common_top_activity(args.age, args.top)
        print(most_common_top_activity)

    elif args.category is not None and args.subcategory is not None:
        list_of_activities = get_activities_from_subcategory(args.category, args.subcategory)
        print(list_of_activities)
    #if user puts --category then call getActivtyByCategory()
    elif args.category is not None:
        list_of_subcategories = get_list_of_subcategories(args.category)
        print(list_of_subcategories)
if __name__ == "__main__":
    main()
