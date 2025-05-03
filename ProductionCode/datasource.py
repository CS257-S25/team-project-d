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

    def get_activity_list(self):
        '''Get a list of activities given the subcategory'''
        #Open a cursor to perform database operations
        id= 'T0101'
        query = "SELECT * FROM activities WHERE activities_ID LIKE %s"
        return self.get_correct_list(id,query)
    
    def get_subcategory_list(self):
        '''Gets a list of subcategories with a given category'''
        id = 'T01'
        query = "SELECT * FROM subcategory WHERE subcategory_ID LIKE %s"
        return self.get_correct_list(id,query)

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
        #Retrieve query results
            records = cursor.fetchall()

            return records
        except psycopg2.Error as e:
            print ("Something went wrong when executing the query: ", e)
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
            print(cursor.fetchall())

        except psycopg2.Error as e:
            print ("Something went wrong when executing the query: ", e)
