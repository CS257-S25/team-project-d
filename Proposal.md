# Title
The Hobby Clock: Reflecting Your Time Against the Nation's (Gemini help/inspired)

# Dataset(s) summary
The dataset is based on the American Time use survey over 20 years. It includes different categories of time use, i.e childcare, sleeping, hobbies, etc. and compares the different characteristics i.e race, age, sex, region, etc. of the surveyed individuals. 

# Dataset(s) Metadata
https://www.icpsr.umich.edu/web/NADAC/studies/36268?utm_source=NADAC%3AATUS+2003-2023_web&utm_medium=NADAC%3AATUS+2003-2023_web&utm_campaign=NADAC%3AATUS+2003-2023_web&utm_id=NADAC%3AATUS+2003-2023 
Downloaded: April 7th, 2025, Version V8 of Mar 10, 2025
Principal Investigator: United States. Bureau of Labor Statistics. Inter-university Consortium for Political and Social Research
American Time Use Survey (ATUS): Arts Activities, [United States], 2003-2023 (ICPSR 36268)
Terms: https://www.icpsr.umich.edu/web/ICPSR/studies/36268/terms, no concerns for this project

United States. Bureau of Labor Statistics. American Time Use Survey (ATUS): Arts Activities, 
[United States], 2003-2023. Inter-university Consortium for Political and Social Research [distributor], 2025-03-10. https://doi.org/10.3886/ICPSR36268.v8 

# Potential User Interactions
User Story 1: A user can search up their generation’s leisure time to determine whether the amount of TikTok they watch is normal.
Acceptance criteria: 
If the user inputs valid generation and TikTok time, works
Test: available generation, possible TikTok times (from none to many hours)
If the user inputs invalid generation and TikTok time, does not work
Test: generations not listed in the set, test over 24 hours of TikTok use per day

User Story 2: A user can input their own activity times to see a visualization of their spent time so that they can compare to others of similar demographics to get inspiration for diversifying their hobbies/leisure time.
Acceptance criteria: 
If user inputs a valid 24 hour time:
Test amount of time left in their day
If user inputs invalid time within the 24 hr timeframe:
Ask for correct input according to the time guidelines given 

User Story 3: A user wants to compare their leisure time to the leisure time of their demographic data ten or twenty years prior
Acceptance criteria: 
If the user inputs valid demographic values:
Test State, gender, children status, what type of demographic?
If the user inputs invalid demographic values:
Test common misspelled  words, addition of other characters
