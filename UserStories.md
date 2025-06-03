User story 1: a college student wants to know the most common activity for a 21 year old

Acceptance tests:
1) given they input a valid age (ex: (int) 21)---> the program should return the most common activity for that age 
2) given they input an invalid age group format (ex: (str) "twenty one")---> the program should return error + message that says no data available try again in range of 15-80 using integers
3) given they input an invalid age group/ out of range/no data (ex: (int) 200)---> the program should return error + message that says no data available try again in range of 15-80 using integers


User Story 2: a parent wants to compare the amount of  hours an average person of their kid’s age (age 16) spends Watching tv (non religious) to the average hours of 16 year olds, 10 years ago spent Watching tv (non religious) so that they know if they spend above average time watching tv

Acceptance tests: 
1) given the user inputs valid age and activity values ->the program returns the hours for a certain activity between their age group now and their age group 10 yeras ago.
2) given the user inputs invalid activity or age group -> program returns usage If the user inputs invalid demographic values:


User story 3: a user wants a list of activities under a specific category (ex: Exercise)

Acceptance tests:
1) given they input a valid category -> the program returns the list of subcategories
2) given they input a valid category and valid subcategory -> the program returns the list of subcategories
3) given they input an invalid category and/or invalid subcategory -> the program returns the usage statement

