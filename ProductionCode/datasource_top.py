'''Connects to the database and does get top activity by age function'''
import psycopg2
from ProductionCode.datasource_activities import DataSource as activities
from ProductionCode.datasource import BaseDataSource as base_data_source

class DataSource(base_data_source):
    '''Class to connect to database and execute functions
    for Get Top Activity By Age'''

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
            name = activities.get_name_from_id(self, 'activities', 'activities_ID',
                                               'activities', activity_id)
            top_activities.append((name, hours))
        return top_activities
