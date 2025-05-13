'''File: test_cl.py'''
import os
import sys
import unittest
import argparse
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

    def test_main_compare(self): 
        pass
    
    def test_main_category_subcategory(self):
        pass

    def test_main_category_only(self):
        pass

    
    ####################################################
    ##########     EVERYTHING BELOW IS OK     ##########
    ####################################################
    # def test_get_parsed_category(self):
    #     '''tests the get_parsed_arguments function'''
    #     script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'cl.py'))
    #     process = subprocess.run([sys.executable, script_path, '--category', 'Personal_Care_Activities'], capture_output=True, text=True)
    #     print(f"category process: {process}")
    #     self.assertEqual(process.returncode, 0)

    @patch.object(sys, 'argv', ['cl.py', '--category', 'Personal_Care_Activities'])
    def test_get_parsed_category(self):
        args = get_parsed_arguments()
        self.assertEqual(args.category, 'Personal_Care_Activities')

    # def test_get_parsed_age(self):
    #     '''tests the get_parsed_arguments function'''
    #     script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'cl.py'))
    #     process = subprocess.run([sys.executable, script_path, '--age', '23'], capture_output=True, text=True)
    #     print(f"age process: {process}")
    #     self.assertEqual(process.returncode, 0)

    # def test_get_parsed_subcategory(self):
    #     '''tests the get_parsed_arguments function'''
    #     script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'cl.py'))
    #     process = subprocess.run([sys.executable, script_path, '--subcateogry', 'Sleeping'], capture_output=True, text=True)
    #     print(f"subcategory process: {process}")
    #     self.assertEqual(process.returncode, 0)

    # def test_get_parsed_compare(self):
    #     '''tests the get_parsed_arguments function'''
    #     script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'cl.py'))
    #     process = subprocess.run([sys.executable, script_path, '--compare', '23'], capture_output=True, text=True)
    #     print(f"compare process: {process}")
    #     self.assertEqual(process.returncode, 0)

    # def test_get_parsed_activity(self):
    #     '''tests the get_parsed_arguments function'''
    #     script_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'cl.py'))
    #     process = subprocess.run([sys.executable, script_path, '--Activity', 'Laundry'], capture_output=True, text=True)
    #     print(f"activity process: {process}")
    #     self.assertEqual(process.returncode, 0)
    
    @patch("cl.datasource.DataSource")
    def test_validate_category_valid(self, mock_datasource_class):
        '''tests the validate_category function'''
        # this can be a helper used in several methods
        mock_instance= MagicMock()
        mock_instance.get_subcategory_list.return_value = ["Sleeping", "Grooming"]
        mock_datasource_class.return_value = mock_instance

        try: 
            cl.validate_category("Personal_Care_Activities", "Sleeping")
        except cl.InvalidCategoryError:
            self.fail("validate_category() raised InvalidCategoryError")
        
        mock_instance.get_subcategory_list.assert_called_once_with("Personal_Care_Activities")

    @patch("cl.datasource.DataSource")
    def test_validate_category_invalid(self, mock_datasource_class):
        '''tests the validate_category function'''
        mock_instance= MagicMock()
        mock_instance.get_subcategory_list.return_value = ["Sleeping", "Grooming"]
        mock_datasource_class.return_value = mock_instance

        with self.assertRaises(cl.InvalidCategoryError):
            cl.validate_category("Invalid_category", "invalid_subcategory")

        mock_instance.get_subcategory_list.assert_called_once()
 
    @patch("cl.datasource.DataSource")
    def test_validate_activity_valid(self, mock_datasource_class):
        '''tests the validate_activity function'''
        mock_instance= MagicMock()
        mock_instance.get_activity_list.return_value = ["Sleeping"]
        mock_instance.get_subcategory_from_activity.return_value = "T0101"
        mock_datasource_class.return_value = mock_instance

        try: 
            cl.validate_activity("Sleeping")
        except cl.InvalidCategoryError:
            self.fail("validate_activity() raised InvalidCategoryError")
    
    @patch("cl.datasource.DataSource")
    def test_validate_activity_invalid(self, mock_datasource_class):
        mock_instance= MagicMock()
        mock_instance.get_activity_list.return_value = "Usage: python3 " \
            "cl.py --compare <age 15-80> --activity <valid activity>"
        mock_instance.get_activity_list.return_value = ["Sleeping"]
        mock_instance.get_subcategory_from_activity.return_value = "Error getting subcategory from activities:"
        mock_datasource_class.return_value = mock_instance

        with self.assertRaises(cl.InvalidCategoryError):
            cl.validate_activity("Carleton")

        mock_instance.get_activity_list.assert_called_once()

    @patch("cl.validate_category")
    @patch("cl.validate_activity")
    def test_check_validity(self, mock_validate_activity, mock_validate_category):
        '''tests the check_validity function'''
        args= argparse.Namespace(category= 'Personal_Care_Activities', subcategory = 'Sleeping',activity='Sleeping', age= None, top= None, compare= None )
        cl.check_validity(args)
        mock_validate_category.assert_called_once_with('Personal_Care_Activities', 'Sleeping')
        mock_validate_activity.assert_called_once_with("Sleeping")

    @patch("cl.datasource.DataSource")
    @patch("cl.get_parsed_arguments")
    def test_main_top_activity(self, mock_get_args, mock_datasource_class):
        '''tests the main function'''
    
        #fake CLI args
        mock_args= MagicMock()
        mock_args.age = 23
        mock_args.top = True
        mock_args.category = None
        mock_args.subcategory = None 
        mock_args.compare = None
        mock_args.activity = None

        # this can be a helper used in several methods
        mock_instance= MagicMock()
        mock_instance.get_top_by_age.return_value = "Sleeping"
        mock_datasource_class.return_value = mock_instance

        with patch("builtins.print") as mock_print:
            cl.main()
            mock_print.assert_called_once_with("Sleeping")

if __name__ == '__main__':
    unittest.main()
