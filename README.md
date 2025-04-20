CS257 S25

Claire Holmes, Camila Mendoza, KD Meraz

To run our command line interface, there are currently two features:

1) Our code can tell the user the activity that participants of a certain age spend the most time doing:

python3 cl.py --age 20 --top

2) Our code can tell the user all of the activities that are listed under a subcategory of a big category. First tell the command line the big cateogry that you are interested in, then choose from the subcategories and run the second command.

python3 cl.py --category "Sports, Exercise, & Recreation"

python3 cl.py --subcategory "Participating in Sports, Exercise, & Recreation"
