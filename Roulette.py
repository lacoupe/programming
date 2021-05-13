# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 19:59:26 2021

@author: diego
"""

import numpy as np
import random



def roulette_game_intro(max_amt):
    
    if max_amt == 0:
        print("You don't have any cash on your current account ... come back later !")
        return 0, 0

    while True :
        try:
            play_type = str(input("Do you want to bet on a color or a number ? color/number  "))
            if play_type not in ('color','Color','number','Number'):
                raise ValueError
        except ValueError:
                print('Please, answer by "color" or "number"')
                continue
        else :
            break
    
    while True :
        try:
            amount_played =float(input("How much do you want to bet for this game ? "))
            if amount_played <=0 or amount_played > max_amt:
                raise ValueError
        except ValueError:
                print('Please, enter a positive amount available on your current account (CHF %d)'%(max_amt))
                continue
        else :
            break
        
    if play_type.lower()== 'color' :
        while True :
            try:
                color_choice = str(input("In which color do you want to bet (Red or Black) ? "))
                if color_choice.lower() not in ('black','red'):
                    raise ValueError
            except ValueError:
                    print('Please, enter "black" or "red" as input')
                    continue
            else:
                break
        
        return roulette_game(play_type, amount_played, color = color_choice)
    
    else :
        while True :
            try:
                number_choice = int(input("In which number do you want to bet (0-36) ? "))
                if number_choice not in list(np.arange(0,37)):
                    raise ValueError
            except ValueError:
                    print('Please, enter a number between 0 and 36')
                    continue
            else:
                break
            
        return roulette_game(play_type, amount_played, number = number_choice)
    
    

def roulette_game(play_type,amount_played,**kwargs):
    
    green = 0
    red = list(np.arange(1,19))
    black = list(np.arange(19,37))
    color = kwargs.get('color', None)
    number = kwargs.get('number', None)
    n = random.randint(0,36)

    if play_type.lower()=='color':
        if n in red :
            color_roulette = 'red'
        elif n in black:
            color_roulette = 'black'
        else:
            color_roulette = 'green'
        if color_roulette == color:
            amount_gained = 2*amount_played
            print('------------------------------------------------------')
            print('You are lucky ! {} color came out'.format(color))
            print('You have won %d !'%amount_gained)
            print('------------------------------------------------------')
        elif color_roulette == 'green':
            amount_gained = 0
            print('------------------------------------------------------')
            print('Wow... bery bad luck... the 0 has came out')
            print('You have lost your entire bet')
            print('------------------------------------------------------')
        else:
            amount_gained = 0
            print('------------------------------------------------------')
            print('Sorry,{} color came out'.format(color_roulette))
            print('You have lost your entire bet')
            print('------------------------------------------------------')
        
    if play_type.lower()=='number':
        if n == number:
            amount_gained = amount_played * 36
            print('------------------------------------------------------')
            print('Wow ! %d has came out !'%number)
            print('You have won %d'%amount_gained)
            print('------------------------------------------------------')
        else: 
            amount_gained = 0
            print('------------------------------------------------------')
            print('Bad luck... %d has came out'%n)
            print('You have lost your entire bet')
            print('------------------------------------------------------')
    
    return amount_played, amount_gained

####################TESTS######################

if __name__ == "__main__":

    roulette_game_intro(100)




