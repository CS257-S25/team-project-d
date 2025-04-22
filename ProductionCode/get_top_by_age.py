'''file: get_top_by_age.py'''
from collections import Counter
from ProductionCode.loadData import load_data


# Future: make it so that it is get_top_activity_by_demographic
# i.e gender, marital status, etc. including age
# Future: make it so it translates what the activity is
# i.e T050101 = watching tv or whatever it is and returns (watching tv, 2)
# Future: make it so it gets the top N activities for a group

#  finding the activity that has has the most hours and came up the most frequently for an age group
# python3 cl.py -- age 20 -- top
# get the top activity for people of age 20

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
        row_age = row['age']
        if int(row_age) == int(age):
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
    ''' Purpose: process the row to get the activity hours
    Args: row: the row to process
    returns: a dictionary of the activity hours'''
    #exclude non activity columns like education, gender, etc.
    activity_hours = {} #ex: T050101: 24
    for key in row:
        # check if the key is an activity (not T010101 - sleeping) and not a non-activity column
        # we remove sleeping from the list of options because everyone/s top activity is sleeping
        if key not in ["ID","TUCASEID", "metropolitan status","education",
                        "hispanic origin", "race", "age", "labor force status", 
                        "school enrollment", "school level", "sex", "number children", 
                        "full time/part time", "presence of spouse", "age youngest child", 
                        "statistical weight", "usual weekly hours worked",
                        "year", "weekly earnings", "T010101"]:
            if row[key] != "NA": # check if the value is not NA / is a number
                try:
                    row[key] = float(row[key]) #handle scientific notation
                    activity_hours[key] = int(row[key])
                except ValueError:
                    print(f"ValueError: could not convert {row[key]} to int for key {key}")
                    continue
    return activity_hours #return the activity hours dictionary

def get_top_activity_from_row(activity_hours):
    ''' Purpose: get the top activity from the row
    Args: activity_hours: the activity hours to get the top activity from
    returns: the top activity from the row'''
    if activity_hours: # check if the activity hours dictionary is not empty
        # find the activity with the most hours
        return max(activity_hours, key = activity_hours.get)
    return None

def count_top_activites(matching_rows):
    ''' Purpose: count the top activities from the matching rows
    Args: matching_rows: the matching rows to count the top activities from
    returns: a dictionary of the top activities and their counts'''
    top_activities = Counter()
    #counter to track the number of times each activity is the top activity
    for row in matching_rows:
        # process the row to get the activity hours
        activity_hours = process_row_for_activity(row)
        # get the top activity from the row
        top_activity = get_top_activity_from_row(activity_hours)
        # add the top activity to the counter
        if top_activity: # check if the top activity is not None
            top_activities[top_activity] += 1 # increment the count of the top activity
    return top_activities

def get_most_common_top_activity(age, top_n):
    ''' purpose:figures out which top activity is the most common in the dictionary
    args: age: the age group to get the most common activity for
    top_n: the number of top activities to return (should be 1)
    returns: the name of the most common top activity (future: list of top names ex top 5) '''
    # get the matching rows for the age group
    matching_rows = load_matching_rows(age)
    # check if there are any matching rows
    if not matching_rows: # if there are no matching rows, return None
        print(f"No data available for age {age}, try ages 15-85")
        return None, 0
    # count the top activities from the matching rows
    top_activities = count_top_activites(matching_rows)
    if top_activities: # check if there are any top activities
        # get the most common top activity
        # NOTE: this will return the most common activity and the count of the activity
        # if there are multiple activities with the same count, it will return the first one
        most_common_activity= top_activities.most_common(top_n)[0]
        return most_common_activity
