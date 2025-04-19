import argparse
import csv
from loadData import load_data
from cl import args
from collections import Counter

# python3 cl.py -- age 20 -- top 1 
# get the top activity for people of age 20 

''' User story: a user wants to know the most common activity for a given age group
Acceptance tests:
1) given they input a valid age group (ex: (int) 18)---> the program should return the most common activity for that age group
2) given they input an invalid age group format (ex: (str) "eighteen")---> the program should return usage statement
3) given they input an invalid age group/ out of range/no data (ex: (int) 200)---> the program should return usage statement, message that says no data available
"'''

def get_matching_rows():
    ''''return: a list of rows/people with the age given in cl'''
    matching_rows = []
    data = load_data()
    for row in data:
        # check if the age is in the row    
        if int(row["age"] == int(args.age)):
            # if it is add it to the list 
            matching_rows.append(row)
    return matching_rows
def get_top_activity():
    ''''checks each row in the list of matching rows for the activity with the most hours
    returns: the name of the activity with the most hours for each row 
    and puts it in a list or something
    then we will see how many times each activity is in the list so we can see which one is the most'''
    matching_rows = get_matching_rows()
    top_activities = []
    for row in matching_rows:
        #exclude non activity columns like education, gender, etc. 
        activity_hours = {}
        for key, value in row.items():
            # check if the key is an activity and not a non-activity column
            if key not in ["ID","TUCASEID", "metropolitan status","education", 
                           "hispanic origin", "race", "age", "labor force status", 
                            "school enrollment", "school level", "sex", "number children", 
                            "full time/part time", "presence of spouse", "age youngest child", 
                            "statistical weight", "usual weekly hours worked", "year"   ]:
                activity_hours[key] = int(value)
        # get the activity with the most hours
        if activity_hours:
            top_activity = max(activity_hours, key = activity_hours.get)
            top_activities.append(top_activity)
    return top_activities
def get_most_common_top_activity():
    ''' figures out which top activity is the most common in the list
    returns: the name of the most common top activity (future: list of top names ex top 5) '''
    top_activities = get_top_activity()

    #count how many times each activity appears as the top activity
    activity_counts = Counter(top_activities)
    most_common_top_activity = activity_counts.most_common(args.top)
    return most_common_top_activity

