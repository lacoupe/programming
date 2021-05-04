# -*- coding: utf-8 -*-
"""
Created on Tue Apr 20 13:42:16 2021

@author: Antoine
"""

from scipy.stats import skewnorm
import numpy as np
from random import choice
import matplotlib.pyplot as plt



def wage_growth_sample(skew_param =1, avg = 0.009, std = 0.01, N = 65):

    """
    Assumption of a pretty much linear wage evolution overs life
    Inclusion of some noise around the mean evolution rate using a Normal distribution around average rate
    Inclusion of some asymetry to allow more positive mean deviations than negative one (skew = 1)
    Assume a yearly average nominal wage growth rate of 0.9% (mean)
    Assume a std of 0.1% to allow some important gaps.
    
    """
    
    w_growths = skewnorm.rvs(skew_param, loc=0.009, scale=0.03, size=N)
    w_growths = np.round(w_growths,4)
    
    plt.plot(w_growths)
    plt.show()
    plt.hist(w_growths, density=True, bins=30)
    plt.show()
    
    return w_growths

def nb_ue_p():
    """
    Function creating a probability distribution to return the number of unemployment periods 
    the user will face (returns only the number, not the lenght of each period) :
        
        P(nb=0)=50%
        P(nb=1)=40%
        P(nb=2)=9%
        P(nb=3)=1%
    """
    
    x = np.random.uniform()

    if x >= 0.5:
        nb_p = 0 # User will never have unemployment time in his life (proba = 50%)
    elif x >= 0.1:
        nb_p = 1 # User will have 1 unemployment time in his life (proba = 40%)
    elif x >= 0.01:
        nb_p = 2 # User will have 2 unemployment times in his life (proba = 9%)
    else:
        nb_p = 3 # User will have 3 unemployment times in his life (proba = 1%)

    print('Number of unemployment periods user will face : ', nb_p)
    return nb_p    

    
def len_ue_p(nb_p):
    """
    Function creating a probability distribution to return the lenght of each unemployment periods 
    the user will face (returns only the lenght, not the lenght of each period) :
        
        P(lenght=1)=70%
        P(lenght=2)=20%
        P(lenght=3)=10%
    """
    len_list = []
    
    if nb_p == 0: #If no unemployment periods no need to compute lenght
        return
    
    for i in range(nb_p):
        
        y = np.random.uniform()
    
        if y >= 0.7:
            len_p = 1 # Pointed unemployment period will lenght for 1 year (proba = 70%)
        elif y >= 0.2:
            len_p = 2 # Pointed unemployment period will lenght for 2 years (proba = 20%)
        else:
            len_p = 3 # Pointed unemployment period will lenght for 3 years (proba = 10%)
            
        len_list.append(len_p)
        
        print('Lenght of unemployment period number {} is {} years'.format(i+1,len_p))

    return len_list


def agenda_ue_p(nb_p, len_p, N):

    """
    This function allows to allocate dates  to all of the unemployments periods given 3 parameters:
        -nb_p : Number of unemployment periods user will face
        -len_p : List of the len of all unemployment periods user will face
        -N : number of periods 
        
    The function takes care that every date is set randomnly but has to follow few rules:
        -Two unemployments periods can't happen in same time
        -An unemployment period is set s.t. ther's still time for others
        -Minimum period of time between two unemployment periods is 1 year
    """    

    agenda = []
    
    if nb_p == 0:
        return    
    
    for i in range(nb_p):
        
        rem_len = sum(len_p[i+1:]) #total lenght of unemployment remaining after period i
        rem_nb = max(nb_p - (i+1), 0) #number of periods of ue remaining after period i
        
        if i == 0 :
            temp_start = 1 #First period of unemployment can happend at t=1
        else:
            temp_start = agenda[i-1] + len_p[i-1] + 1 #An ue period cannot follow directly previous one (min 1 year break)
        
        temp_end = N - len_p[i] - rem_len - max(rem_nb -1, 0) #An ue period needs to happen s.t. remaining periods can still happen
        
        temp_t_line = range(temp_start,temp_end + 1) #Possible dates for the ith ue period
        
        date = choice(temp_t_line) #Random choice over possible dates 
        
        agenda.append(date) #Create agenda with all dates
        
    return agenda




def gen_ue_agenda(N=65):
    """
    Function calling all functions we need to generate final unemployment agenda in the form of
    
    - a dict:
        
        {(date_1) = len_1, (date_2) = len_2, ...}
        
    - a list:
        
        [date_1.1, date_1.2, ... ]
    """
    agenda_dict = {}
    agenda_list = []
    
    nb_p = nb_ue_p()
    
    if nb_p == 0:
        return agenda_dict, agenda_list
    
    len_p = len_ue_p(nb_p)
    agenda = agenda_ue_p(nb_p, len_p, N)
    
    #Generate dict.
    for i in range(nb_p):
        agenda_dict[agenda[i]] = len_p[i]
   
    #Generate list
    for i in range(nb_p):
        temp_len = len_p[i]
        for j in range(temp_len):
            date = agenda[i] + j
            agenda_list.append(date)
   
    return agenda_dict, agenda_list



####################TESTS######################

if __name__ == "__main__":

    #Wage growth sample
    print(wage_growth_sample())
    
    #Unemployment
    nb_test = nb_ue_p()
    len_test = len_ue_p(nb_test)
    agenda_test = agenda_ue_p(nb_test, len_test, N=65)
    print(agenda_test)
    
    print(gen_ue_agenda())

