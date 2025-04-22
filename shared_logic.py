
def get_the_subcategories(sent_category):
    '''Return the list of activities from the subcategory of the category from the user's input'''
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