'''This is the Test file to use'''
import os
import sys
import unittest
from io import StringIO
from unittest.mock import patch
import cl
from ProductionCode.get_activity_by_category import load_category_data, load_subcategory_data
from ProductionCode.get_activity_by_category import load_activity_data, get_category_from_data
from ProductionCode.get_activity_by_category import get_list_of_subcategories
from ProductionCode.get_activity_by_category import get_activities_from_subcategory
from shared_logic import get_the_subcategories
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

class TestCL(unittest.TestCase):
    '''Test class for the command line interface (CLI) for the project.'''
    def setUp(self):
        self.category_data = load_category_data()
        self.subcategory_data = load_subcategory_data()
        self.activity_data = load_activity_data()

    @patch("ProductionCode.get_activity_by_category.get_category_from_data")
    def test_get_category_from_data(self, mock_get_category_from_data):
        '''tests the get_category_from_data function and Acceptance Test 1
        test if the function returns T01 for the category Personal Care Activities'''
        mock_get_category_from_data.return_value = "T01" #might not be needed
        self.assertEqual('T01', get_category_from_data('Personal_Care_Activities'))

    @patch("ProductionCode.get_activity_by_category.load_subcategory_data")
    def test_get_list_of_subcategories(self, mock_load_sub_data):
        '''tests the get_list_of_subcategories function and Acceptance Test 2
        test if the function returns correct thing given the cateogry ID'''
        mock_load_sub_data.return_value = [
            {"Activity_ID": "T0201", "Activity_Name": "Housework"},
            {"Activity_ID": "T0202",
                "Activity_Name":"Food_&_Drink_Preparation/Presentation/Clean-Up"},
            {"Activity_ID": "T0301", "Activity_Name": "rats"}
        ]
        result = get_list_of_subcategories("Household_Activities")
        self.assertEqual(["Housework", "Food_&_Drink_Preparation/Presentation/Clean-Up"], result)

    @patch("shared_logic.get_the_subcategories")
    def test_get_the_subcategories(self, mock_get_the_subcategories):
        '''tests get_the_subcategories from shared_logic.py
        test if the function returns ['Sleeping', 'Grooming'] given the category name'''
        mock_get_the_subcategories.return_value = ['Sleeping', 'Grooming']
        result = get_the_subcategories("Personal_Care_Activities")
        self.assertEqual(['Sleeping', 'Grooming','Health-related_self_care',
                          'Personal_Activities','Personal_Care_Emergencies'], result)

    @patch("ProductionCode.get_activity_by_category.get_activities_from_subcategory")
    def test_get_activities_from_subcategory(self, mock_get_activities_from_subcategory):
        '''tests get_activity_from_subcategory from get_activity_by_category
        test if the function returns ['Interior_cleaning', 'Laundry', 
        'Sewing_repairing_&_maintaining_textiles', 'Storing_interior_hh_items_inc._food'] 
        given the subcategory name'''
        mock_get_activities_from_subcategory.return_value = ['Interior_cleaning', 'Laundry',
            'Sewing_repairing_&_maintaining_textiles', 'Storing_interior_hh_items_inc._food']
        result = get_activities_from_subcategory('Housework')
        self.assertEqual(['Interior_cleaning', 'Laundry',
            'Sewing_repairing_&_maintaining_textiles',
            'Storing_interior_hh_items_inc._food'], result)
        
    @patch("ProductionCode.get_activity_by_category.get_activities_from_subcategory")
    def test_invalid_get_activities_from_subcategory(self, mock_get_activities_from_subcategory):
        '''tests get_activity_from_subcategory from get_activity_by_category
        test if the function returns '''
        mock_get_activities_from_subcategory.return_value = [None]
        result = get_activities_from_subcategory(None
        self.assertEqual(None, result)

    #Acceptance Tests for user story 2:
    def output_usage(self, args, expected_error_message):
        '''helper method to call main from cl and check error messahes '''
        sys.stdout = StringIO()
        sys.argv = args
        try:
            cl.main()
        except cl.InvalidCategoryError as e:
            output = str(e)
            self.assertEqual(output, expected_error_message)
            return output
        return None

    def test_invalid_category(self):
        '''test an invalid category for Acceptance Test 3
        '''
        args = ["cl.py", "--category", "Astronaut"]
        expected_error_message = "Usage: python3 cl.py --category <valid category>"
        output = self.output_usage(args, expected_error_message)
        self.assertIsNotNone(output)

    def test_invalid_subcategory(self):
        '''test an invalid subcategory for Acceptance Test 3
        '''
        args= ["cl.py", "--category", "Household_Activities", "--subcategory", "Astronaut"]
        expected_error_message = "Usage: python3 cl.py --category <valid category> --subcategory " \
            "<valid subcategory> \n reference python3 cl.py --category for valid subcategory inputs"
        output = self.output_usage(args, expected_error_message)
        self.assertIsNotNone(output)

if __name__ == '__main__':
    unittest.main()
