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
            query = f"SELECT {id_column} FROM {table} WHERE {name_column} = %s"
            cursor.execute(query, (name,))
            records = cursor.fetchone()

            if records: 
                #issue: returning ('T0101', 'Sleeping') want it to just return Sleeping
                return records[0]
            else:
                return None
        except psycopg2.Error as e: 
            print(f"Error getting ID from {table}: ", e)
            return None


    def get_top_by_age(self, age):
        '''finds the top activity for a given age
        param age: the age to find the top activity for'''
        try:
            cursor = self.connection.cursor()
            query = "SELECT " \
            "CASE " \
            "WHEN SUM(Sleeping) > SUM(Hygiene) AND SUM(Sleeping) > SUM(Cleaning) AND " \
            "SUM(Sleeping) > SUM(Work) AND SUM(Sleeping) > SUM(Eating) THEN 'Sleeping' " \
            "WHEN SUM(Hygiene) > SUM(Sleeping) AND SUM(Hygiene) > SUM(Cleaning) AND " \
            "SUM(Hygiene) > SUM(Work) AND SUM(Hygiene) > SUM(Eating) THEN 'Hygiene' " \
            "WHEN SUM(Cleaning) > SUM(Sleeping) AND SUM(Cleaning) > SUM(Hygiene) AND " \
            "SUM(Cleaning) > SUM(Work) AND SUM(Cleaning) > SUM(Eating) THEN 'Cleaning' " \
            "WHEN SUM(Work) > SUM(Sleeping) AND SUM(Work) > SUM(Hygiene) AND SUM(Work) > " \
            "SUM(Cleaning) AND SUM(Work) > SUM(Eating) THEN 'Work' " \
            "WHEN SUM(Eating) > SUM(Sleeping) AND SUM(Eating) > SUM(Hygiene) AND " \
            "SUM(Eating) > SUM(Cleaning) AND SUM(Eating) > SUM(Work) THEN 'Eating' " \
            "END AS top_activity " \
            "FROM time_use WHERE age=%s"

            cursor.execute(query, (age,))
            records= cursor.fetchone()
            return records

        except psycopg2.Error as e:
            print ("Something went wrong when executing the query: ", e)
            return None
