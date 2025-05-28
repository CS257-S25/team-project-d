'''Tests app.py for the functions (get top, compare) of the Flask app
file: test_app_functions.py'''
import unittest
from unittest.mock import patch, MagicMock
from app import app

class TestApp(unittest.TestCase):
    '''class for tests for app.py'''
    def setUp(self):
        self.mock_conn = MagicMock()
        self.mock_cursor = self.mock_conn.cursor.return_value
        self.app = app.test_client()

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
            b"People aged 23 engaged in Sleeping on average",
            response.data)

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_compare_activity_for_age_invalid(self, mock_compare_activity_for_age):
        '''test that the compare activity for age function returns the right thing'''
        mock_compare_activity_for_age.return_value = self.mock_conn
        response = self.app.get('/show_compare?age=invalid&activity=Sleeping')
        self.assertIn(b"Error: unexpected result from compare_by_age", response.data)
