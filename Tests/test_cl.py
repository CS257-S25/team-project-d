'''This is the Test file to use'''
import unittest
import cl
import sys
from unittest import patch
from io import StringIO



class TestCL(unittest.TestCase):
    def setUp(self):
    #mock data for testing
    # ID, Age, tv, basketball, sleeping, lifting
        @patch ("ProductionCode.core.data", 
            ["p1", 20, 120, 30, 40, 50], 
            ["p2", 20. 60, 69, 36, 66],
            ["p3", 30, 70, 35, 14, 21],
            ["p4", 45, 55, 89, 71, 2], 
            ["p5", 20, 12. 100, 89, 36])
        
    #activity, category
        @patch ("ProductionCode.core.data2",
            ["TV", "entertainment"],
            ["basketball", "exercise"],
            ["sleeping", "rest"],
            ["lifting", "exercise"])
        
    def output_usage_for_age(self):
        '''helper method to call main from cl
        returns: usage message (str)
        simplifies repeated calls to main'''
        sys.stdout = StringIO()
        cl.main()
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "Usage: python3 cl.py --age <age> --top <number of activities>")
    
    ##### TESTS FOR USER STORY 1: getAge --- getting the top n activities by age #####
    # tests for the finctions in getAge.py
    def test_get_matching_rows(self):
        pass

    def test_get_top_activity(self):
        pass

    def test_get_most_common_top_activity(self):
        pass
    
    #acceptance tests for user story 1 for getAge 
    ''' User story: a user wants to know the most common activity for a given age group
    Acceptance tests:
    1) given they input a valid age group (ex: (int) 18)---> the program should return the most common activity for that age group
    2) given they input an invalid age group format (ex: (str) "eighteen")---> the program should return usage statement
    3) given they input an invalid age group/ out of range/no data (ex: (int) 200)---> the program should return usage statement, message that says no data available
    "'''
    

