###### delete this file

import argparse
import csv
from ProductionCode.loadData import load_data
from collections import Counter

def get_matching_rows(age):
    # Your existing logic to return rows where the age matches
    data= load_data()
    matching_rows = [row for row in data if row['age'] == age]
    return matching_rows

def process_row_for_activity(row):
    # Extract hours for all activities and find the one with the highest hours
    activity_hours = {key: int(row[key]) for key in row if key.startswith('T')}
    return get_top_activity_from_row(activity_hours)

def get_top_activity_from_row(activity_hours):
    # Return the activity with the maximum hours
    return max(activity_hours, key=activity_hours.get)

def count_top_activities(matching_rows):
    # Find top activities for each row
    top_activities = [process_row_for_activity(row) for row in matching_rows]
    
    # Count occurrences of each activity
    from collections import Counter
    activity_counts = Counter(top_activities)
    return activity_counts

def get_most_common_top_activity(age, top_n=1):
    matching_rows = get_matching_rows(age)
    if not matching_rows:
        print(f"No data available for age {age}")
        return None

    activity_counts = count_top_activities(matching_rows)
    most_common_activities = activity_counts.most_common(top_n)
    
    # Return top N most common activities
    result = [(activity, count) for activity, count in most_common_activities]
    return result

def get_most_common_top_activity(age, top_n=1):
    matching_rows = get_matching_rows(age)
    if not matching_rows:
        print(f"No data available for age {age}")
        return None

    activity_counts = count_top_activities(matching_rows)
    most_common_activities = activity_counts.most_common(top_n)
    
    # Return top N most common activities
    result = [(activity, count) for activity, count in most_common_activities]
    return result
