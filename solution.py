# Madison London
# This program calculates a qualifying offer based on the data from https://questionnaire-148920.appspot.com/swe/data.html
import pandas as pd
import numpy as np
from re import sub
from decimal import Decimal
import datetime

data = pd.read_html("https://madisonlondon.github.io/mlbsalarydata.github.io/")
date = datetime.datetime.now()

salaries1 = data[0]['Salary']
salaries2 = []

for s in salaries1: 
    s = str(s)
    if '$' in s:
        s = s.split('$') # Separate the salary value from the dollar sign 
        s = s[len(s) - 1] # Since we do not know how many '$'s preceed the salary, we want to take the last token 
        salaries2.append(float(sub(r'[^\d.]', '', s))) # Remove the commas and convert the string to a float 

salaries2.sort() # Sorting in ascending order 

q1, q3 = np.percentile(salaries2,[25,75]) # Find the first quartile and third quartile
iqr = q3 - q1
lower_bound = q1 - (1.5 * iqr) 
upper_bound = q3 + (1.5 * iqr) 

outliers = False
outliersData = []
if salaries2[0] < lower_bound:
    outliers = True
    for i in salaries2: 
        if i < lower_bound: 
            outliersData.append(i)
        else: 
            break
elif salaries2[len(salaries2) - 1] > upper_bound: 
    outliers = True
    for i in reversed(salaries2): 
        if i > upper_bound: 
            outliersData.append(i)
        else: 
            break

average = round(sum(salaries2) / len(salaries2)) 

if outliers: 
    print("Based on the data taken on " + str(date.strftime("%B")) +  " " + str(date.day) + ", " + str(date.year) + " at " + str(date.strftime("%X")) + " from " + str(len(salaries2)) + " players, the average salary is $" + str(average) + ", and there were " + str(len(outliersData)) + " outlier(s) found.")
    print("Would you like to see the outlier(s) listed?")
    val = input("y/n: ")
    if val == "y": 
        print(outliersData)
else: 
    print("Based on the data taken on " + str(date.strftime("%B")) +  " " + str(date.day) + ", " + str(date.year) + " at " + str(date.strftime("%X")) + " from " + str(len(salaries2)) + " players, the average salary is $" + str(average) + ", and there are no outliers." )




