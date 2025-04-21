'''This is the Test file to use'''
import unittest
import cl
import sys
from unittest import patch
from io import StringIO
from ProductionCode.get_top_by_age import *

class TestCL(unittest.TestCase):
    def setUp(self):
        @patch ("ProductionCode.core.data", #get_top_by_age.py would return (T050101,2) for age 23
            ["23, 5, 1, 1 "]
            ["57, 1, 5, 3"]
            ["23, 5, 1, 3"] ) #age, hours for T050101, T050102, T050103
        
        @patch("ProductionCode.core.data2",
            ["T050101, insert_name_of_activity"],)  
              
    def output_usage_for_age(self):
        '''helper method to call main from cl
        returns: usage message (str)
        simplifies repeated calls to main'''
        sys.stdout = StringIO()
        cl.main()
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "Usage: python3 cl.py --age <age from 15-85> --top")
    
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
        self.asserEqual(rows, [
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
        self.assertEqual(result, ("T050101", 2)) #returns the first one in the list
        pass
    
    #acceptance tests for user story 1 for get_top_by_age
    ''' User story: a user wants to know the most common activity for a given age group
    Acceptance tests:
    1) given they input a valid age group (ex: (int) 18)---> the program should return the most common activity for that age group
    2) given they input an invalid age group format (ex: (str) "eighteen")---> the program should return usage statement
    3) given they input an invalid age group/ out of range/no data (ex: (int) 200)---> the program should return usage statement, message that says no data available valid: 15-85
    "'''
    def test_acceptance_valid_age(self):
        self.assertEqual(cl.get_most_common_top_activity(23, 1), "T050101, 2")

    def test_acceptance_invalid_age_format(self):
        '''test if the function returns usage statement for invalid age format'''
        sys.argv = ["cl.py", "--age", "eighteen"]
        self.output_usage_for_age()

    def test_acceptance_invalid_age_range(self): #the range is 15-85 i thinkkkkk
        '''test if the function returns usage statement for invalid age range'''
        sys.argv = ["cl.py", "--age", "200"]
        self.output_usage_for_age()
