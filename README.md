CS257 S25

Claire Holmes, Camila Mendoza, KD Meraz

To run our command line interface, there are currently two features:

1) Our code can tell the user the activity that participants of a certain age spend the most time doing:

Usage: python3 cl.py --age <age from 15-85> --top

python3 cl.py --age 20 --top

2) Our code can tell the user all of the activities that are listed under a subcategory of a category. First tell the command line the cateogry that you are interested in, then choose from the subcategories and run the second command.

*Note: this usage statement is for current test data*

Usage: python3 cl.py --category <"Personal Care Activities" or "Household Activities">

python3 cl.py --category "Household Activities"

Usage: python3 cl.py --category <valid category> --subcategory <valid subcategory> 

*reference python3 cl.py --category for valid subcategory inputs because they change based on the category*

python3 cl.py --category "Household Activities" --subcategory "Housework"
