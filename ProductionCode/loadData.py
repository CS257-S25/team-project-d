'''file: loadData.py'''

import csv

def load_data():
    ''' Purpose: Load data from a file
    Returns: None'''
    print("Loading data from file...")
    #actually use this:"Data/teamproject22-23FINAL_updatedpls.csv"
    with open("Data/teamproject22-23FINAL_updatedpls.csv", "r") as file:
        ##### usually: keep these ones but actully just edit the dataset and remove first useless row
        
        #lines = file.readlines()
        #     remove the first line (header) from the file because it was just the title 
        #cleaned_lines = lines[1:]
        #     use DictReader to read the csv file into a dictionary (avoid closing the file early)
        #reader =csv.DictReader(cleaned_lines)
        #data = list(reader) #convert to list to be able to pass around the data

        ##############
        reader=csv.DictReader(file)
        data = list(reader)
        #print("Sample row:", data[2])
        #print("CSV HEaders:", reader.fieldnames)
        return data

