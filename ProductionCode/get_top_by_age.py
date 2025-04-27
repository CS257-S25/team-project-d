'''file: get_top_by_age.py'''
from collections import Counter
from ProductionCode.load_data import load_data

# Future: make it so that it is get_top_activity_by_demographic
# i.e gender, marital status, etc. including age
# Future: make it so it translates what the activity is
# i.e T050101 = watching tv or whatever it is and returns (watching tv, 2)
# Future: make it so it gets the top N activities for a group

# Purpose: finding the activity that has has the most hours and came up the most frequently for an age group
# python3 cl.py -- age 20 -- top
# get the top activity for people of age 20

def load_main_data():
    '''loads the data from main data file'''
    dataset= "Data/teamproject22-23FINAL_updatedpls.csv"
    data = load_data(dataset)
    return data

def get_matching_rows(age):
    ''' Purpose: get the rows that match the age group given
    Args: age: the age group to get the rows for
    returns: a list of rows/people with the age given in cl'''
    print("Getting matching rows for age group: ", age)
    data = load_main_data()
    matching_rows = []
    for row in data:
        row_age = row['age']
        if int(row_age) == int(age):
            matching_rows.append(row)
        if not matching_rows: # this is repeated later on, make into helper
            print(f"No data available for age {age}")
            return None
    return matching_rows

#i don't think we actually need this 
#def filter_matching_rows(age):
    ''' Purpose: filter the matching rows for the age group given
    Args: age: the age group to get the rows for
    #returns: a list of rows/people with the age given in cl'''
    print("Getting the top activity for age group: ", age)
    matching_rows = get_matching_rows(age)
    if not matching_rows:
        print(f"No data available for age {age}")
        return None
    return matching_rows

def get_excluded_columns():
    '''return a list of columns that should be excluded from processing, 
    i.e exclude identifiers, and demographics / non-activities'''
    # we remove sleeping from the list of options because everyone/s top activity is sleeping (T010101)
    # might need to consider removing T050101 which is work,main job
    excluded_columns = ["ID","TUCASEID", "metropolitan status","education",
                        "hispanic origin", "race", "age", "labor force status", 
                        "school enrollment", "school level", "sex", "number children", 
                        "full time/part time", "presence of spouse", "age youngest child", 
                        "statistical weight", "usual weekly hours worked",
                        "year", "weekly earnings", "T010101"]
    return excluded_columns

def process_row_for_activity(row):
    ''' Purpose: process the row to get the activity hours
    Args: row: the row to process
    returns: a dictionary of the activity hours'''
    excluded_columns = get_excluded_columns()
    activity_hours = {} 
    for key in row:
        if key not in excluded_columns and row[key] != "NA":
            try:
                row[key] = float(row[key]) #handle scientific notation
                activity_hours[key] = int(row[key])
            except ValueError:
                print(f"ValueError: could not convert {row[key]} to int for key {key}")
                continue
    return activity_hours 

def get_top_activity_from_row(activity_hours):
    ''' Purpose: get the top activity from the row
    Args: activity_hours: the activity hours to get the top activity from
    returns: the top activity from the row'''
    if activity_hours: 
        return max(activity_hours, key = activity_hours.get)
    return None

def count_top_activites(matching_rows):
    ''' Purpose: count the top activities from the matching rows
    Args: matching_rows: the matching rows to count the top activities from
    returns: a dictionary of the top activities and their counts'''
    top_activities = Counter()
    for row in matching_rows:
        activity_hours = process_row_for_activity(row)
        top_activity = get_top_activity_from_row(activity_hours)
        if top_activity: 
            top_activities[top_activity] += 1 
    return top_activities

def get_activity_name(activity_id):
    '''purpose: finds the name of the activity based on the ID
    arg activity_ID: the id of the activity to find
    return: the name of the activity
    '''
    categories = load_data("Data/Activities_All_Data.csv")
    for row in categories:
        if row['Activity ID'] == activity_id:
            return row['Activity Name']
    return "invalid Activity ID"
    
def get_most_common_top_activity(age):
    ''' purpose:figures out which top activity is the most common in the dictionary
    args: age: the age group to get the most common activity for
    top_n: the number of top activities to return (should be 1)
    returns: the name of the most common top activity (future: list of top names ex top 5) '''
    matching_rows = get_matching_rows(age)
    if not matching_rows:
        print(f"No data available for age {age}, try ages 15-85")
        return None
    top_activities = count_top_activites(matching_rows)
    if top_activities: 
        # NOTE: this will return the most common activity and the count of the activity
        # if there are multiple activities with the same count, it will return the first one numerically
        most_common_activity = top_activities.most_common(1)[0][0]
        activity = get_activity_name(most_common_activity)
        return most_common_activity, activity #activity, most_common_activity
