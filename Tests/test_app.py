'''Tests app.py for the homepage and error pages of the Flask app
file: test_app.py'''
import unittest
from unittest.mock import patch, MagicMock
from app import app

class TestApp(unittest.TestCase):
    '''class for tests for app.py'''
    def setUp(self):
        #create a mock connection and cursor
        self.mock_conn = MagicMock()
        self.mock_cursor = self.mock_conn.cursor.return_value
        self.app = app.test_client()

    @patch("ProductionCode.datasource.psycopg2.connect")
    def test_route_home_template(self, mock_homepage):
        '''tests that the homeroute uses the correct template'''
        mock_homepage.return_value = self.mock_conn
        response = self.app.get('/')
        self.assertIn(
            b'Welcome to the Homepage for Time Use Survey!', response.data)

    #####################################################
    ###########             Others            ###########
    #####################################################
    #TO DO: update this
    def test_page_not_found(self):
        '''test to make sure error returns correct thing'''
        response = self.app.get('/invalid_route')
        self.assertEqual(response.data, b"404 Not Found: The requested URL was not found on the " \
        b"server. If you entered the URL manually please check your spelling and try again.")

    def assert_404(self, route):
        '''test to make sure error returns correct thing'''
        response = self.app.get(route)
        self.assertEqual(response.status_code, 404)
        self.assertIn(b"404 Not Found: The requested URL was not found on the server. " \
        b"If you entered the URL manually please check your spelling and try again. " \
        b"... refer to homepage (/) for options", response.data)

