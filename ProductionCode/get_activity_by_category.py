'''file: get_activity_by_category'''
from ProductionCode.load_data import load_data

#Future: including more categories and subcategories to work with
#Future: organize loading functions into a separate file

#Finding the general types of activities of a certain category
#Usage: python3 cl.py --category <valid category>
#       python3 cl.py --category <"Personal Care Activities" or "Household Activities">
#Returns the subcategories of the category given

#Finding the activities of a certain valid subcategory
#Usage: python3 cl.py --category <valid category> --subcategory <valid subcategory>
#       python3 cl.py --category <"Personal Care Activities"> --subcategory <"Sleeping">
#Returns a list of activities of the subcategory given

def load_category_data():
    '''Purpose: loads the general categories data from the file
    Args: None
    Returns: a list of dicitionaries containing the categories data from the file'''
    return load_data("Data/Categories_Data.csv")

def load_subcategory_data():
    '''Purpose: loads the subcategories data from the file
    Args: None
    Returns: a list of dicitionaries containing the subcategories data from the file'''
    return load_data("Data/Subcategories_Data.csv")

def load_activity_data():
    '''Purpose: loads the activities data from the file
    Args: None
    Returns: a list of dicitionaries containing the activities data from the file'''
    return load_data("Data/Activities_Data.csv")

def find_id_by_name(data_loader, name_key, target_name):
    '''helper function to reduce repeated code to fin an Activity_ID by name
    params: data_loader, the data you want to load
    param: name_key, 
    paramL target_name, '''
    data = data_loader
    key = name_key[0:-5] + '_ID'
    for row in data:
        if row[name_key] == target_name:
            print(row[key])
            return row[key]
    return None

def filter_by_prefix(data_loader, id_prefix, name_key, prefix_length=None):
    '''helper function to filter &return names whose Activity_ID matches a prefix 
    param: data_loader, a function that loads and returns activity data
    param: id_prefix, the prefix to match at the beginning of each Activity_ID 
    param: name_key, the key name in dict with the calue you want 
    param: prefix_length: how many char of Activity_ID to compare
    returns a list of names whose Activity_ID match the given prefix'''
    data = data_loader()
    results = []
    key = name_key + '_ID'
    for row in data:
        if prefix_length:
            prefix = row[key][:prefix_length]
        else:
            prefix = row[key]
        if prefix == id_prefix:
            results.append(row[name_key])
    return results

def get_category_from_data(category):
    '''Purpose: gets the category ID from the selected category
    Args: category: the category to get the ID for
    Returns: the ID of the category'''
    category_id = find_id_by_name(load_category_data(), 'Category', category)
    if not category_id:
        print("Usage: python3 cl.py --category <valid category>")
    return category_id

def get_subcategory_from_data(subcategory):
    '''Purpose: gets the ID of the selected subcategory
    Args: subcategory: the subcategory to get the ID for
    Returns: the ID of the subcategory'''
    subcategory_id = find_id_by_name(load_subcategory_data, 'Subcategory_Name', subcategory)
    if not subcategory_id:
        print("Usage: python3 cl.py --category <valid category> --subcategory " \
        "<valid subcategory> \n reference python3 cl.py --category for valid subcategory inputs")
    return subcategory_id

def get_list_of_subcategories(category):
    '''Purpose: gets the list of subcategories from the selected category
    Args: category: the category to get the subcategories for
    Returns: a list of subcategories in the category'''
    category_id = get_category_from_data(category)
    if category_id:
        return filter_by_prefix(load_subcategory_data, category_id,
                                'Activity_Name', prefix_length = len(category_id))
    return []

def get_activities_from_subcategory(subcategory):
    '''Purpose: gets the list of activities from the selected subcategory
    Args: category: the category to get the activities for
          subcategory: the subcategory to get the activities for
    Returns: a list of activities in the subcategory'''
    subcategory_id = get_subcategory_from_data(subcategory)
    activities = filter_by_prefix(load_activity_data, subcategory_id,
                                  'Activity Name', prefix_length=5)
    return activities
