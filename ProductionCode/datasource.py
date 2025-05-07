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
        subcategory_id= self.get_id_from_name("subcategory", "subcategory_ID", "subcategory", subcategory)
        
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

    def get_top_by_age(self, age):
        '''finds the top activity for a given age
        param age: the age to find the top activity for'''
        try:
            cursor = self.connection.cursor()
            age_str = str(age)
            query = f'SELECT (activity_id, "{age_str}") FROM transposed ORDER BY activity_id ASC LIMIT 1;'
            cursor.execute(query)
            records = cursor.fetchall()
            return records

        except psycopg2.Error as e:
            print ("Something went wrong when executing the query: ", e)
            return None
