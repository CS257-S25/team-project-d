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

    def query_filter_rows_for_age(self, age):
        q= "CREATE TEMP TABLE age_filtered AS SELECT * FROM data WHERE age = %s;"
        return q
    
    def turn_into_activityID_and_duration(self):
        columns = activity_id_list()# put this list into another file and call it cuz why is it so long
        
        sql_lines = []
        for col in columns: 
            line = f"SELECT age, ROW_NUMBER() OVER() AS person_id, '{col}' AS activity_id, {col} AS duration FROM age_filtered"
            sql_lines.append(line)

        unpivot_sql = "\nUNION ALL\n".join(sql_lines)
        q= "CREATE TEMP TABLE unpivoted AS\n" + unpivot_sql + ";"
        print(q)
        return q
    
    def find_max_activity_per_person(self):
        q = "CREATE TEMP TABLE top_activity_per_person AS\
            SELECT person_id, activity_id \
            FROM unpivoted \
            WHERE (person_id, duration) IN ( \
                SELECT person_id, MAX(duration) \
                FROM unpivoted \
                GROUP BY person_id \
            );"

    def count_most_frequent_top_activity(self):
        q = "SELECT activity_id, COUNT(*) AS frequency \
            FROM top_activity_per_person \
            GROUP BY activity_id \
            ORDER BY frequency DESC \
            LIMIT 1;" 
        return q

    def get_top_by_age(self, age):
        '''finds the top activity for a given age
        param age: the age to find the top activity for'''
        try:
            cursor = self.connection.cursor()
            #filter rows by age
            query1 = self.query_filter_rows_for_age(age)
            cursor.execute ("DROP TABLE IF EXISTS age_filtered;")
            cursor.execute(query1, (age,))

            #unpivot to activity_id and duration 
            query2 = self.turn_into_activityID_and_duration
            cursor.execute("DROP TABLE IF EXISTS unpivoted;")
            cursor.execute(query2)

            #find top activity per person
            query3 =self.find_max_activity_per_person()
            cursor.execute("DROP TABLE IF EXISTS top_activity_per_person;")
            cursor.execute(query3)

            #count most frequent top activity
            query4 = self.count_most_frequent_top_activity()
            cursor.execute(query4)
            records = cursor.fetchone()
            return records

        except psycopg2.Error as e:
            print ("Something went wrong when executing the query: ", e)
            return None
