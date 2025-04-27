'''
file: app.py
'''
from flask import Flask, request
from ProductionCode.get_top_by_age import get_most_common_top_activity
from ProductionCode.get_activity_by_category import load_category_data
from ProductionCode.get_activity_by_category import get_category_from_data
from ProductionCode.get_activity_by_category import get_list_of_subcategories
from ProductionCode.get_activity_by_category import get_activities_from_subcategory
app = Flask(__name__)

@app.route('/')
def homepage():
    '''Purpose: Homepage provides instructions for what URL to go to see the data you choose'''
    return "This is the homepage: "\
    " 1) TO GET the top activity for a certain age, go to /get-top/'<'age'>'"\
    " 2) TO GET a list of all category options, go to /get-all-categories "\
    " 3) TO GET a list of subcategory options from a category, "\
    "go to /get-subcategories/'<'category'>' "\
    " 4) TO GET a list of activities from a subcategory, "\
    "go to /get-activities/'<'category'>'/'<'subcategory'>'"

@app.route('/get-top/<age>')
def get_top_by_age(age):
    '''param: age, the age you want to see the top category for
    returns a string that gives the information for the top activity for an age group'''
    top= get_most_common_top_activity(age)[0]
    return "the top activity for people age " + str(age) + " is " + str(top)

@app.route('/get-top/')
def missing_age():
    '''returns a message if you forgot to add a /age'''
    return "Please include an age, ex: /get-top/23", 200

@app.route('/get-all-categories')
def get_all_categories():
    '''returns a list of category options'''
    data_for_get_category = load_category_data()
    category_list = []
    for row in data_for_get_category:
        category_list.append(row['Category'])
    return "The category options are: " + str(category_list)

@app.route('/get-subcategories/<category>')
def get_subcategories_for_category(category):
    ''' param: category, the category you want more info about(subcategories for)
    returns a list of subcategories for a given category'''
    sub_list = get_list_of_subcategories(category)
    return f"These are the subcategories: {sub_list} for {category}"

@app.route('/get-subcategories/')
def missing_category():
    '''returns a message if you forgot to add a /category'''
    return "Please include a category, ex: /get-subcategories/Personal_Care_Activities", 200

@app.route('/get-activities/<category>/<subcategory>')
def get_activities_from_sub(category, subcategory):
    ''' param: category, the category you want to look at 
    param: subcategory, the subcategory you want more info about (activities for)
    returns a list of activities from a subcategory'''
    activities = get_activities_from_subcategory(subcategory)
    return f"here are the activities for {subcategory} in {category}: {activities}"

@app.route('/get-activities/')
def missing_cat_and_sub():
    '''returns a message if you forgot to add a category and subcategory'''
    return "Please include a category and a subcategory, " \
        "ex: /get-activities/Personal_Care_Activities/Sleeping"

@app.route('/get-activities/<category>/')
def missing_subcategory(category):
    '''returns a message if you forgot to add a subcategory'''
    return "Please include a subcategory, " \
        "ex: /get-activities/Personal_Care_Activities/Sleeping"

@app.errorhandler(404)
def page_not_found(e):
    '''returns error message if the page wasn't found'''
    base_url = request.host_url.rstrip('/')
    return f"{e} ... refer to homepage ({base_url}) for options "

@app.errorhandler(500)
def python_bug(e):
    ''' returns a message to let you know if there's an internal error/bug'''
    base_url = request.host_url.rstrip('/')
    return f"{e} Further information on correct inputs can be found on the homepage at: {base_url}"

if __name__ == '__main__':
    app.run()
