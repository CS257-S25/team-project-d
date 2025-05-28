'''
THIS IS THE FLASK APP FOR THE SQL DATABASE
file: app.py
'''
from flask import Flask, request, render_template
from ProductionCode.datasource import DataSource

app = Flask(__name__)

@app.route('/')
def homepage():
    '''Purpose: Homepage provides instructions for what URL to go to see the data you choose'''
    return render_template('index.html', title = "Homepage")

@app.route('/about',  methods=['GET'])
def about_page():
    '''purpose: provides information about our data'''
    return render_template('about.html', title= 'About The Hobby Clock')

#####################################################
###########    Get Top Activity By Age    ###########
#####################################################
@app.route('/get_top',  methods=['GET'] )
def show_age_form():
    '''display form to select an age
    checks if they selected the get_top_by_age option and renders a template for age input
    else return an error message'''
    option =request.args.get('option')
    if option == 'get_top_by_age':
        return render_template(
            "age_form.html", 
            title = "Get Top Activity by Age"
        )
    return render_template('404.html', title = "ERROR 404: PAGE NOT FOUND")

@app.route('/show_top_activities', methods = ['GET'])
def get_top_by_age():
    ''' returns the information for the top activity for an age group'''
    data = DataSource()
    age = request.args.get('age')
    if not age:
        return render_template('404.html', title = "ERROR 404: PAGE NOT FOUND")
    top_ids = data.get_top_by_age(age)
    if "invalid age" in top_ids:
        return render_template('404.html', title = "ERROR 404: PAGE NOT FOUND",
            message = "invalid age, try again with an age from 15 to 80")

    top_activities, times = process_top(top_ids)
    return render_template("get_top.html",title= "Top Activity Result", age=age,
                           activities=top_activities, times= times)

def process_top(top_ids):
    '''returns activity names and times as two lists from top tuples'''
    top_activities = []
    times = []
    for activity, hrs in top_ids:
        hours= int(hrs)
        top_activities.append(activity)
        times.append(hours)
    return top_activities, times

#####################################################
###########        Get Cat/Sub/Act        ###########
#####################################################
@app.route('/get-all-categories')
def get_all_categories():
    '''returns a list of category options'''
    data = DataSource()
    data_for_get_category = data.get_category_list()
    return "The category options are: " + str(data_for_get_category)

@app.route('/get-subcategories/<category>')
def get_subcategories_for_category(category):
    ''' param: category, the category you want more info about(subcategories for)
    returns a list of subcategories for a given category'''
    data = DataSource()
    sub_list = data.get_subcategory_list(category)
    return f"These are the subcategories for {category}: {sub_list}"

@app.route('/get-activities/<category>/<subcategory>')
def get_activities_from_sub(category, subcategory):
    ''' param: category, the category you want to look at 
    param: subcategory, the subcategory you want more info about (activities for)
    returns a list of activities from a subcategory'''
    data = DataSource()
    activities = data.get_activity_list(subcategory)
    return f"here are the activities for {subcategory} in {category}: {activities}"

@app.route('/find_activities', methods = ['GET'])
def show_activity_form():
    '''display form '''
    option =request.args.get('option')
    if option == 'get_activities_results':
        data = DataSource()
        categories= data.get_category_list()
        return render_template("activity_form.html", title = "Find Activities",
                               categories=categories)
    return render_template('404.html', title = "ERROR 404: PAGE NOT FOUND")

@app.route('/show_find_activities', methods = ['GET'])
def get_activities_results():
    '''display form to find activities'''
    category= request.args.get('category')
    subcategory = request.args.get('subcategory')
    data = DataSource()
    categories = data.get_category_list()
    subcategories = data.get_subcategory_list(category)
    activities = data.get_activity_list(subcategory)
    return render_template('activity_form.html', categories=categories,
                            subcategories= subcategories, selected_category= category,
                            selected_subcategory=subcategory, activities=activities)

#####################################################
###########            Compare            ###########
#####################################################
@app.route('/compare')
def show_compare_form():
    '''display form to select an age, activity, and year to compare
    checks if they selected the compare_activity_for_age option and renders a template 
    else return an error message'''
    option =request.args.get('option')
    if option == 'compare_activity_for_age':
        return render_template("compare_form.html", title = "Compare 2022-23 to 2012-13")
    return render_template('404.html', title = "ERROR 404: PAGE NOT FOUND")

@app.route('/show_compare', methods = ['GET'])
def compare_activity_for_age():
    '''param: age, the age you want to compare the activity for
    param: activity, the activity you want to compare
    returns render template that gives the comparison for an age group'''
    age= request.args.get('age')
    activity= request.args.get('activity')
    data = DataSource()
    hours = data.compare_by_age(age, activity)
    if not isinstance(hours, (tuple, list)) or len(hours) != 2:
        return render_template('404.html', title = "ERROR 404: PAGE NOT FOUND",
            message = "make sure to input a valid age from 15 to 80 and\
            a valid activity name such as 'Playing baseball' or 'Laundry'")
    return render_template('compare_activity.html', age=age, activity=activity,
                           hours_2223 = hours[0], hours_1213=hours[1])

#####################################################
###########             Errors            ###########
#####################################################
@app.errorhandler(404)
def page_not_found(e):
    '''returns error message if the page wasn't found'''
    print(e)
    return render_template('404.html', title = "ERROR 404: PAGE NOT FOUND")

@app.errorhandler(500)
def python_bug(e):
    ''' returns a message to let you know if there's an internal error/bug'''
    print(e)
    return render_template ('500.html')

if __name__ == '__main__':
    app.run(debug=True, port=5137)
