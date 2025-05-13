'''Tests app_OG.py for all of the python code Flask app
file: test_app.py'''
import unittest
import psycopg2
from unittest.mock import patch, MagicMock

from app import get_subcategories_for_category, page_not_found, python_bug
from app import get_activities_from_sub, compare_activity_for_age, get_all_categories
from app import missing_category, missing_cat_and_sub, missing_subcategory, get_top_by_age, app

class TestApp(unittest.TestCase):
    '''class for tests for app.py'''
    def setUp(self):
        #create a mock connection and cursor
        self.mock_conn = MagicMock() 
        self.mock_cursor = self.mock_conn.cursor.return_value
        self.app = app.test_client()

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_route_home(self, mock_homepage):
        '''tests that the home route returns the correct thing'''
        mock_homepage.return_value = self.mock_conn
        self.mock_cursor.fetchall.return_value = b"This is the homepage for the time use project! "\
        b"1) TO GET the top activity for a certain age between 15 and 80, go to /get-top/'<'age'>' "\
        b"For example: http://127.0.0.1:5000/get-top/23 "\
        b"2) TO COMPARE the top activity for a certain age from 2022/2023 to 2012/2013, go to /compare/'<'age'>'/'<'activity'>' "\
        b"For example: http://127.0.0.1:5000/compare/23/Sleeping "\
        
        b"To see all options, use any of the following: "\
        b"A) TO GET a list of all category options, go to /get-all-categories "\
        b"B) TO GET a list of subcategory options from a category, "\
        b"go to /get-subcategories/'<'category'>' C) TO GET a list of activities from a subcategory, "\
        b"go to /get-activities/'<'category'>'/'<'subcategory'>'"
        
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(b"This is the homepage for the time use project! "\
        b"1) TO GET the top activity for a certain age between 15 and 80, go to /get-top/'<'age'>' "\
        b"For example: http://127.0.0.1:5000/get-top/23 "\
        b"2) TO COMPARE the top activity for a certain age from 2022/2023 to 2012/2013, go to /compare/'<'age'>'/'<'activity'>' "\
        b"For example: http://127.0.0.1:5000/compare/23/Sleeping "\
        
        b"To see all options, use any of the following: "\
        b"A) TO GET a list of all category options, go to /get-all-categories "\
        b"B) TO GET a list of subcategory options from a category, "\
        b"go to /get-subcategories/'<'category'>' C) TO GET a list of activities from a subcategory, "\
        b"go to /get-activities/'<'category'>'/'<'subcategory'>'", response.data )

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_route_top_by_age(self, mock_get_top_by_age):
        '''tests that the route to get top by age returns the right thing, given age 23'''
        mock_get_top_by_age.return_value = self.mock_conn
        self.mock_cursor.fetchall.return_value = "the top activity for people age 23 is Sleeping"
        response = get_top_by_age(23)
        self.assertEqual("the top activity for people age 23 is Sleeping", response)

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_get_all_categories(self, mock_get_all_categories):
        '''tests that the route to get all categories returns the correct thing'''
        mock_get_all_categories.return_value = self.mock_conn
        self.mock_cursor.fetchall.return_value = [
            ("T01", 'Personal_Care_Activities'), 
            ("T02", 'Household_Activities')
        ]
        response = get_all_categories()
        self.assertEqual("The category options are: ['Personal_Care_Activities', "\
        "'Household_Activities']", response)

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_get_subcategories_for_category(self, mock_get_subcategories_for_category):
        '''tests that the route to get subcategories given a category returns the right thing '''
        mock_get_subcategories_for_category.return_value = self.mock_conn
        self.mock_cursor.fetchall.return_value = [
            ('T0101', 'Sleeping'),
            ('T0102', 'Grooming'),
            ('T0103', 'Health-related_self_care'),
            ('T0104', 'Personal_Activities'),
            ('T0105', 'Personal_Care_Emergencies')
        ]
        result = get_subcategories_for_category('Personal_Care_Activities')
        self.assertEqual("These are the subcategories for Personal_Care_Activities : "\
        "['Sleeping', 'Grooming', 'Health-related_self_care', 'Personal_Activities', 'Personal_Care_Emergencies']", result)

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_get_activities_from_sub(self, mock_get_activities_from_sub):
        '''tests that the route to get activities returns the correct thing '''
        mock_get_activities_from_sub.return_value = self.mock_conn
        self.mock_cursor.fetchall.return_value = [
            ("T010101", "Sleeping"),
            ("T010102", "Sleeplessness")
        ]
        #result = get_activities_from_sub("Personal_Care_Activities", "Sleeping")
        #self.assertEqual()
        #self.assertEqual(result.status_code, 200)
        #self.assertIn("Here are the activities for Sleeping in Personal_Care_Activities", result)
        response = self.app.get('/get-activities/Personal_Care_Activities/Sleeping')

        self.assertEqual(response.status_code, 200)
        decoded = response.data.decode()
        self.assertIn("here are the activities for Sleeping in Personal_Care_Activities", decoded)
        self.assertIn("Sleeping", decoded)
        self.assertIn("Sleeplessness", decoded)
        
    def assert_404(self, route):
        '''test to make sure error returns correct thing'''
        response = self.app.get(route)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"404 Not Found: The requested URL was not found on the server. " \
        b"If you entered the URL manually please check your spelling and try again. " \
        b"... refer to homepage (/) for options", response.data)

    def check_missing_route(self, route, message):
        '''helper to test missing parameter routes'''
        response= self.app.get(route)
        self.assertEqual(response.status_code, 200)
        self.assertIn(message.encode(), response.data)

    def test_missing_age(self):
        '''test for missing_age route'''
        self.check_missing_route('/get-top/',
                                "Please include an age, ex: /get-top/23" ) 

    def test_missing_category(self):
        '''test for missing_category route'''
        self.check_missing_route('/get-subcategories/',
                                "Please include a category, " \
                                "ex: /get-subcategories/Personal_Care_Activities")

    def test_missing_cat_and_sub(self):
        '''test for missing_cat_and_sub route'''
        self.check_missing_route('/get-activities/',
                                "Please include a category and a subcategory, " \
                                "ex: /get-activities/Personal_Care_Activities/Sleeping" ) 
    #def test_missing_subcategory(self):
        #'''test for missing_subcategory'''
        #response = self.app.get('/get-activities/Personal_Care_Activities/')
        #self.assertEqual(response.status_code, 200)
        #self.assertIn(b"please include subcategory, " \
            #b"ex: /get-activities/Personal_Care_Activities/Sleeping", response.data)
    #def test_invalid_inputs(self):
        #response = self.app.get("/get-top/eighteen")
        #self.assertEqual(response.status_code. 200) if i add to app.py a test valid age thing
