'''
THIS IS THE FLASK APP FOR THE SQL DATABASE
file: app.py
'''
from flask import Flask, request
from ProductionCode.datasource import DataSource
app = Flask(__name__)

test = DataSource()

def directions_message():
    '''message that is printed on homepage and error pages to tell the user what to do'''
    base_url = request.host_url.rstrip('/')
    message = " 1) TO GET the top activity for a certain age between 15 and 80,"\
        " go to /get-top/'<'age'>'<br>"\
        f" For example: {base_url}/get-top/23 <br>"\
        " 2) TO COMPARE the top activity for a certain age from 2022/2023 to 2012/2013," \
        " go to /compare/'<'age'>'/'<'activity'>'<br>"\
        f" For example: {base_url}/compare/23/Sleeping <br> <br>"\
        " To see all options, use any of the following: <br>" \
        " A) TO GET a list of all category options, go to /get-all-categories <br>"\
        " B) TO GET a list of subcategory options from a category,<br>"\
        " go to /get-subcategories/'<'category'>' "\
        " C) TO GET a list of activities from a subcategory,<br>"\
        " go to /get-activities/'<'category'>'/'<'subcategory'>'" 
    return message

@app.route('/')
def homepage():
    '''Purpose: Homepage provides instructions for what URL to go to see the data you choose'''
    return "This is the homepage for the time use project! <br>" + directions_message()

@app.route('/get-top/<age>')
def get_top_by_age(age):
    '''param: age, the age you want to see the top category for
    returns a string that gives the information for the top activity for an age group'''
    top = test.get_top_by_age(age)
    if "invalid age" in top:
        return top
    return "the top activity for people age " + age + " is " + str(top)

@app.route('/get-top/')
def missing_age():
    '''returns a message if you forgot to add a /age'''
    return "Please include an age, ex: /get-top/23", 200

@app.route('/get-all-categories')
def get_all_categories():
    '''returns a list of category options'''
    data_for_get_category = test.get_category_list()
    return "The category options are: " + str(data_for_get_category)

@app.route('/get-subcategories/<category>')
def get_subcategories_for_category(category):
    ''' param: category, the category you want more info about(subcategories for)
    returns a list of subcategories for a given category'''
    sub_list = test.get_subcategory_list(category)
    return f"These are the subcategories for {category} : {sub_list}"

@app.route('/get-subcategories/')
def missing_category():
    '''returns a message if you forgot to add a /category'''
    return "Please include a category, ex: /get-subcategories/Personal_Care_Activities", 200

@app.route('/get-activities/<category>/<subcategory>')
def get_activities_from_sub(category, subcategory):
    ''' param: category, the category you want to look at 
    param: subcategory, the subcategory you want more info about (activities for)
    returns a list of activities from a subcategory'''
    activities = test.get_activity_list(subcategory)
    return f"here are the activities for {subcategory} in {category}: {activities}"

@app.route('/get-activities/')
def missing_cat_and_sub():
    '''returns a message if you forgot to add a category and subcategory'''
    return "Please include a category and a subcategory, " \
        "ex: /get-activities/Personal_Care_Activities/Sleeping"

@app.route('/get-activities/<category>/')
def missing_subcategory(_category):
    '''returns a message if you forgot to add a subcategory'''
    return "Please include a subcategory, " \
        "ex: /get-activities/Personal_Care_Activities/Sleeping"

@app.route('/compare/<age>/<activity>')
def compare_activity_for_age(age, activity):
    '''param: age, the age you want to compare the activity for
    param: activity, the activity you want to compare
    returns a string that gives the comparison for an age group'''
    hours = test.compare_by_age(age, activity)
    return "For people age " + age + " they engaged in " + activity + " on average " + \
        + str(hours[0]) + " hours in 2022 & 2023 and " + str(hours[1]) + " hours in 2012 & 2013"

@app.errorhandler(404)
def page_not_found(e):
    '''returns error message if the page wasn't found'''
    return f"{e} <br>" + directions_message()

@app.errorhandler(500)
def python_bug(e):
    ''' returns a message to let you know if there's an internal error/bug'''
    return f"{e} <br>"  + directions_message()

if __name__ == '__main__':
    app.run()
