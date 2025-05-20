User story 1: a user wants to know the most common activity for a given age group

Acceptance tests:
1) given they input a valid age group (ex: (int) 18)---> the program should return the most common activity for that age group
2) given they input an invalid age group format (ex: (str) "eighteen")---> the program should return usage statement
3) given they input an invalid age group/ out of range/no data (ex: (int) 200)---> the program should return usage statement, message that says no data available

User Story 2: a user wants to compare the leisure time on a certain activity of their age group to the leisure time of their age group ten years prior

Acceptance tests:

1) given the user inputs valid demographic values ->the program returns the hours for a certain activity between their age group now and their age group 10 yeras ago.
2) given the user inputs invalid activity or age group -> program returns usage 
If the user inputs invalid demographic values:

User story 3: a user wants a list of activities under a specific category (ex: Exercise)

Acceptance tests:
1) given they input a valid category -> the program returns the list of subcategories
2) given they input a valid category and valid subcategory -> the program returns the list of subcategories
3) given they input an invalid category and/or invalid subcategory -> the program returns the usage statement

