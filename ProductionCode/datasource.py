'''Connects to the database'''
import sys
import psycopg2
from ProductionCode import psqlConfig as config

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
        except ConnectionError as e:
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


    def get_correct_list(self, id, query):
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

