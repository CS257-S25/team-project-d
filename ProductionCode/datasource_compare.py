'''Connects to the database'''
import sys
import psycopg2
from ProductionCode import psql_config as config
from ProductionCode.datasource_activities import DataSource

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