import sys
import psycopg2
from ProductionCode import psql_config as config

class BaseDataSource:
    '''Class to connect to database for all functions'''

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
