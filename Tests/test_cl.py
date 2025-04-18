'''This is the Test file to use'''
import unittest
import cl
import sys
from io import StringIO

class TestCL(unittest.TestCase):
    def setUp(self):
    #mock data for testing
        cl.data1= [
            # ID, Age, tv, basketball, sleeping, lifting
            ["p1", 20, 120, 30, 40, 50], 
            ["p2", 20. 60, 69, 36, 66],
            ["p3", 30, 70, 35, 14, 21],
            ["p4", 45, 55, 89, 71, 2], 
            ["p5", 20, 12. 100, 89, 36]
        ]
    
        cl.data2 = [
            #activity, category
            ["TV", "entertainment"],
            ["basketball", "exercise"],
            ["sleeping", "rest"],
            ["lifting", "exercise"]
        ]
    def output_usage_for_age(self):
        '''helper method to call main from cl
        returns: usage message (str)
        simplifies repeated calls to main'''
        sys.stdout = StringIO()
        cl.main()
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "Usage: python3 cl.py --age <age> --top <number of activities>")
    def test_get_age(self):
        pass

