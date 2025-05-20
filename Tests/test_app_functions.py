'''Tests app.py for the functions (get top, compare, get activities) of the Flask app
file: test_app_functions.py'''
import unittest
from unittest.mock import patch, MagicMock
from app import get_subcategories_for_category
from app import  get_all_categories, app

class TestApp(unittest.TestCase):
    '''class for tests for app.py'''
    def setUp(self):
        #create a mock connection and cursor
        self.mock_conn = MagicMock()
        self.mock_cursor = self.mock_conn.cursor.return_value
        self.app = app.test_client()

    def check_missing_route(self, route, message):
        '''helper to test missing parameter routes'''
        response= self.app.get(route)
        self.assertEqual(response.status_code, 200)
        self.assertIn(message.encode(), response.data)

    #####################################################
    ###########    Get Top Activity By Age    ###########
    #####################################################
    def test_show_app_form(self):
        '''test that the app form shows up correctly'''
        response = self.app.get('/get_top?option=get_top_by_age')
        self.assertIn(b"Get Top Activity by Age", response.data)
        self.assertIn(b"Submit", response.data)

    def test_show_app_form_invalid(self):
        '''test that the app form shows up correctly'''
        response = self.app.get('/get_top')
        self.assertEqual(response.status_code, 400)
        self.assertIn(b"invalid option selected.", response.data)

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_route_top_by_age(self, mock_get_top_by_age):
        '''tests that the route to get top by age returns the right thing, given age 23'''
        mock_get_top_by_age.return_value = self.mock_conn
        response = self.app.get('/show_top_activities?age=23')
        self.assertIn(b"Top Activity Result", response.data)

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_route_top_by_age_no_age(self, mock_get_top_by_age):
        '''tests that the route to get top by age returns the right thing, given invalid age'''
        mock_get_top_by_age.return_value = self.mock_conn
        response = self.app.get('/show_top_activities?age=')
        self.assertIn(b"Age not provided", response.data)

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_route_top_by_age_invalid_age(self, mock_get_top_by_age):
        '''tests that the route to get top by age returns the right thing, given invalid age'''
        mock_get_top_by_age.return_value = self.mock_conn
        response = self.app.get('/show_top_activities?age=invalid')
        self.assertIn(b"invalid age, please use a number between 15 and 80", response.data)

    def test_missing_age(self):
        '''test for missing_age route'''
        self.check_missing_route('/get-top/',
                                "Please include an age, ex: /get-top/23" ) 

    #####################################################
    ###########        Get Cat/Sub/Act        ###########
    #####################################################
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
        self.assertEqual("These are the subcategories for Personal_Care_Activities: "\
        "['Sleeping', 'Grooming', 'Health-related_self_care', 'Personal_Activities', " \
        "'Personal_Care_Emergencies']", result)

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_get_activities_from_sub(self, mock_get_activities_from_sub):
        '''tests that the route to get activities returns the correct thing '''
        mock_get_activities_from_sub.return_value = self.mock_conn
        self.mock_cursor.fetchall.return_value = [
            ("T010101", "Sleeping"),
            ("T010102", "Sleeplessness")
        ]
        response = self.app.get('/get-activities/Personal_Care_Activities/Sleeping')

        self.assertEqual(response.status_code, 200)
        decoded = response.data.decode()
        self.assertIn("here are the activities for Sleeping in Personal_Care_Activities", decoded)
        self.assertIn("Sleeping", decoded)
        self.assertIn("Sleeplessness", decoded)

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

    def test_missing_subcategory(self):
        '''test for missing_subcategory route'''
        self.check_missing_route('/get-activities/Personal_Care_Activities/',
                                "Please include a subcategory, " \
                                "ex: /get-activities/Personal_Care_Activities/Sleeping" )

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_show_activity_form(self, mock_show_activity_form):
        '''test that the activity form shows up correctly'''
        mock_show_activity_form.return_value = self.mock_conn
        response = self.app.get('/find_activities?option=get_activities_results')
        self.assertIn(b"Find Activities", response.data)

    def test_show_activity_form_invalid(self):
        '''test that the activity form shows up correctly'''
        response = self.app.get('/find_activities')
        self.assertEqual(response.status_code, 400)

    @patch("ProductionCode.datasource.psycopg2.connect")
    @patch("ProductionCode.datasource.DataSource.get_category_list")
    @patch("ProductionCode.datasource.DataSource.get_subcategory_list")
    @patch("ProductionCode.datasource.DataSource.get_activity_list")
    def test_get_activities_results(self, mock_get_category, mock_get_subcategory,
                                    mock_get_activity, mock_get_activities_results):
        '''test that the get activities results function returns the right thing'''
        mock_get_activities_results.return_value = self.mock_conn
        mock_get_category.return_value = ["Personal_Care_Activities"]
        mock_get_subcategory.return_value = ["Sleeping"]
        mock_get_activity.return_value = ["Sleeping", "Sleeplessness"]
        response = self.app.get(
            '/show_find_activities?category=Personal_Care_Activities&subcategory=Sleeping')
        self.assertIn(b"Sleeping", response.data)
        self.assertIn(b"Sleeplessness", response.data)

    #####################################################
    ###########            Compare            ###########
    #####################################################
    def test_show_compare_form(self):
        '''test that the compare form shows up correctly'''
        response = self.app.get('/compare?option=compare_activity_for_age')
        self.assertIn(b"Compare 2022-23 to 2012-13", response.data)

    def test_show_compare_form_invalid(self):
        '''test that the compare form shows up correctly'''
        response = self.app.get('/compare')
        self.assertEqual(response.status_code, 400)

    @patch("ProductionCode.datasource.psycopg2.connect")
    @patch("ProductionCode.datasource.DataSource.compare_by_age")
    def test_compare_activity_for_age(self, mock_compare_by_age, mock_compare_activity_for_age):
        '''test that the compare activity for age function returns the right hours and message'''
        mock_compare_activity_for_age.return_value = self.mock_conn
        mock_compare_by_age.return_value = (559, 552)
        self.mock_cursor.fetchall.return_value= [(559,), (552,)]
        response = self.app.get('/show_compare?age=23&activity=Sleeping')
        self.assertIn(
            b"For people age 23 they engaged in Sleeping on average 559 hours in 2022 & 2023 " \
            b"and 552 hours in 2012 & 2013",
            response.data)

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_compare_activity_for_age_invalid(self, mock_compare_activity_for_age):
        '''test that the compare activity for age function returns the right thing'''
        mock_compare_activity_for_age.return_value = self.mock_conn
        response = self.app.get('/show_compare?age=invalid&activity=Sleeping')
        self.assertIn(b"Error: unexpected result from compare_by_age", response.data)
