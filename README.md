CS257 S25

Claire Holmes, Camila Mendoza, KD Meraz

**Copy statements for SQL database tables.**
**After creating data tables, run our SQL-based Flask App by running app.py from the command line.**

\copy activities FROM 'Data/Activities_Data.csv' DELIMITER ',' CSV header

\copy subcategory FROM 'Data/Subcategories_Data.csv' DELIMITER ',' CSV header

\copy category FROM 'Data/Categories_Data.csv' DELIMITER ',' CSV header

\copy data_2223 FROM 'Data/averaged_by_age_22-23.csv' DELIMITER ',' CSV header

\copy data_1213 FROM 'Data/averaged_by_age_12-13.csv' DELIMITER ',' CSV header

**To run our python-based Flask App, run python3 app_OG.py from the command line.**

The features of the app are the same as the command line interface. More details on how to access these features are on the homepage of the Flask website and are repeated here: 

Homepage Instructions:
1) TO GET the top activity for a certain age, go to /get-top/<age>
2) TO GET a list of all category options, go to /get-all-categories 
3) TO GET a list of subcategory options from a category, go to /get-subcategories/<category> 
4) TO GET a list of activities from a subcategory, go to /get-activities/<category>/<subcategory>


**To run our command line interface, there are currently two features:**

1) Our code can tell the user the activity that participants of a certain age spend the most time doing:

Usage: python3 cl.py --age <age from 15-85> --top

python3 cl.py --age 20 --top

2) Our code can tell the user all of the activities that are listed under a subcategory of a category. First tell the command line the cateogry that you are interested in, then choose from the subcategories and run the second command.

*Note: this usage statement is for current test data*

Usage: python3 cl.py --category <valid category>

python3 cl.py --category "Household Activities"

Usage: python3 cl.py --category <valid category> --subcategory <valid subcategory> 

*reference python3 cl.py --category for valid subcategory inputs because they change based on the category*

python3 cl.py --category "Household Activities" --subcategory "Housework"
