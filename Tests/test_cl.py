'''This is the Test file to use'''
import os
import sys
import unittest
from io import StringIO
from unittest.mock import patch, MagicMock
import cl
import subprocess
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

    def test_get_parsed_arguments(self):
        '''tests the get_parsed_arguments function'''
        script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'cl.py'))
        process = subprocess.run([sys.executable, script_path, '--category', 'Personal_Care_Activities'], capture_output=True, text=True)
        self.assertEqual(process.returncode, 0)
        
    @patch("ProductionCode.datasource")
    def test_validate_category(self, mock_validate_category):
        '''tests the validate_category function'''
        mock_validate_category.return_value = self.mock_conn
        self.mock_cursor.fetchall.return_value = [('T01','Personal_Care_Activities')]
        print(f"here: {self.mock_cursor.fetchall.return_value}")
        result = validate_category('Personal_Care_Activities')
        print(f"result: {result}")
        self.assertEqual(result, 'Personal_Care_Activities')

    @patch("ProductionCode.datasource")
    def test_check_validity(self, mock_check_validity):
        '''tests the check_validity function'''
        mock_check_validity.return_value = self.mock_conn
        pass

    @patch("ProductionCode.datasource")
    def test_validate_activity(self, mock_validate_activity):
        '''tests the validate_activity function'''
        mock_validate_activity.return_value = self.mock_conn
        pass

    @patch("ProductionCode.datasource")
    def test_main(self, mock_main):
        '''tests the main function'''
        mock_main.return_value = self.mock_conn
        pass

if __name__ == '__main__':
    unittest.main()
