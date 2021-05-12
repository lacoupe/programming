# -*- coding: utf-8 -*-
"""
Created on Tue Apr 27 19:59:26 2021

@author: diego
"""

import numpy as np
import random





while True :
    try:
        play_type =str(input("Do you want to bet on a color or a number ? "))
        if play_type not in ('color','Color','number','Number'):
            raise ValueError('Please, answer by "color" or "number"')
    except ValueError:
            print('Please, answer by "color" or "number"')
            continue
    else :
        break

while True :
    try:
        amount_played =float(input("How much do you want to bet for this game ? "))
        if amount_played <=0:
            raise ValueError('Please, enter a positive amount"')
    except ValueError:
            print('Please, enter a positive amount"')
            continue
    else :
        break
    
if play_type.lower()== 'color' :
    while True :
        try:
            color_choice = str(input("In which color do you want to bet (Red or Black) ? "))
            if color_choice.lower() not in ('black','red'):
                raise ValueError('Please, enter "black" or "red" as input')
        except ValueError:
                print('Please, enter "black" or "red" as input')
                continue
        else:
            break
else :
    while True :
        try:
            number_choice = int(input("In which number do you want to bet (0-36) ? "))
            if number_choice not in list(np.arange(0,37)):
                raise ValueError('Please, a number between 0 and 36')
        except ValueError:
                print('Please, a number between 0 and 36')
                continue
        else:
            break
    
    


class Roulette :

    def __init__(self,play_type,amount_played,**kwargs):
        self.play_type = play_type
        self.amount_played = amount_played
        self.color = kwargs.get('color',None)
        self.number = kwargs.get('number',None)
        
        
        
        
    def roulette_game(self,play_type,amount_played,**kwargs):
        
        """
        
        
        """
        
        green = 0
        red = list(np.arange(1,19))
        black = list(np.arange(19,37))
        color = kwargs.get('color', None)
        number = kwargs.get('number', None)
        if play_type.lower()=='color':
            n = random.randint(0,36)
            if n in red :
                color_roulette = 'red'
            elif n in black:
                color_roulette = 'black'
            else:
                color_roulette = 'green'
            if color_roulette == color:
                amount_gained = 2*amount_played
                print('You are lucky ! {} color came out'.format(color))
                print('You have won %d !'%amount_gained)
            elif color_roulette == 'green':
                amount_gained = 0
                print('Wow... bery bad luck... the 0 has came out')
                print('You have lost your entire bet')
            else:
                amount_gained = 0
                print('Sorry,{} color came out'.format(color_roulette))
                print('You have lost your entire bet')
            
        if play_type.lower()=='number':
            n = random.randint(0,36)
            if n == number:
                amount_gained = amount_played * 36
                print('Wow ! %d has came out !'%number)
                print('You have won %d'%amount_gained)
            else: 
                amount_gained = 0
                print('Bad luck... %d has came out'%n)
                print('You have lost your entire bet')
        
        return amount_gained


if play_type.lower()=='color':
    a = Roulette(play_type.lower(),amount_played,color = color_choice)
    a.roulette_game(play_type, amount_played, color = color_choice)
else:
    b = Roulette(play_type.lower(),amount_played,number = number_choice)
    b.roulette_game(play_type, amount_played, number = number_choice)

    

