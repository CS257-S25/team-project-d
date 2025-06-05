'''Connects to the database'''
import psycopg2
from ProductionCode.datasource import BaseDataSource as base_data_source

class DataSource(base_data_source):
    '''Class to connect to database and execute functions
    for processing, accessing, and displaying categories,
    subcategories, and activities'''

    #####################################################
    ###########        Get Cat/Sub/Act        ###########
    #####################################################
    def get_activity_list(self, subcategory):
        '''Get a list of activities given the subcategory'''
        subcategory_id= self.get_id_from_name("subcategory",
                                              "subcategory_ID", "subcategory", subcategory)

        if not subcategory_id:
            print(f"subcategory name {subcategory} not found")
            return None

        subcategory_id = subcategory_id + "%"
        query = "SELECT * FROM activities WHERE activities_ID LIKE %s"
        names = self.get_names_from_list(self.get_correct_list(subcategory_id,query))
        return names

    def get_subcategory_list(self, category):
        '''Gets a list of subcategories with a given category'''
        category_id = self.get_id_from_name("category","category_ID", "category", category)
        if not category_id:
            print(f"category name {category} not found")
            return None

        category_id = category_id + "%"
        query = "SELECT * FROM subcategory WHERE subcategory_ID LIKE %s"
        names = self.get_names_from_list(self.get_correct_list(category_id,query))
        return names

    def get_category_list(self):
        '''Gets the list of categories available'''
        try:
            cursor = self.connection.cursor()
            cursor.execute("SELECT category FROM category")
            all_cats = cursor.fetchall()
            records = []
            for category in all_cats:
                records.append(category[0])
            return records
        except psycopg2.Error as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def get_correct_list(self, list_id, query):
        '''Helper method for getting lists of categories, subcategories, or activities'''
        try:
            cursor = self.connection.cursor()
            level_id = str(list_id)
            pattern = level_id + '%'
            cursor.execute(query, (pattern,))
            records = cursor.fetchall()
            return records
        except psycopg2.Error as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def get_id_from_name(self, table, id_column, name_column, name):
        '''helper method to get a name from an id in a given table
        params: 
            table, the table name (ex. category, subcategory, activities)
            id_column, the id column name (ex. 'category_ID') 
            name_column, the name column to match (ex. 'category_Name')
            id, the id to search for (ex. 'Personal Care Activities')
        returns the value for the id or none'''
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT {id_column} FROM {table} WHERE {name_column} = '{name}';")
            records = cursor.fetchone()

            if records:
                return records[0]

            return None
        except psycopg2.Error as e:
            print(f"Error getting activity from {table}: ", e)
            return None

    #Helpers!
    def get_name_from_id(self, table, id_column, name_column, id_find):
        '''helper method to get a name from an id in a given table
        params: 
            table, the table name (ex. category, subcategory, activities)
            id_column, the id column name (ex. 'category_ID') 
            name_column, the name column to match (ex. 'category_Name')
            id, the id to search for (ex. 'T01')
        returns the value for the id or none'''
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT \"{name_column}\" FROM {table} " \
                           f"WHERE {id_column} = '{id_find}';")
            records = cursor.fetchall()

            if records:
                return records[0][0]

            return None
        except psycopg2.Error as e:
            print(f"Error getting activity from {table}: ", e)
            return None

    def get_names_from_list(self, list_of_id_name):
        '''helper method to return a list of names from a list of ids and names
        params: 
            list_of_id_name, a list of tuples with the id and name
        returns a list of names'''
        names = []
        for id_name in list_of_id_name:
            name = str(id_name[1])
            names.append(name)
        return names

    def get_subcategory_from_activity(self, activity):
        '''helper method to get the subcategory from an activity
        params: activity, the activity to search for
        returns the subcategory'''
        try:
            cursor = self.connection.cursor()
            activity_id = self.get_id_from_name('activities', 'activities_ID',
                                                'activities', activity)
            cursor.execute("SELECT activities_ID FROM activities "\
                           f"WHERE activities_ID = '{activity_id}';")
            records = cursor.fetchone()
            if records:
                subcategory_id = str(records[0][0:-2])
                subcategory = self.get_name_from_id('subcategory', 'subcategory_ID',
                                                    'subcategory', subcategory_id)
                return subcategory

            return None
        except psycopg2.Error as e:
            print(f"Error getting subcategory from activities: {e}")
            return None
