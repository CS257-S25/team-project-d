'''This is the Test file to use'''
import os
import sys
import unittest
from io import StringIO
from unittest.mock import patch
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import cl
from ProductionCode.get_top_by_age import get_matching_rows, load_matching_rows
from ProductionCode.get_top_by_age import process_row_for_activity, get_top_activity_from_row
from ProductionCode.get_top_by_age import count_top_activites, get_most_common_top_activity
from ProductionCode.getActivtyByCategory import load_category_data, load_subcategory_data
from ProductionCode.getActivtyByCategory import load_activity_data, get_category_from_data
from ProductionCode.getActivtyByCategory import get_list_of_subcategories, get_list_of_activities
from shared_logic import get_the_subcategories

class TestCL(unittest.TestCase):
    '''Test class for the command line interface (CLI) for the project.'''
    def setUp(self):
        self.category_data = load_category_data()
        self.subcategory_data = load_subcategory_data()
        self.activity_data = load_activity_data()

    @patch("ProductionCode.data",#get_top_by_age.py would return (T050101,2) for age 23
        ["23, 5, 1, 1 "],
        ["57, 1, 5, 3"],
        ["23, 5, 1, 3"] )#age, hours for T050101, T050102, T050103
    def output_usage_for_age(self):
        '''helper method to call main from cl
        returns: usage message (str)
        simplifies repeated calls to main'''
        sys.stdout = StringIO()
        try:
            cl.main()
            output = sys.stdout.getvalue().strip()
        except ValueError:
            print("Usage: python3 cl.py --age <age from 15-85> --top")
            return

    ##### TESTS FOR USER STORY 1: get_top_by_age --- getting the top activity by age #####
    # tests for the functions in get_top_by_age.py
    def test_get_matching_rows(self):
        '''tests the get_matching_rows function
        verifies the method returns the correct number of rows that match the age given'''
        rows = get_matching_rows(23)
        self.assertEqual(len(rows), 2)

    def test_load_matching_rows(self):
        '''tests the load_matching_rows function
        verifies the method returns a list of rows that match the age given'''
        rows = load_matching_rows(23)
        self.assertEqual(rows, [
            ["23", "5", "1", "1"],
            ["23", "5", "1", "3"]
        ])

    def test_process_row_for_activity(self):
        '''tests the process_row_for_activity function
        verifies the method returns a dictionary of the activity hours for the row given'''
        row = ["23", "5", "1", "3"]
        result = process_row_for_activity(row)
        self.assertEqual(result, {
            "T050101": 5,
            "T050102": 1,
            "T050103": 3
        })

    def test_get_top_activity_from_rows(self):
        '''tests the get_top_activity_from_row function
        veriifies the method returns the top activity for the rows given'''
        rows = [
            ["23", "5", "1", "1"],
            ["23", "5", "1", "3"]
        ]
        result = get_top_activity_from_row(rows)
        self.assertEqual(result, ["T050101", "T050101"])

    def test_count_top_activites(self):
        '''tests the count_top_activites function
        verifies the method returns a dictionary of the top activities and their counts'''
        top_activities =["T050101, T050101, T050103"]
        result = count_top_activites(top_activities)
        self.assertEqual(result, {
            "T050101": 2,
            "T050103": 1
        })

    def test_get_most_common_top_activity(self):
        '''test the get_most_common_top_activity function
        verifies the method returns the most common activity for the age group given
        '''
        counts= {"T050101": 2, "T050103": 1}
        result = get_most_common_top_activity(counts, 2)
        self.assertEqual(result, ("T050101", 2))

        #tie case
        counts = {"T050101": 2, "T050103": 2}
        result = get_most_common_top_activity(counts, 2)
        self.assertEqual(result, ("T050101", 2))#returns the first one in the list
        pass

    #acceptance tests for user story 1 for get_top_by_age
    ''' User story: a user wants to know the most common activity for a given age group
    Acceptance tests:
    1) given they input a valid age group (ex: (int) 18)---> the program should return the most common activity for that age group
    2) given they input an invalid age group format (ex: (str) "eighteen")---> the program should return usage statement
    3) given they input an invalid age group/ out of range/no data (ex: (int) 200)---> the program should return usage statement, message that says no data available valid: 15-85
    '''

    def test_acceptance_valid_age(self):
        '''test if the function returns the correct category ID and number of times it is top'''
        self.assertEqual(cl.get_most_common_top_activity(23, 1), "T050101, 2")

    def test_acceptance_invalid_age_format(self):
        '''test if the function returns usage statement for invalid age format'''
        sys.argv = ["cl.py", "--age", "eighteen"]
        with self.assertRaises(ValueError):
            self.output_usage_for_age()

    def test_acceptance_invalid_age_range(self):# the range is 15-85
        '''test if the function returns usage statement for invalid age range'''
        sys.argv = ["cl.py", "--age", "200"]
        with self.assertRaises(ValueError):
            self.output_usage_for_age()

    ##### TESTS FOR USER STORY 2: getActivtyByCategory --- getting the activities by category #####
    def test_get_category_from_data(self):
        '''tests the get_category_from_data function and Acceptance Test 1
        test if the function returns T01 for the category Personal Care Activities'''
        self.assertEqual('T01', get_category_from_data('Personal Care Activities'))

    def test_get_list_of_subcategories(self):
        '''tests the get_list_of_subcategories function and Acceptance Test 2
        test if the function returns ['Interior cleaning', 'Laundry'] given the cateogry ID'''
        self.assertEqual("['Interior cleaning', 'Laundry']", get_list_of_subcategories("T02"))

    def test_get_list_of_activities(self):
        '''tests get_list_of_activities from getActivityByCategory
        test if the function returns ['Interior cleaning', 'Laundry'] given the subcategory name'''
        self.assertEqual("['Interior cleaning', 'Laundry']", get_list_of_activities("Housework"))

    def output_usage_for_category(self):
        '''helper method to call main from cl
        returns: usage message (str)
        simplifies repeated calls to main'''
        sys.stdout = StringIO()
        cl.main()
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "Usage: python3 cl.py --category <'Personal Care Activities' or 'Household Activities'>")

    def test_invalid_category(self):
        '''test an invalid category for Acceptance Test 3
        '''
        sys.argv = 'Astronaut'
        self.output_usage_for_category()

    def output_usage_for_subcategory(self):
        '''helper method to call main from cl
        returns: usage message (str)
        simplifies repeated calls to main'''
        sys.stdout = StringIO()
        cl.main()
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "Usage: python3 cl.py --category <valid category> --subcategory <valid subcategory> " \
        "\n reference python3 cl.py --category for valid subcategory inputs")

    def test_invalid_subcategory(self):
        '''test an invalid subcategory for Acceptance Test 3
        '''
        sys.argv = 'Astronaut'
        self.output_usage_for_subcategory()
