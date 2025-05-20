CS257 S25

Claire Holmes, Camila Mendoza, KD Meraz

**Copy statements for SQL database tables.**
**After creating data tables, run our SQL-based Flask App by running app.py from the command line.**

\copy activities FROM 'Data/Activities_Data.csv' DELIMITER ',' CSV header

\copy subcategory FROM 'Data/Subcategories_Data.csv' DELIMITER ',' CSV header

\copy category FROM 'Data/Categories_Data.csv' DELIMITER ',' CSV header

\copy data_2223 FROM 'Data/averaged_by_age_22-23.csv' DELIMITER ',' CSV header

\copy data_1213 FROM 'Data/averaged_by_age_12-13.csv' DELIMITER ',' CSV header


**To run our command line interface, there are currently two features and information on available categories, subcategories, and activities:**

1) Our code can tell the user the activity that participants of a certain age spend the most time doing:

Usage: python3 cl.py --age <age from 15-80>

python3 cl.py --age 20

2) Our code can tell the user the number of average hours that a certain age spent on an activity in 2022-2023 compared to 2012-2013.

Usage: python3 cl.py --compare <age from 15-80> --activity <valid activity>

python3 cl.py --compare 23 --activity "Sleeping"

3) Our code can tell the user all of the activities that are listed under a subcategory of a category. First tell the command line the cateogry that you are interested in, then choose from the subcategories and run the second command.

Usage: python3 cl.py --category <valid category>

python3 cl.py --category "Household_Activities"

Usage: python3 cl.py --category <valid category> --subcategory <valid subcategory> 

*reference python3 cl.py --category for valid subcategory inputs because they change based on the category*

python3 cl.py --category "Household_Activities" --subcategory "Housework"

