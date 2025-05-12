'''This is the Test file to use'''
import os
import sys
import unittest
from io import StringIO
from unittest.mock import patch, MagicMock
import cl
from app import app
from cl import get_parsed_arguments, validate_category, check_validity
from cl import validate_activity, main

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestCL(unittest.TestCase):
    '''Test class for the command line interface (CLI) for the project.'''
    def setUp(self):
        #create a mock connection and cursor
        self.mock_conn = MagicMock() 
        self.mock_cursor = self.mock_conn.cursor.return_value
        self.app = app.test_client()

        # mock_get_top_by_age.return_value = self.mock_conn
        # self.mock_cursor.fetchall.return_value = "the top activity for people age 23 is Sleeping"
        # response = get_top_by_age(23)
        # self.assertEqual("the top activity for people age 23 is Sleeping", response)

    def test_get_parsed_arguments(self, mock_get_parsed_arguments):
        '''tests the get_parsed_arguments function'''
        mock_get_parsed_arguments.return_value = self.mock_conn
        # Mock the command line arguments   
        self.mock_cursor.fetchall.return_value = ['cl.py', '--category', 'Personal_Care_Activities']
        # Call the function to test
        response = get_parsed_arguments()
        # Check if the response is as expected
        self.assertEqual(response.category, 'Personal_Care_Activities')
        # Check if the other arguments are None
        self.assertIsNone(response.subcategory)
        self.assertIsNone(response.activity)
        self.assertIsNone(response.age)
        self.assertIsNone(response.compare)
        self.assertIsNone(response.top)
        
    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_validate_category(self, mock_validate_category):
        '''tests the validate_category function'''
        mock_validate_category.return_value = self.mock_conn
        pass

    def test_check_validity(self, mock_check_validity):
        '''tests the check_validity function'''
        mock_check_validity.return_value = self.mock_conn
        pass

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_validate_activity(self, mock_validate_activity):
        '''tests the validate_activity function'''
        mock_validate_activity.return_value = self.mock_conn
        pass

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_main(self, mock_main):
        '''tests the main function'''
        mock_main.return_value = self.mock_conn
        pass

if __name__ == '__main__':
    unittest.main()
