'''This is the Test file to use'''
import os
import sys
import unittest
from io import StringIO
from unittest.mock import patch
#from unittest.mock import mock_open
import cl
#from ProductionCode.get_top_by_age import get_matching_rows, load_matching_rows
#from ProductionCode.get_top_by_age import process_row_for_activity, get_top_activity_from_row
#from ProductionCode.get_top_by_age import count_top_activites, get_most_common_top_activity
from ProductionCode.get_activity_by_category import load_category_data, load_subcategory_data
from ProductionCode.get_activity_by_category import load_activity_data, get_category_from_data
from ProductionCode.get_activity_by_category import get_list_of_subcategories, get_subcategory_from_data
from ProductionCode.get_activity_by_category import get_activities_from_subcategory
from shared_logic import get_the_subcategories
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

#def mock_file_selector(file, *args, **kwargs):
    #if "Categories_Data_test.csv" in file:
        #mock_categories = (
            #"Activity_ID,Category\n"
            #"T02,Household Activities\n"
        #)
        #return mock_open(read_data=mock_categories).return_value
    #elif "SubCategories_data.csv" in file:
        #mock_subcategories = (
            #"Activity_ID,Activity_Name\n"
            #"T0101,Sleeping\n"
            #"T0201,Housework\n"
            #"T0202,Food & Drink Preparation/Presentation/Clean-Up\n"
        #)
        #return mock_open(read_data=mock_subcategories).return_value
    #else:
        #raise FileNotFoundError(f"Unexpected file path: {file}")

class TestCL(unittest.TestCase):
    '''Test class for the command line interface (CLI) for the project.'''
    def setUp(self):
        self.category_data = load_category_data()
        self.subcategory_data = load_subcategory_data()
        self.activity_data = load_activity_data()
   
    
    ##### TESTS FOR USER STORY 2: get_activty_by_category --- getting the activities by category #####

    @patch("ProductionCode.get_activity_by_category.get_category_from_data")
    def test_get_category_from_data(self, mock_get_category_from_data):
        '''tests the get_category_from_data function and Acceptance Test 1
        test if the function returns T01 for the category Personal Care Activities'''
        mock_get_category_from_data.return_value = "T01" #might not be needed
        self.assertEqual('T01', get_category_from_data('Personal Care Activities'))

    @patch("ProductionCode.get_activity_by_category.load_subcategory_data")
    #use same structure astets-Get_list _of_activities
    def test_get_list_of_subcategories(self, mock_load_sub_data):
        '''tests the get_list_of_subcategories function and Acceptance Test 2
        test if the function returns ['Interior cleaning', 'Laundry'] given the cateogry ID'''
        mock_load_sub_data.return_value = [
            #idk what this should be 
        ]
        result =get_list_of_subcategories("T02")
        self.assertEqual(['Interior cleaning', 'Laundry'], result)

    @patch("shared_logic.get_the_subcategories")
    def test_get_the_subcategories(self, mock_get_the_subcategories):
        '''tests get_the_subcategories from shared_logic.py
        test if the function returns ['Sleeping', 'Grooming'] given the category name'''
        mock_get_the_subcategories.return_value = ['Sleeping', 'Grooming']
        result = get_the_subcategories("Personal Care Activities")
        self.assertEqual(['Sleeping', 'Grooming','Health-related self care','Personal Activities','Personal Care Emergencies'], result)

    @patch("ProductionCode.get_activity_by_category.get_activities_from_subcategory")
    def test_get_activities_from_subcategory(self, mock_get_activities_from_subcategory):
        '''tests get_activity_from_subcategory from get_activity_by_category
        test if the function returns ['Interior cleaning', 'Laundry'] given the subcategory name'''
        mock_get_activities_from_subcategory.return_value = ['Interior cleaning', 'Laundry']
        result = get_activities_from_subcategory('Household Activities','Housework')
        self.assertEqual(['Interior cleaning', 'Laundry'], result) 

    def output_usage_for_category(self):
        '''helper method to call main from cl
        returns: usage message (str)
        simplifies repeated calls to main'''
        sys.stdout = StringIO()
        cl.main()
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, "Usage: python3 cl.py --category <'Personal Care Activities' or" \
            " 'Household Activities'>")

    def test_invalid_category(self):
        '''test an invalid category for Acceptance Test 3
        '''
        sys.argv = ["cl.py", "--category", "Astronaut"]
        self.output_usage_for_category()

    def output_usage_for_subcategory(self):
        '''helper method to call main from cl
        returns: usage message (str)
        simplifies repeated calls to main'''
        sys.stdout = StringIO()
        cl.main()
        output = sys.stdout.getvalue().strip()
        self.assertEqual(output, b"Usage: python3 cl.py --category <valid category> --subcategory " \
            b"<valid subcategory> \n reference python3 cl.py --category for valid subcategory inputs")

    def test_invalid_subcategory(self):
        '''test an invalid subcategory for Acceptance Test 3
        '''
        sys.argv = ["cl.py", "--category", "Household Activities", "--subcategory", "Astronaut"]
        self.output_usage_for_subcategory()

if __name__ == '__main__':
    unittest.main()
        