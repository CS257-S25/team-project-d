''' File: cl.py '''
import argparse
import ProductionCode.datasource as datasource

class InvalidCategoryError(Exception):
    '''exception raised for invalid category or subcategory'''

def get_parsed_arguments():
    '''parse the command line arguments
    returns: the parsed arguments (argparse.Namespace)'''
    parser = argparse.ArgumentParser(description="Get the top activity for a given age group")
    parser.add_argument("--age", "-a", type=int, choices = range(15,81),
                         help="the age (15-80) to get the top activity for")
    parser.add_argument("--top", "-t", action='store_true', help="the top activity")
    parser.add_argument("--category", type=str, help="the category to get the activities for")
    parser.add_argument("--subcategory", type=str, help="the subcategory to get the activities for")
    parser.add_argument("--compare", "-c", type=int, choices = range(15,81),
                        help="the age (15-80) to compare the activity for")
    parser.add_argument("--activity", type=str, help="the activity to compare for a given age")
    args = parser.parse_args()

    check_validity(args)

    return args

def validate_category(category, subcategory = None):
    '''helper method for check valid category and subcategory'''
    source = datasource.DataSource()
    valid_subcategories = source.get_subcategory_list(category)

    if not valid_subcategories:
        raise InvalidCategoryError("Usage: python3 cl.py --category <valid category>")

    if subcategory and subcategory not in valid_subcategories:
        raise InvalidCategoryError(
            "Usage: python3 cl.py --category <valid category> --subcategory <valid subcategory> " \
            "\n reference python3 cl.py --category for valid subcategory inputs")

def check_validity(args):
    '''checks if the category and subcategory are valid'''
    if args.category:
        validate_category(args.category, args.subcategory)

    if args.activity:
        validate_activity(args.activity)

def validate_activity(activity):
    '''helper method to check if the activity is valid'''
    source = datasource.DataSource()
    subcategory = source.get_subcategory_from_activity(activity)
    valid_activities = source.get_activity_list(subcategory)
    if activity not in valid_activities:
        raise InvalidCategoryError(
            "Usage: python3 cl.py --compare <age 15-80> --activity <valid activity>")

def main():
    '''main function for the command line interface'''
    source = datasource.DataSource()
    args = get_parsed_arguments()

    if args.age is not None and args.top is not None:
        most_common_top_activity = source.get_top_by_age(args.age)
        print(most_common_top_activity)

    elif args.compare is not None and args.activity is not None:
        hours = source.compare_by_age(args.compare, args.activity)
        print("For people age " + str(args.compare) + " they engaged in " + str(args.activity) \
            + " on average " + str(hours[0]) \
            + " hours in 2022 & 2023 and " + str(hours[1]) + " hours in 2012 & 2013")

    elif args.category is not None and args.subcategory is not None:
        list_of_activities = source.get_activity_list(args.subcategory)
        print(list_of_activities)

    elif args.category is not None:
        list_of_subcategories = source.get_subcategory_list(args.category)
        print(list_of_subcategories)

if __name__ == "__main__":
    main()
