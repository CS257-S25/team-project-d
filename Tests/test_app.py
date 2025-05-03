'''Tests app_OG.py for all of the python code Flask app
file: test_app.py'''
import unittest
from app_OG import app

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
        response = self.app.get('/get-top/23', follow_redirects=True)
        self.assertEqual(b"the top activity for people age 23 is T050101", response.data)

    def test_get_all_categories(self):
        '''tests that the route to get all categories returns the correct thing'''
        response = self.app.get('/get-all-categories', follow_redirects=True)
        self.assertEqual(b"The category options are: " \
            b"['Personal_Care_Activities', 'Household_Activities', " \
            b"'Caring_For_&_Helping_Household_(HH)_Members', " \
            b"'Caring_For_&_Helping_Nonhousehold_(NonHH)_Members', " \
            b"'Work_&_Work-Related_Activities', 'Education', " \
            b"'Consumer_Purchases', 'Professional_&_Personal_Care_Services', " \
            b"'Household_Services', 'Government_Services_&_Civic_Obligations', " \
            b"'Eating_and_Drinking', " \
            b"'Socializing_Relaxing_and_Leisure', 'Sports_Exercise_&_Recreation', " \
            b"'Religious_and_Spiritual_Activities', " \
            b"'Volunteer_Activities', 'Telephone_Calls', 'Traveling']", response.data)

    def test_get_subcategories_for_category(self):
        '''tets that the route to get subcatefories given a category returns the right thing '''
        response = self.app.get('/get-subcategories/Personal_Care_Activities',
                                follow_redirects=True)
        self.assertEqual(b"These are the subcategories: "
        b"['Sleeping', 'Grooming', 'Health-related_self_care', " \
        b"'Personal_Activities', 'Personal_Care_Emergencies'] "
        b"for Personal_Care_Activities", response.data)

    def test_get_activities_from_sub(self):
        '''tests that the route to get activities returns the correct thing '''
        response = self.app.get('/get-activities/Personal_Care_Activities/Sleeping',
                                follow_redirects=True)
        self.assertEqual(b"here are the activities for Sleeping in Personal_Care_Activities: "
        b"['Sleeping', 'Sleeplessness']", response.data)

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
