'''file: test_get_top.py --- tests for get_top_by_age.py'''
import os
import sys
import unittest
from io import StringIO
from unittest.mock import patch
from unittest.mock import mock_open
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
import cl
from ProductionCode.get_top_by_age import get_matching_rows, load_matching_rows
from ProductionCode.get_top_by_age import process_row_for_activity, get_top_activity_from_row
from ProductionCode.get_top_by_age import count_top_activites, get_most_common_top_activity

class TestGetTop(unittest.TestCase):
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
    @patch("ProductionCode.get_top_by_age.load_data", 
           #get_top_by_age.py would return (T050101,2) for age 23
        return_value= [
            {"age":"23", "T050101": "5", "T050102": "1", "T050103": "1"},
            {"age":"23", "T050101": "5", "T050102": "1", "T050103": "3"}
        ])

    #patch where the function is looked up not where it's defined
    @patch("ProductionCode.get_top_by_age.load_data") #get_top_by_age.py would return (T050101,2) for age 23
    def test_get_matching_rows(self, mock_load_data):
        '''tests the load_matching_rows function
        verifies the method returns a list of rows that match the age given'''
        mock_load_data.return_value = [
            {"age":"23", "T050101": "5", "T050102": "1", "T050103": "1"},
            {"age":"23", "T050101": "5", "T050102": "1", "T050103": "3"},
            {"age":"57", "T050101": "3", "T050102": "1", "T050103": "3"}
        ]
        rows = load_matching_rows(23)
        self.assertEqual(rows, [
            {"age":"23", "T050101": "5", "T050102": "1", "T050103": "1"},
            {"age":"23", "T050101": "5", "T050102": "1", "T050103": "3"}
        ])

    def test_process_row_for_activity(self):
        '''tests the process_row_for_activity function
        verifies the method returns a dictionary of the activity hours for the row given'''
        row = {"age":"23", "T050101": "5", "T050102": "1", "T050103": "3"}
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
            {"age":"23", "T050101": "5", "T050102": "1", "T050103": "1"},
            {"age":"23", "T050101": "5", "T050102": "1", "T050103": "3"}
        ]
        expected = ["T050101", "T050101"]
        results = []
        for row in rows:
            activity_hours = process_row_for_activity(row)
            top_activity = get_top_activity_from_row(activity_hours)
            results.append(top_activity)
        self.assertEqual(results, expected)

    def test_count_top_activites(self):
        '''tests the count_top_activites function
        verifies the method returns a dictionary of the top activities and their counts'''
        matching_rows =[
            {"age":"23", "T050101": "5", "T050102": "1", "T050103": "1"},
            {"age":"23", "T050101": "5", "T050102": "1", "T050103": "3"}
        ]
        result = count_top_activites(matching_rows)
        expected = {"T050101": 2} #should this be {"T050101": 2} or  {'T050101': 2, 'T050103': 1}
        self.assertEqual(result, expected)

    @patch("ProductionCode.get_top_by_age.load_matching_rows")
    def test_get_most_common_top_activity(self, mock_load_matching_rows):
        '''test the get_most_common_top_activity function
        verifies the method returns the most common activity for the age group given
        '''
        mock_load_matching_rows.return_value = [
            {"age":"23", "T050101": "5", "T050102": "1", "T050103": "1"},
            {"age":"23", "T050101": "5", "T050102": "1", "T050103": "3"}
        ]
        result = get_most_common_top_activity(23)
        self.assertEqual(result, ("T050101", 2))


    #acceptance tests for user story 1 for get_top_by_age
    ''' User story: a user wants to know the most common activity for a given age group
    Acceptance tests:
    1) given they input a valid age group (ex: (int) 18)---> the program should return the most common activity for that age group
    2) given they input an invalid age group format (ex: (str) "eighteen")---> the program should return usage statement
    3) given they input an invalid age group/ out of range/no data (ex: (int) 200)---> the program should return usage statement, message that says no data available valid: 15-85
    '''
    @patch("ProductionCode.get_top_by_age.get_matching_rows", 
        return_value=[
        {"age":"23", "T050101": "5", "T050102": "1", "T050103": "1"},
        {"age":"23", "T050101": "5", "T050102": "1", "T050103": "3"}
    ])
    def test_acceptance_valid_age(self, mock_load_data):
        '''test if the function returns the correct category ID and number of times it is top'''
        self.assertEqual(cl.get_most_common_top_activity(23, 1), ("T050101", 2))

    def test_acceptance_invalid_age_format(self):
        '''test if the function returns usage statement for invalid age format'''
        sys.argv = ["cl.py", "--age", "eighteen"]
        with self.assertRaises(SystemExit):
            self.output_usage_for_age()

    def test_acceptance_invalid_age_range(self):# the range is 15-85
        '''test if the function returns usage statement for invalid age range'''
        sys.argv = ["cl.py", "--age", "200"]
        with self.assertRaises(SystemExit) as cm:
            self.output_usage_for_age()
        self.assertEqual(cm.exception.code,2)

if __name__ == '__main__':
    unittest.main()
