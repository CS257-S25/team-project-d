'''Connects to the database'''
import sys
import psycopg2
from ProductionCode import psql_config as config

class DataSource:
    '''Class to connect to database and create sql table'''
    def __init__(self):
        '''Constructor that initiates connection to database'''
        self.connection = self.connect()

    def connect(self):
        '''Initiates connection to database using information in the psql_config.py file.
        Returns the connection object.'''
        try:
            connection = psycopg2.connect(database=config.DATABASE, user=config.USER,
            password=config.PASSWORD, host="localhost")
        except psycopg2.Error as e:
            print("Connection error: ", e)
            sys.exit()
        return connection

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
<<<<<<< HEAD

            category_id = ''
            query = "SELECT * FROM category WHERE category_ID LIKE %s"
            names = self.get_names_from_list(self.get_correct_list(category_id, query))
            return names

            #cursor = self.connection.cursor()
            #cursor.execute("SELECT category FROM category")
            #records = [row[1] for row in cursor.fetchall()]
            #return records

=======
            cursor = self.connection.cursor()
            cursor.execute("SELECT category FROM category")
            all_cats = cursor.fetchall()
            records = []
            for category in all_cats:
                records.append(category[0])
            return records
>>>>>>> 023e8dcbbf43725cd8a942ce7774cd088114cd5b
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

    #####################################################
    ###########    Get Top Activity By Age    ###########
    #####################################################
    def get_top_by_age(self, age):
        '''finds the top activity for a given age
        param age: the age to find the top activity for'''
        age = self.validate_age(age)
        if age is None:
            return "invalid age, please use a number between 15 and 80"

        records= self.get_top_records(age)
        if records is None:
            return "No data found for this age :("

        top_activities = self.convert_ids_to_names(records)

        return top_activities

    # Helpers!
    def validate_age(self, age):
        '''Helper method to validate the age input and return as int if valid, else None'''
        try:
            age_int= int(age)
        except ValueError:
            return None

        if age_int not in range(15, 81):
            return None
        return age_int

    def get_top_records(self,age):
        '''Helper method to Query the database to get the top 3 activities for given age
        return list of tuples or None'''
        try:
            cursor = self.connection.cursor()
            q = f'SELECT activity_id, "{age}" FROM data_2223 ORDER BY "{age}" DESC LIMIT 3;'
            cursor.execute(q)
            records = cursor.fetchall()

            if not records:
                return "no data found for this age"

            return records

        except psycopg2.Error as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def convert_ids_to_names(self, records):
        ''' Helper Method to convert activity_id to activity names
        return list of (name, hours)'''
        top_activities= []

        for activity_id, hours in records:
            name = self.get_name_from_id('activities', 'activities_ID',
                                            'activities', activity_id)
            top_activities.append((name, hours))
        return top_activities

    #####################################################
    ###########            Compare            ###########
    #####################################################
    def compare_by_age(self, age, activity):
        '''finds the time spent on an activity for a given age in 2022-2023 and 10 years before
        param age: the age to find the top activity for
        param activity: the activity to find the time spent on'''
        try:
            age= int(age)
        except ValueError:
            return "invalid age, please use a number between 15 and 80"

        if age not in range(15, 81):
            return "invalid age, please use a number between 15 and 80"
        try:
            hours = self.compare_by_age_hours(age, activity)
            return hours

        except psycopg2.Error as e:
            print ("Something went wrong when executing the query: ", e)
            return None

    def compare_by_age_hours(self, age, activity):
        '''finds the time spent on an activity for a given age in 2022-2023 and 10 years before'''
        cursor = self.connection.cursor()
        activity_id = self.get_id_from_name('activities', 'activities_ID',
                                            'activities', activity)
        cursor.execute(self.create_query_for_compare(age, activity_id), (age, activity_id,))
        records = cursor.fetchall()
        if not records:
            return "no data found for this age"
        hours = (records[0][0], records[1][0])
        return hours

    def create_query_for_compare(self, age, activity_id):
        '''Helper method to create the query for comparing the activity
        param age: the age to find the top activity for
        param activity_id: the activity id to find the time spent on'''
        q_new = f'SELECT "{age}" FROM data_2223 WHERE activity_id = \'{activity_id}\''
        q_old = f'SELECT "{age}" FROM data_1213 WHERE activity_id = \'{activity_id}\''
        q = q_new + " UNION ALL " + q_old + ";"
        return q
