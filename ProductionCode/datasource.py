'''Connects to the database'''
import sys
import psycopg2
from ProductionCode import psql_config as config
from ProductionCode.activity_id_list import columns

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

    def get_activity_list(self, subcategory):
        '''Get a list of activities given the subcategory'''
        subcategory_id= self.get_id_from_name("subcategory", 
                                              "subcategory_ID", "subcategory", subcategory)

        if not subcategory_id:
            print(f"subcategory name {subcategory} not found")
            return "not found "

        query = "SELECT * FROM activities WHERE activities_ID LIKE %s"
        return self.get_correct_list(subcategory_id,query)

    def get_subcategory_list(self, category):
        '''Gets a list of subcategories with a given category'''
        category_id = self.get_id_from_name("category","category_ID", "category", category)

        if not category_id:
            print(f"category name {category} not found")
            return "not found "

        query = "SELECT * FROM subcategory WHERE subcategory_ID LIKE %s"
        return self.get_correct_list(category_id,query)

    def get_category_list(self):
        '''Gets the list of categories available'''
        id = ''
        query = "SELECT * FROM category WHERE category_ID LIKE %s"
        return self.get_correct_list(id, query)

    def get_correct_list(self, id, query):
        '''Helper method for getting lists of categories, subcategories, or activities'''
        try:
            cursor = self.connection.cursor()
            level_id = str(id)
            pattern = level_id + '%'
            cursor.execute(query, (pattern,))
            records = cursor.fetchall()
            return records
        except psycopg2.Error as e:
            print ("Something went wrong when executing the query: ", e)
            return None
        return records
    
    def get_id_from_name (self, table, id_column, name_column, name):
        '''helper method to get an id from a name in a given table
        params: 
            table, the table name (ex. category, subcategory, activities)
            id_column, the id column name (ex. 'category_ID') 
            name_column, the name column to match (ex. 'category_Name')
            name, the name to search for (ex. 'Personal Care Activities')
        returns the ID calue for the name or none'''
        try:
            cursor = self.connection.cursor()
            cursor.execute(f"SELECT {name_column} FROM {table} WHERE {id_column} = '{name}';")
            records = cursor.fetchone()

            if records: 
                #issue: returning ('T0101', 'Sleeping') want it to just return Sleeping
                return records[0]
            else:
                return None
        except psycopg2.Error as e: 
            print(f"Error getting ID from {table}: ", e)
            return None

    def get_top_by_age(self, age, table='data_2223'):
        '''finds the top activity for a given age
        param age: the age to find the top activity for'''
        if int(age) not in range(15, 81):
            return "invalid age, please use a number between 15 and 80"
        try:
            cursor = self.connection.cursor()
            q = f'SELECT (activity_id, "{age}") FROM "{table}" ORDER BY activity_id ASC LIMIT 1;'
            cursor.execute(q)
            records = cursor.fetchall()
            if not records:
                return "no data found for this age"
            return records

        except psycopg2.Error as e:
            print ("Something went wrong when executing the query: ", e)
            return None
