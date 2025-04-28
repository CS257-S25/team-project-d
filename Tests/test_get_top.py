'''file: test_get_top.py --- tests for get_top_by_age.py'''
import os
import sys
import unittest
from io import StringIO
from unittest.mock import patch
import cl
from ProductionCode.get_top_by_age import get_matching_rows
from ProductionCode.get_top_by_age import process_row_for_activity, get_top_activity_from_row
from ProductionCode.get_top_by_age import count_top_activites, get_most_common_top_activity

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestGetTop(unittest.TestCase):
    '''class to test stuff from get_top_by_age'''
    def output_usage_for_age(self):
        '''helper method to call main from cl
        returns: usage message (str)
        simplifies repeated calls to main'''
        sys.stdout = StringIO()
        try:
            cl.main()
        except ValueError:
            print("Usage: python3 cl.py --age <age from 15-85> --top")

    #patch where the function is looked up not where it's defined
    @patch("ProductionCode.get_top_by_age.load_data")
    def test_get_matching_rows(self, mock_load_data):
        '''tests the get_matching_rows function
        verifies the method returns a list of rows that match the age given'''
        mock_load_data.return_value = [
            {"age":"23", "T050101": "5", "T050102": "1", "T050103": "1"},
            {"age":"23", "T050101": "5", "T050102": "1", "T050103": "3"},
            {"age":"57", "T050101": "3", "T050102": "1", "T050103": "3"}
        ]
        rows = get_matching_rows(23)
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
        expected = {"T050101": 2}
        self.assertEqual(result, expected)

    @patch("ProductionCode.get_top_by_age.get_matching_rows")
    def test_get_most_common_top_activity(self, mock_get_matching_rows):
        '''test the get_most_common_top_activity function
        verifies the method returns the most common activity for the age group given
        '''
        mock_get_matching_rows.return_value = [
            {"age":"23", "T050101": "5", "T050102": "1", "T050103": "1"},
            {"age":"23", "T050101": "5", "T050102": "1", "T050103": "3"}
        ]
        result = get_most_common_top_activity(23)
        self.assertEqual(result, ("T050101",'Work_main_job' ))

    #Acceptance tests for User Story 1:
    @patch('ProductionCode.get_top_by_age.load_data')
    @patch("ProductionCode.get_top_by_age.get_matching_rows")
    def test_acceptance_valid_age(self, mock_get_matching_rows, mock_load_data):
        '''test if the function returns the correct category ID and number of times it is top'''
        mock_load_data.return_value = [
            {"Activity_ID": "T050101", "Activity_Name": "Work_main_job"},
            {"Activity_ID": "T050102", "Activity_Name": "Other_work"},
            {"Activity_ID": "T050103", "Activity_Name": "Another_work"}
        ]
        mock_get_matching_rows.return_value = [
            {"age": "23", "T050101": "5", "T050102": "1", "T050103": "1"},
            {"age": "23", "T050101": "5", "T050102": "1", "T050103": "3"}
        ]

        sys.argv = ["cl.py", "--age", "23", "--top"]
        sys.stdout = StringIO()
        cl.main()

        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "('T050101', 'Work_main_job')")

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
        sys.argv = ["cl.py", "--age", "-5"]
        with self.assertRaises(SystemExit) as cm:
            self.output_usage_for_age()
        self.assertEqual(cm.exception.code,2)

if __name__ == '__main__':
    unittest.main()
