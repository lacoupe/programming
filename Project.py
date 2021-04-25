# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

import pandas as pd

print('Welcome to the Wealth Management Planner')
print('Please follow the instructions on the terminal')
print('We will begin by asking you some questions to better know you and simulate your potential first salary')


try:
    age =int(input("How old are you ? "))
    if age<0:
        raise ValueError("%d is not a valid age. Age must be positive (or zero) and integer."%age)
except ValueError:
    print("%d is not a valid age. Age must be positive (or zero) and integer."%age)


try:
    experience =float(input("How many years of work experience do you already have ? "))
    if experience<0:
        raise ValueError("Please, enter an integer and positive number")
except ValueError:
    print("Please, enter an integer and positive number")
    

try:
    capital_q =str(input("Do you have a starting capital (Yes/No) ? "))
    if capital_q not in ('Yes','yes','No','no'):
        raise ValueError('Please, answer by Yes or No')
except ValueError:
        print('Please, answer by Yes or No')
try:
    if capital_q in ('Yes','yes'):
        capital_0 =float(input("How much is your starting capital ? "))
        if capital_0<0:
            raise ValueError("Please, enter a positive number")
except ValueError:
        print("Please, enter a positive number")
    
    

sectors = ['Banking and Insurance','Accounting','Human Ressources','IT','Law','Education','Healthcare',\
           'Industrial','Real Estate','Public Services','Hospitality',\
           'Consulting and Management','Energy and utilities']
    
    
    
print(sectors)
try:
    sector_choosed =str(input("Among those sectors, in which one do you work ? "))
    if sector_choosed not in sectors:
        raise ValueError('Please,choose among the sectors listed')
except ValueError:
        print('Please,choose among the sectors listed')
    

try:
    education =int(input("How many years of education do you have after High School ? "))
    if education<0:
        raise ValueError("%d is not a valid number. Please, enter a positive and integer number."%education)
except ValueError:
    print("%d is not a valid number. Please, enter a positive and integer number."%education)


sal = [90000,85000,80000,75000,70000,65000,60000,55000,50000,45000,40000,35000,30000]
growth_rate = [0.02,0.03,0.02,0.03,0.04,0.05,0.02,0.03,0.04,0.05,0.06,0.02,0.01]

Salaries = pd.DataFrame(
    {'Sector':sectors,
     'Starting Salary': sal,
     'Annual Growth Rate': growth_rate})
Salaries.set_index('Sector',inplace=True)

agent_salary = Salaries.loc[sector_choosed][0]
agent_salary_g = Salaries.loc[sector_choosed][1]


if experience == 0:
    agent_salary = agent_salary
elif 1<= experience <=3:
    agent_salary += 1000
elif experience <=5 :
    agent_salary += 2000
elif experience <= 10 :
    agent_salary +=3000
else :
    agent_salary +=4000
    

if education == 0:
    agent_salary = agent_salary
elif 1<= education <=3:
    agent_salary += 1000
elif experience <=5 :
    agent_salary += 2000
else :
    agent_salary +=3000
    
print('With the information collected about you, your starting salary is %d '%agent_salary)



