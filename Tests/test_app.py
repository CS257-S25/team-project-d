'''Tests app_OG.py for all of the python code Flask app
file: test_app.py'''
import unittest
import psycopg2
from app import app

from app import get_subcategories_for_category, page_not_found, python_bug
from app import get_activities_from_sub, compare_activity_for_age, get_all_categories
from app import missing_category, missing_cat_and_sub, missing_subcategory, get_top_by_age

class TestApp(unittest.TestCase):
    '''class for tests for app.py'''
    def setUp(self):
        '''set up for testing'''
        app.config['TESTING']= True
        self.app = app.test_client()

    def test_route_home(self):
        '''tests that the home route returns the correct thing'''
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual(b"This is the homepage: "\
            b" 1) TO GET the top activity for a certain age, go to /get-top/'<'age'>'"\
            b" 2) TO GET a list of all category options, go to /get-all-categories "\
            b" 3) TO GET a list of subcategory options from a category, "\
            b"go to /get-subcategories/'<'category'>' "\
            b" 4) TO GET a list of activities from a subcategory, "\
            b"go to /get-activities/'<'category'>'/'<'subcategory'>'", response.data )

    def test_route_top_by_age(self):
        '''tests that the route to get top by age returns the right thing, given age 23'''
        response = get_top_by_age(23)
        self.assertEqual("the top activity for people age 23 is Sleeping", response)

    def test_get_all_categories(self):
        '''tests that the route to get all categories returns the correct thing'''
        response = get_all_categories()
        self.assertEqual("The category options are: [('T01', 'Personal_Care_Activities'), ('T02', 'Household_Activities'), ('T03', 'Caring_For_&_Helping_Household_(HH)_Members'), ('T04', 'Caring_For_&_Helping_Nonhousehold_(NonHH)_Members'), ('T05', 'Work_&_Work-Related_Activities'), ('T06', 'Education'), ('T07', 'Consumer_Purchases'), ('T08', 'Professional_&_Personal_Care_Services'), ('T09', 'Household_Services'), ('T10', 'Government_Services_&_Civic_Obligations'), ('T11', 'Eating_and_Drinking'), ('T12', 'Socializing_Relaxing_and_Leisure'), ('T13', 'Sports_Exercise_&_Recreation'), ('T14', 'Religious_and_Spiritual_Activities'), ('T15', 'Volunteer_Activities'), ('T16', 'Telephone_Calls'), ('T18', 'Traveling')]", response)

    def test_get_subcategories_for_category(self):
        '''tests that the route to get subcategories given a category returns the right thing '''
        result = get_subcategories_for_category('Personal_Care_Activities')
        self.assertEqual("These are the subcategories for Personal_Care_Activities : [('T0102', 'Grooming'), ('T0103', 'Health-related_self_care'), ('T0104', 'Personal_Activities'), ('T0105', 'Personal_Care_Emergencies')]", result)

    #
    def test_get_activities_from_sub(self):
        '''tests that the route to get activities returns the correct thing '''
        result = get_activities_from_sub('Personal_Care_Activities', 'Sleeping')
        self.assertEqual("here are the activities for Sleeping in Personal_Care_Activities: not found ", result)

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
