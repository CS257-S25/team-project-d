'''file: test_app.py'''
import unittest
from app import app

class TestApp(unittest.TestCase):
    '''class for tests for app.py'''
    def setUp(self):
        '''set up for testing'''
        app.config['TESTING']= True
        self.app = app.test_client()
    
    def test_route_home(self):
        '''tests that the home route returns the correct thing'''
        response = self.app.get('/', follow_redirects=True)
        self.assertEqual("This is the homepage: "\
            " 1) TO GET the top activity for a certain age, go to /get-top/'<'age'>'"\
            " 2) TO GET a list of all category options, go to /get-all-categories "\
            "....  NOTE: for now you can only shoose these categories: "\
            "Personal Care Activities or Household Activities"\
            " 3) TO GET a list of subcategory options from a category, "\
            "go to /get-subcategories/'<'category'>' "\
            "....  NOTE: for now you can only shoose these categories: "\
            "Personal Care Activities or Household Activities"\
            " 4) TO GET a list of activities from a subcategory, "\
            "go to /get-activities/'<'category'>'/'<'subcategory'>'", response.data )
    
    def test_route_top_by_age(self):
        '''tests that the route to get top by age returns the right thing, given age 23'''
        response = self.app.get('/get-top/23', follow_redirects=True)
        self.assertEqual(b"the top activity for people age 23 is T050101", response.data)

    def test_get_all_categories(self):
        '''tests that the route to get all categories returns the correct thing'''
        response = self.app.get('/get-all-categories', follow_redirects=True)
        self.assertEqual(b"the category options are: "
            b"['Personal Care Activities', 'Household Activities', " \
            b"'Caring For & Helping Household (HH) Members', " \
            b"'Caring For & Helping Nonhousehold (NonHH) Members', " \
            b"'Work & Work-Related Activities', 'Education', " \
            b"'Consumer Purchases', 'Professional & Personal Care Services', " \
            b"'Household Services', 'Government Services & Civic Obligations', " \
            b"'Eating and Drinking', " \
            b"'Socializing, Relaxing, and Leisure', 'Sports, Exercise, & Recreation', " \
            b"'Religious and Spiritual Activities', " \
            b"'Volunteer Activities', 'Telephone Calls', 'Traveling']", response.data)

    def test_get_subcategories_for_category(self):
        '''tets that the route to get subcatefories given a category returns the right thing '''
        response = self.app.get('/get-subcategories/Personal Care Activities',
                                follow_redirects=True)
        self.assertEqual(b"These are the subcategories: "
        b"['Sleeping', 'Grooming', 'Health-related self care', " \
        b"'Personal Activities', 'Personal Care Emergencies'] "
        b"for Personal Care Activities", response.data)

    def test_get_activities_from_sub(self):
        '''tests that the route to get activities returns the correct thing '''
        response = self.app.get('/get-activities/Personal Care Activities/Sleeping',
                                follow_redirects=True)
        self.assertEqual(b"here are the activities for Sleeping in Personal Care Activities: "
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
                                "ex: /get-subcategories/Personal Care Activities")

    def test_missing_cat_and_sub(self):
        '''test for missing_cat_and_sub route'''
        self.check_missing_route('/get-activities/',
                                "Please include a category and a subcategory, " \
                                "ex: /get-activities/Personal Care activities/Sleeping" ) 
    #def test_missing_subcategory(self):
        #'''test for missing_subcategory'''
        #response = self.app.get('/get-activities/Personal Care Activities/')
        #self.assertEqual(response.status_code, 200)
        #self.assertIn(b"please include subcategory, " \
            #b"ex: /get-activities/Personal Care activities/Sleeping", response.data)
    #def test_invalid_inputs(self):
        #response = self.app.get("/get-top/eighteen")
        #self.assertEqual(response.status_code. 200) if i add to app.py a test valid age thing
