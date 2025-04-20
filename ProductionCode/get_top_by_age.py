'''file: get_top_by_age.py'''
import argparse
import csv
from ProductionCode.loadData import load_data
from collections import Counter

# NOTE: currently we are calculating mode but we want the median

#finding the activity that has has the most hours and came up the most frequently for an age group 
# python3 cl.py -- age 20 -- top 1 
# get the top activity for people of age 20 

''' User story: a user wants to know the most common activity for a given age group
Acceptance tests:
1) given they input a valid age group (ex: (int) 18)---> the program should return the most common activity for that age group
2) given they input an invalid age group format (ex: (str) "eighteen")---> the program should return usage statement
3) given they input an invalid age group/ out of range/no data (ex: (int) 200)---> the program should return usage statement, message that says no data available
"'''
#issue: this is just returning ('T010101', ###) for every age group for the real dataset


def get_matching_rows(age):
    ''' Purpose: get the rows that match the age group given
    Args: age: the age group to get the rows for
    returns: a list of rows/people with the age given in cl'''
    #testing print statement
    print("Getting matching rows for age group: ", age)
    matching_rows = []
    data = load_data()
    for row in data:
        # check if the age is in the row    
        if "age" in row and int(row["age"]) == int(age):
            # if it is add it to the list 
            matching_rows.append(row)
    return matching_rows

def load_matching_rows(age):
    ''' Purpose: load the matching rows for the age group given
    Args: age: the age group to get the rows for
    returns: a list of rows/people with the age given in cl'''
    ##testing print statement
    print("Getting the top activity for age group: ", age)
    matching_rows = get_matching_rows(age)
    if not matching_rows:
        print(f"No data available for age {age}")
        return None
    return matching_rows

def process_row_for_activity(row):
    #print("Processing row for activity: ", row)
    #print(" 1 got here to process row for activity: ")
    
    #exclude non activity columns like education, gender, etc. 
    activity_hours = {}
        #ex: T010101: 24
    for key, value in row.items():
            # check if the key is an activity and not a non-activity column
        if key not in ["ID","TUCASEID", "metropolitan status","education", 
                        "hispanic origin", "race", "age", "labor force status", 
                        "school enrollment", "school level", "sex", "number children", 
                        "full time/part time", "presence of spouse", "age youngest child", 
                        "statistical weight", "usual weekly hours worked", "year", "weekly earnings", "T010101"   ]:
            if value != "NA":
                try:
                    value = float(value) #handle scientific notation
                    activity_hours[key] = int(value) 
                except ValueError:
                    print(f"ValueError: could not convert {value} to int for key {key}")
                    continue
    return activity_hours
    
def get_top_activity_from_row(activity_hours):
    ''' Purpose: get the top activity from the row
    Args: activity_hours: the activity hours to get the top activity from
    returns: the top activity from the row'''
    #testing print statement
    print("getting the top activity from row")
    #print("Getting the top activity from row: ", activity_hours)
    if activity_hours:
        return max(activity_hours, key = activity_hours.get)
    return None

def count_top_activites(matching_rows):
    ''' Purpose: count the top activities from the matching rows
    Args: matching_rows: the matching rows to count the top activities from
    returns: a dictionary of the top activities and their counts'''
    #testing print statement
    print("Counting top activities from matching rows")
    #print("Counting top activities from matching rows: ", matching_rows)
    top_activities = Counter() # counter to track the number of times each activity is the top activity
    for row in matching_rows:
        activity_hours = process_row_for_activity(row)
        top_activity = get_top_activity_from_row(activity_hours)
        if top_activity:
            top_activities[top_activity] += 1
    return top_activities

def get_most_common_top_activity(age, top_n):
    ''' figures out which top activity is the most common in the dictionary
    returns: the name of the most common top activity (future: list of top names ex top 5) '''
    #testing print statement
    print("Getting the most common top activity for age group: ", age)
    matching_rows = load_matching_rows(age)
    if not matching_rows:
        print(f"No data available for age {age}")
        return None, 0
    top_activities = count_top_activites(matching_rows)
    if top_activities:
        most_common_activity, count= top_activities.most_common(top_n)[0]
        return most_common_activity, count
    else:
        print(f"No activities found for age {age}")
        return None, 0


