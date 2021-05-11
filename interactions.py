# -*- coding: utf-8 -*-
"""
Created on Tue May 11 15:24:00 2021

@author: Antoine
"""

import pandas as pd

### INTRODUCTION; GAME DESCRIPTION; RULES; OPTIONS; ...

def intro():
    
    print('')
    print('---------------------------------------------------------------------------')
    print('-----------------Welcome to the Wealth Management Planner------------------')
    print('---------------------------------------------------------------------------')
    print('')
    print('Decription')
    print('---------------------------------------------------------------------------')
    print(" - This game aims to simulate user's wealth evolution along his life")
    print(" - The simulated timeline goes from user's first job to retirement")
    print(" - The goal is making decisions to reach retirement as rich as possible")
    print(" - Following terminal instructions, you'll be facing different choices")
    print(" - The largest your terminal window is, the better it is!")    
    print('')
    print('Here we go ! Please follow the instructions on the terminal')
    print('---------------------------------------------------------------------------')
    
    
def simulate_salary(sec, exp, ed):
    
    sectors = ['Banking and Insurance','Accounting','Human Ressources',\
               'IT','Law','Education','Healthcare', 'Industrial','Real Estate',\
                'Public Services','Hospitality','Consulting and Management','Energy and utilities']
    
    sal = [90000,85000,80000,75000,70000,65000,60000,55000,50000,45000,40000,35000,30000]
    
    Salaries = pd.DataFrame(
        {'Sector':sectors,
         'Starting Salary': sal})
    Salaries.set_index('Sector',inplace=True)
    
    agent_salary = Salaries.loc[sec][0]

    
    if exp == 0:
        agent_salary = agent_salary
    elif 1<= exp <=3:
        agent_salary += 1000
    elif exp <=5 :
        agent_salary += 2000
    elif exp <= 10 :
        agent_salary +=3000
    else :
        agent_salary +=4000
        
    
    if ed == 0:
        agent_salary = agent_salary
    elif 0< ed <=3:
        agent_salary += 1000
    elif 3< ed <=5 :
        agent_salary += 2000
    else :
        agent_salary +=3000

    return agent_salary


def get_info_salary():
    
    sectors = ['Banking and Insurance','Accounting','Human Ressources','IT','Law','Education','Healthcare',\
           'Industrial','Real Estate','Public Services','Hospitality',\
           'Consulting and Management','Energy and utilities']
    
    
    print('')
    print('First Salary Simulator')
    print('---------------------------------------------------------------------------')
    print('')
    print('We will begin by asking you some questions to better know you \nand simulate your potential first salary')

    #Age question
    while True : 
        try:
            age =int(input("How old are you ? Enter a positive number "))
            if age<0:
                raise ValueError("This is not a valid age. Age must be positive (or zero).")
        except ValueError:
            print("This is not a valid age. Age must be positive (or zero) and integer.")
            continue
        else :
            break
    
    #Education question
    while True :
        try:
            ed = int(input("How many years of education do you have after High School ? "))
            if ed<0:
                raise ValueError("Your input is not a valid number. Please, enter a positive and integer number.")
        except ValueError:
            print("Your input is not a valid number. Please, enter a positive and integer number.")
            continue
        else:
            break
    
    #Experience question
    while True:
        try:
            exp  =float(input("How many years of work experience do you already have ? Enter a positive number "))
            if exp<0:
                raise ValueError("Please, enter a positive number")
        except ValueError:
            print("Please, enter a positive number")
            continue
        else : 
            break

    #Sector question
    print('\nAmong the following sectors :\n')
    for s in sectors:
        print(' - ', s)
    print('\nIn which sector do you work/will you work ? Enter exact name ')
    while True:
        try:
            sec  =input('In which sector do you work/will you work ? Enter exact name ')
            if sec not in sectors:
                raise ValueError("Please,choose among the sectors listed")
        except ValueError:
            print("Please,choose among the sectors listed")
            continue
        else : 
            break


    agent_salary = simulate_salary(sec, exp, ed)

    print('')
    print('---------------------------------------------------------------------------')
    print('Thanks for the informations ! ')
    print('Today we are at time t = 0, you are %d years old'%(age))
    print('You will reach retirement at time t = %d when you will be %d years old!'%(65 - age, 65))
    print('---------------------------------------------------------------------------')
    print('')    
    print('---------------------------------------------------------------------------')
    print('1st Salary Simulation done: \nin one year, at t = 1, you will be paid CHF ', agent_salary)
    print('---------------------------------------------------------------------------')

    return age, agent_salary

def get_info_capital():
    
    while True :
        try:
            capital_q =str(input("Do you have a starting capital (Yes/No) ? "))
            if capital_q not in ('Yes','yes','No','no'):
                raise ValueError('Please, answer by Yes or No')
        except ValueError:
                print('Please, answer by Yes or No')
                continue
        else :
            break

    while True : 
        try:
            if capital_q in ('No','no'):
                capital_0 = 0
            if capital_q in ('Yes','yes'):
                capital_0 =float(input("How much is your starting capital ? "))
                if capital_0<0:
                    raise ValueError("Please, enter a positive number")
        except ValueError:
                print("Please, enter a positive number")
                continue
        else :
            break

    print('')
    print('---------------------------------------------------------------------------')
    print('Thanks again for the informations ! ')
    print('You start the game with an initial amount on your saving account of : CHF %d'%(capital_0))

    return capital_0

def first_simulation():
    print('')
    print('First Year Simulation (t = 0 -> t = 1')
    print('---------------------------------------------------------------------------')
    
    while True :
        try:
            frac_s = float(input('First things first, chose the fraction of salary you want to save \n(e.g. If you want to save 20% type 0.2) '))
            frac_c = float(input('Second, chose the fraction of salary you want to consume \n(e.g. If you want to save 20% type 0.2) '))
            if frac_s > 1 or frac_c > 1 or frac_s < 0 or frac_c < 0:
                raise ValueError
            if frac_s + frac_c > 1:
                raise ValueError
        except ValueError:
                print("Please, valid fraction between 0 and 1 (e.g. 0.1, 0.25, ...) \nYou can't consume and save more than what you warn (sum <= 1)")
                continue
        else :
            break
        
    while True : 
        try:
            go = input('Alright, are you ready to start playing with your life ? If yes type ok ')
            if not go == 'ok':
                raise ValueError("Please, enter a fraction between 0 and 1 (e.g. 0.1, 0.25, ...")
        except ValueError:
                print("To continue the game type ok")
                continue
        else :
            break 
    
    return frac_s, frac_c
    
####################TESTS######################

if __name__ == "__main__":
    
    #get_info_capital()        
    
    first_simulation()    
        
