'''File: test_cl.py'''
import os
import sys
import unittest
import argparse
from argparse import Namespace
from unittest.mock import patch, MagicMock
import cl
from app import app
from cl import get_parsed_arguments

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestCL(unittest.TestCase):
    '''Test class for the command line interface (CLI) for the project.'''
    def setUp(self):
        self.mock_conn = MagicMock()
        self.mock_cursor = self.mock_conn.cursor.return_value
        self.app = app.test_client()

    #####################################################
    ###########            Compare            ###########
    #####################################################
    @patch("cl.datasource_top.DataSource")
    @patch("cl.datasource_compare.DataSource")
    @patch("cl.datasource_activities.DataSource")
    @patch("cl.get_parsed_arguments")
    def test_main_compare(self, mock_get_args, mock_datasource_class, activities, age):
        '''tests the main compare function'''
        parameter_list = [mock_get_args, mock_datasource_class, None, 23,
                                "Sleeping", None, None, (559,552), "compare_by_age"]
        self.main_helper_method(parameter_list)

        with patch("builtins.print") as mock_print:
            cl.main()
            mock_print.assert_called_once_with("For people age 23 they engaged in Sleeping on " \
            "average 559 hours in 2022 & 2023 and 552 hours in 2012 & 2013")

    #####################################################
    ###########        Get Cat/Sub/Act        ###########
    #####################################################
    @patch("cl.datasource_top.DataSource")
    @patch("cl.datasource_compare.DataSource")
    @patch("cl.datasource_activities.DataSource")
    @patch("cl.get_parsed_arguments")
    def test_main_category_subcategory(self, mock_get_args, mock_datasource_class, compare, age):
        '''tests the main function for category and subcategory'''
        parameter_list = [mock_get_args, mock_datasource_class, None, None, None,
                                "Personal Care Activities", "Sleeping",
                                ["Sleeping", "Sleeplessness"], "get_activity_list"]
        self.main_helper_method(parameter_list)
        with patch("builtins.print") as mock_print:
            cl.main()
            mock_print.assert_called_once_with(["Sleeping", "Sleeplessness"])

    @patch("cl.datasource_top.DataSource")
    @patch("cl.datasource_compare.DataSource")
    @patch("cl.datasource_activities.DataSource")
    @patch("cl.get_parsed_arguments")
    def test_main_category_only(self, mock_get_args, mock_datasource_class, compare, age):
        '''tests the main function for category only'''
        parameter_list = [mock_get_args, mock_datasource_class, None, None, None,
                                "Personal Care Activities", None, ["Sleeping", "Grooming"],
                                "get_subcategory_list"]
        self.main_helper_method(parameter_list)
        with patch("builtins.print") as mock_print:
            cl.main()
            mock_print.assert_called_once_with(["Sleeping", "Grooming"])

    @patch('cl.check_validity')
    @patch.object(sys, 'argv', ['cl.py', '--category', 'Personal Care Activities'])
    def test_get_parsed_args(self, mock_check_validity):
        '''tests the get_parsed_arguments function'''
        args = get_parsed_arguments()
        self.assertEqual(args.category, 'Personal Care Activities')
        mock_check_validity.assert_called_once_with(args)

    @patch("cl.datasource_top.DataSource")
    @patch("cl.datasource_compare.DataSource")
    @patch("cl.datasource_activities.DataSource")
    def test_validate_category_valid(self, mock_datasource_class, compare, age):
        '''tests the validate_category function'''
        self.validating_helper_method(mock_datasource_class,
                                      ["sub", "Sleeping", "Grooming"], None, None)
        try:
            cl.validate_category("Personal Care Activities", "Sleeping")
        except cl.InvalidCategoryError:
            self.fail("validate_category() raised InvalidCategoryError")

        mock_datasource_class.return_value.get_subcategory_list.assert_called_once_with(
            "Personal Care Activities")

    @patch("cl.datasource_top.DataSource")
    @patch("cl.datasource_compare.DataSource")
    @patch("cl.datasource_activities.DataSource")
    def test_validate_category_invalid(self, mock_datasource_class, compare, age):
        '''tests the validate_category function'''
        self.validating_helper_method(mock_datasource_class,
                                      ["sub", "Sleeping", "Grooming"], None, None)
        with self.assertRaises(cl.InvalidCategoryError):
            cl.validate_category("Invalid_category", "invalid_subcategory")

        mock_datasource_class.return_value.get_subcategory_list.assert_called_once()

    @patch("cl.datasource_top.DataSource")
    @patch("cl.datasource_compare.DataSource")
    @patch("cl.datasource_activities.DataSource")
    def test_validate_activity_valid(self, mock_datasource_class, compare, age):
        '''tests the validate_activity function'''
        self.validating_helper_method(mock_datasource_class, ["act", "Sleeping"],
                                      True, "T0101")
        try:
            cl.validate_activity("Sleeping")
        except cl.InvalidCategoryError:
            self.fail("validate_activity() raised InvalidCategoryError")

    @patch("cl.datasource_top.DataSource")
    @patch("cl.datasource_compare.DataSource")
    @patch("cl.datasource_activities.DataSource")
    def test_validate_activity_invalid(self, mock_datasource_class, compare, age):
        '''tests the validate_activity function returns an error for invalid activity'''
        self.validating_helper_method(mock_datasource_class, ["act", "Sleeping"],
                                      True, "Error getting subcategory from activities:")
        with self.assertRaises(cl.InvalidCategoryError):
            cl.validate_activity("Carleton")

        mock_datasource_class.return_value.get_activity_list.assert_called_once()

    @patch("cl.validate_category")
    @patch("cl.validate_activity")
    def test_check_validity(self, mock_validate_activity, mock_validate_category):
        '''tests the check_validity function'''
        args= argparse.Namespace(category= 'Personal Care Activities', subcategory = 'Sleeping',
                                 activity='Sleeping', age= None, top= None, compare= None )
        cl.check_validity(args)
        mock_validate_category.assert_called_once_with('Personal Care Activities', 'Sleeping')
        mock_validate_activity.assert_called_once_with("Sleeping")

    #####################################################
    ###########    Get Top Activity By Age    ###########
    #####################################################
    @patch("cl.datasource_top.DataSource")
    @patch("cl.datasource_compare.DataSource")
    @patch("cl.datasource_activities.DataSource")
    @patch("cl.get_parsed_arguments")
    def test_main_top_activity(self, mock_get_args, mock_datasource_class, compare, age):
        '''tests the main function'''
        parameter_list = [mock_get_args, mock_datasource_class, 23,
                                None, None, None, None, "Sleeping", "get_top_by_age"]
        self.main_helper_method(parameter_list)
        with patch("builtins.print") as mock_print:
            cl.main()
            mock_print.assert_called_once_with("Sleeping")

    #####################################################
    ###########        Helper Methods         ###########
    #####################################################
    def main_helper_method(self, parameter_list):
        '''helper method for the main function'''
        mock_args = Namespace(
        age=parameter_list[2],
        compare=parameter_list[3], activity=parameter_list[4],
        category=parameter_list[5], subcategory=parameter_list[6]
        )
        mock_get_args = parameter_list[0]
        mock_datasource_class = parameter_list[1]
        answer_list = parameter_list[7]
        list_type = parameter_list[8]

        mock_get_args.return_value = mock_args
        mock_source = self.mock_source_return_value(answer_list, list_type)
        mock_datasource_class.return_value = mock_source

    def mock_source_return_value(self, answer_list, list_type):
        '''helper to  mock source return value based on list_type '''
        mock_source = MagicMock()

        if list_type == "get_subcategory_list":
            mock_source.get_subcategory_list.return_value = answer_list
        elif list_type == "get_activity_list":
            mock_source.get_activity_list.return_value = answer_list
        elif list_type == "get_top_by_age":
            mock_source.get_top_by_age.return_value = answer_list
        elif list_type == "compare_by_age":
            mock_source.compare_by_age.return_value = answer_list

        return mock_source

    def validating_helper_method(self, mock_datasource_class,
                                 type_and_results, activities, activities_list):
        '''helper method for the validate_category functions'''
        mock_instance= MagicMock()
        if type_and_results[0] == "sub":
            mock_instance.get_subcategory_list.return_value = type_and_results[1:]
        elif type_and_results[0] == "act":
            mock_instance.get_activity_list.return_value = type_and_results[1:]
        if activities:
            mock_instance.get_subcategory_from_activity.return_value = activities_list
        mock_datasource_class.return_value = mock_instance

if __name__ == '__main__':
    unittest.main()
