CS257 S25

Claire Holmes, Camila Mendoza, KD Meraz

---------------------------------------------------------------------------

**TD5: Code Design Improvements**

*The Long Method:*

Our first refactoring focused on shortening one of our method’s lines of code. The main issue with having a long method is its understability; oftentimes, more lines of code makes it harder for other people to understand the method’s purpose. Additionally, more lines means more proneness to the duplication of code and a weaker structure to further build the code. 

The method we restructured is called compare_by_age (starting in line 210), located in datasource.py under the ProductionCode folder. Our method used to be longer than ten lines and served multiple purposes: connecting to the database, accessing our tables to create queries, and executing the queries for our desired output. 

To solve our code smell, we decided to turn the function into three. The compare_by_age (line 210), would be considered our main function, having a try and exempt to recognize valid inputs, and return our desired output. Inside compare_by_age, the method compare_by_age_hours is called. This method connects to the database, gathers the information inputted by the user, and gets the desired output through the data tables; it outputs the amount of time spent on an activity given the age in 2022-2023. To reduce the lines of code required for multiple queries, we created a helper method called create_query_for_compare, which takes in the selected age and activity, and returns a single query line to execute.

*Dead Code:*

Our second refactoring of our code was identifying and deleting unnecessary files in our repository. Having dead code in a directory, where most files depend on each other, can make it difficult to find problems with the code. Furthermore, other file methods that are not supposed to use old code, might still access them without the coder’s knowledge.

The following files were previously used by our python production or old database code that are no longer in use: Data/teamproject12-13.csv, Data/teamproject22-23FINAL_updatedpls.csv, Data/teamproject22-23_database.csv, templates/activity_results.html.

After deleting all of these files, we ensured none of the newer code was dependent on them, and checked that every method was functional in its intended way.


--------------------------------------------------------------

**TD4: Scanability, Satisficing, & Muddling Through**

*Scanability:* 

Our website enables scanability because of the large navigation bar and action buttons. For example, on the hompage we have a button for each of our two functions. A key to the scanability principle is that the user only cares about the task they want to complete. Our project allows for two main functions, so we put the buttons to complete those functions in big letters on the homepage so that the user can easily scan and find the two functions. We make these buttons known to be links because they are underlined. On our pages for the functions, the submit buttons are labeled and in a box to indicate they are clickable. Our Find Activities page has two dropdowns that take advantage of the conventions for dropdown menus by the default being --select category-- and --select subcategory-- so the user knows action needs to be taken, and a small downward triangle on the right side of the box to indicate the list will drop down with all of the options. The navigation is consistent on all of our pages and follow the convention of being across the top of the page. The results for our Top Activity by Age and Find Activities page use bulleted lists to present the results in easily understandable and scannable ways. 

*Satisficing:*

Our website enables satisficing because of the easy navigation between different functions. One of the key ideas of satisficing is that if the wrong choice is chosen in a hurry, it is easy to go back and pick the other options. If the user picks the wrong function from the homepage, when they click the button to go back, there is only one other choice which they can pick quickly and without too much mental effort. On our individual function pages, there are "back" and "clear" buttons that let the user start over their search process if they make the wrong choice or want to try something else (i.e., another age or activity)

*Muddling Through:*

Our website enables muddling through because there are not a large amount of affordances on each page. There is always our navigation bar which includes four possible choices. Our homepage offers two buttons, our Top Activity By Age page has one box to input an age, our Compare page only has two spots for the age and activity, and our Find Activities page has a dropdown for categories and subcategories. Because we limit the number of affordances that our website offers the user, there is less for a user to muddle through and get confused by. The user is less likely to get confused or lost on our site because there are limited options that take them to certain areas of the site.

---------------------------------------------------------------------------

**TD3: Copy statements for SQL database tables.**
**TD3: After creating data tables, run our SQL-based Flask App by running app.py from the command line.**

\copy activities FROM 'Data/Activities_Data.csv' DELIMITER ',' CSV header

\copy subcategory FROM 'Data/Subcategories_Data.csv' DELIMITER ',' CSV header

\copy category FROM 'Data/Categories_Data.csv' DELIMITER ',' CSV header

\copy data_2223 FROM 'Data/averaged_by_age_22-23.csv' DELIMITER ',' CSV header

\copy data_1213 FROM 'Data/averaged_by_age_12-13.csv' DELIMITER ',' CSV header

------------------------------------------------------------------

**TD1: To run our command line interface, there are currently two features and information on available categories, subcategories, and activities:**

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

