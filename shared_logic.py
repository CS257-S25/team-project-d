
def get_the_subcategories(sent_category):
    '''Return the list of activities from the subcategory of the category from the user's input
    Args: sent_category: the category to get the subcategories for
    Returns: a list of subcategories in the category'''
    list_of_subcategories = []
    if sent_category:
        category = sent_category
        print("Recognizes that there is only one argument")
        # Call the function to get subcategories (assume it's implemented elsewhere)
        #data = load_subcategory_data()
        # Filter activities based on the category (example logic)
        from ProductionCode.getActivtyByCategory import get_list_of_subcategories

        list_of_subcategories= get_list_of_subcategories(category)

    return list_of_subcategories