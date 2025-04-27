'''
File: cl.py
The eventual location for the command line interface (CLI) for the project.
This will be the entry point for the project when run from the command line.
'''
import argparse
import sys
from ProductionCode.get_activity_by_category import get_activities_from_subcategory, get_list_of_subcategories
from ProductionCode.get_top_by_age import get_most_common_top_activity
from shared_logic import get_the_subcategories

class InvalidCategoryError(Exception):
    '''exception raised for invalid category or subcategory'''
    pass

def get_parsed_arguments():
    '''parse the command line arguments
    returns: the parsed arguments (argparse.Namespace)'''
    # python3 cl.py -- age 20 -- top
    # get the top activity for people of age 20
    parser = argparse.ArgumentParser(description="Get the top activity for a given age group")
    parser.add_argument("--age", "-a", type=int, choices = range(15,85),
                         help="the age (15-85) to get the top activity for")
    parser.add_argument("--top", "-t", action='store_true', help="the top activity")
    parser.add_argument("--category", type=str, help="the category to get the activities for")
    parser.add_argument("--subcategory", type=str, help="the subcategory to get the activities for")
    args = parser.parse_args()

    check_validity(args)

    return args

def validate_category(category, subcategory = None):
    valid_subcategories = get_list_of_subcategories(category)

    if not valid_subcategories: 
        raise InvalidCategoryError("Usage: python3 cl.py --category <valid category>")
    
    if subcategory and subcategory not in valid_subcategories:
        raise InvalidCategoryError("Usage: python3 cl.py --category <valid category> --subcategory " \
            "<valid subcategory> \n reference python3 cl.py --category for valid subcategory inputs")


def check_validity(args):
    '''checks if the category and subcategory are valid'''
    if args.category:
        validate_category(args.category, args.subcategory)

def main():
    '''main function for the command line interface'''
    args = get_parsed_arguments()

    if args.age is not None and args.top is not None:
        most_common_top_activity = get_most_common_top_activity(args.age)
        print(most_common_top_activity)

    elif args.category is not None and args.subcategory is not None:
        list_of_activities = get_activities_from_subcategory(args.subcategory)
        print(list_of_activities)

    elif args.category is not None:
        list_of_subcategories = get_the_subcategories(args.category)
        print(list_of_subcategories)
if __name__ == "__main__":
    main()
