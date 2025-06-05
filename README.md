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

We also deleted a few functions from app.py that relied on the user typing in specific urls that users didn't really have to type anymore due to new front end features. Because of this, they were not really being used anymore and were dead code. 

*Long Class:*

The Long Class is known for having a lot of functions, methods, and lines of code that may affect the readability of the code. Our approach to this issue was to divide one of our long classes into three based on the website’s components.

Our long class was originally called datasource.py, but has now been split up into the following files: datasource_activities.py, datasource_compare.py, and datasource_top.py. All of the code following line 26 in all three files used to be together in datasource.py.

To refactor our code, we decided to make three DataSource classes, each one for our three user stories: finding activities, getting the top three activities by age, and comparing data between ten decades. Depending on what component the user would like to use, python will access the corresponding DataSource.

*Duplicate Code:*

Having duplicate code, especially between two classes will only take up more data, decrease the readability, and possibly confuse the program. When refactoring for out long class, we ended up with three classes, each withholding a piece of code that was the same for the other three.

The files in question are as follows: datasource_activities.py, datasource_compare.py, and datasource_top.py. Each of these files created a Datasource constructor (previously lines 9-12) and connected itself to the database (previously lines 13-23).

To complement the refactoring of our long class, we created a superclass called datasource.py, that includes a DataSource constructor and connects to the database. All three datasource files, that use the database for their functions, now inherit this class, eliminating duplicate code.

**TD5: Front-End Design Improvements**

Usability Issue: Unecessary/Useless form 
Page where change was made: compare_form.html
What we did to adress the issue: Removed Select Years of Interest part of the Compare Page since we only have two to choose from. 

Usability Issue: Structure in html pages could be improved
Page where change was made: get_top.html, compare_activity.html, 404.html
What we did to adress the issue: Added more headings in the html files to add structure to the pages (get_top.html line 20), (404.html liknes 6 and 8), (compare_activity.html line 20)

Usability Issue: 404 page not useful or stylish 
Page where change was made: 404.html
What we did to adress the issue:created an html page with useful instructions for 404 errors and 500 errors and structured them with different headings 

Usability Issue: it might not be clear to users to go to the navigation bar to resubmit a form, people are more used to back buttons or resubmit buttons 
Page where change was made: get_top.html, compare_activity.html, activity_form
What we did to adress the issue: added back buttons to the get_top.html and to compare_activity.html as well as a clear dropdowns button to activity_form.html

Usability Issue: charts should be in a separate file from html
Page where change was made: static folder
What we did to adress the issue:created get_top_chart.js and compare_chart.js to keep html as just structural things

Usability Issue: fonts should be consistent 
Page where change was made: project.css, get_top_chart.js, compare_chart.js
What we did to adress the issue:changed the font of the body in css to make sure all pages have a consistent font. globally changed the font in both js functions to same font as ecerything else

Usability Issue: website should be polished and professional; plots should have better labels  
Page where change was made: get_top_chart.js and compare_chart.js
What we did to adress the issue: some of the labels for the charts were not very clear so we changed them to be more specific 

Usability Issue: users won't really know all possible valid activities to input when trying to use the compare feature and going to find activities might be too much work
Page where change was made: compare --> we made changes to datsource.py, app.py and compare_form.html and created compare_suggestions.js
What we did to adress the issue: we made it so that the form where you input an activity will give you 10 activities that start similarly to what you are typing so that if you don't know what you could look for or the exact wording of an activity, it will give you some suggestions and you can just click one and compare.

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

python3 cl.py --category "Household Activities"

Usage: python3 cl.py --category <valid category> --subcategory <valid subcategory> 

*reference python3 cl.py --category for valid subcategory inputs because they change based on the category*

python3 cl.py --category "Household Activities" --subcategory "Housework"

## 
Thanks to W3Schools html help 
Chart.js help: https://www.chartjs.org/docs/latest/getting-started/usage.html
compare_suggestions help: a mixture of elements from: https://www.youtube.com/watch?v=pdyFf1ugVfk and https://www.w3schools.com/js/js_ajax_php.asp and https://www.algolia.com/blog/engineering/how-to-implement-autocomplete-with-javascript-on-your-website and https://www.w3schools.com/howto/howto_js_autocomplete.asp 
