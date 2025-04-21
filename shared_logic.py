def get_list_of_activities(args, load_subcategory_data):
    '''Return the list of activities from the subcategory of the category from the user's input'''
    list_of_activities = []
    if args.category:
        category = args.category
        print("Recognizes that there is only one argument")
        # Call the function to get subcategories (assume it's implemented elsewhere)
        subcategories = load_subcategory_data()
        # Filter activities based on the category (example logic)
        for subcategory in subcategories:
            if subcategory['category'] == category:
                list_of_activities.append(subcategory['activity'])
    return list_of_activities