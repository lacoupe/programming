

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
import sys
from sys import exit
from stock_class import Stock


def stock_simulation():

    ### DATA

    number_years = 1

    eatcoin_desc = 'best cryptocurrency'
    teslo_desc = 'electric car company'
    nestlo_desc = 'milk company'
    gold_desc = 'something that is precious'

    eatcoin = Stock('Eatcoin','very_high', eatcoin_desc, number_years)
    teslo = Stock('Teslo','high', teslo_desc, number_years)
    nestlo = Stock('Nestlo','medium', nestlo_desc, number_years)
    gold = Stock('Gold','low',gold_desc, number_years)
    
    number_days = number_years * 365
    today = datetime.datetime.today() # datetime simulation
    date_list = [today + datetime.timedelta(days=x) for x in range(number_days)] 
    d = {eatcoin.name : eatcoin.price , teslo.name : teslo.price, \
     nestlo.name : nestlo.price, gold.name : gold.price}
    df_price = pd.DataFrame(data = d, index = date_list)

    df_daily_ret = df_price.pct_change(1).fillna(0) # dataframe of the daily returns
    df_daily_ret_cum = 100*(df_daily_ret+1).cumprod().dropna(how='all')

    #######################################################################

    ### INPUT COMMAND

    list_stocks = []
    notional_stocks = []
    temp_list = list(d.keys())
    capital = 10000
    print( 'BIENVENIDO AL JUEGO DE LA BOLSA! Try not to loose money :) ')
    while True:
        print('stocks available :', end = ' ')
        for stock_name in temp_list:
            if stock_name == temp_list[-1]:
                print(stock_name)
            else :
                print(stock_name, end = ', ')   
        print(f'capital available : ${capital}')
        try:
            stock = str(input('stock name : ("ok" to end) '))
            if stock == 'ok': # the user write "ok" if he does not want to invest more
                print('*' * 50)
                break
            if stock not in list(d.keys()):
                raise ValueError
        except ValueError:
            print('Enter a valid stock name :')
            continue

        while True:
            try:
                amount = int(input('amount of money : '))
                if amount <= 0:
                    raise ValueError
                if capital < amount:
                    raise ValueError
            except ValueError:
                if amount <= 0:
                    print('Enter a positive amount, short selling not allowed')
                    continue
                elif capital < amount:
                    print('You have not enough cash')
                    continue
                else:
                    print('Enter a valid number')
                
            else:
                list_stocks.append(stock)
                notional_stocks.append(amount)
                capital = capital - amount            
                temp_list.remove(stock)  
                break
        if capital == 0:
            print('*' * 50)
            break
        

    # notional_stocks = [5000,5000]
    # list_stocks = ['Gold','Eatcoin']
    

    #######################################################################

    ### PORTFOLIO

    notional_stocks = np.array(notional_stocks)
    input_money = sum(notional_stocks)
    weight_stocks = notional_stocks/input_money

    df_weights = pd.DataFrame(index = df_price.index, columns = list_stocks )
    for i,item in enumerate(list_stocks):
        df_weights[item] = weight_stocks[i]

    df_port = pd.DataFrame()
    df_port['total_return'] = (df_daily_ret[list_stocks]*df_weights).sum(axis = 1)
    df_port['portfolio'] = input_money*((df_port['total_return']+1).cumprod())

    tot_ret = (df_port.portfolio.iloc[-1]-df_port.portfolio.iloc[0])/df_port.portfolio.iloc[0]
    output_money = (1+tot_ret) * input_money
    delta_money = output_money - input_money

    #######################################################################

    ### PRINT OUTPUT

    for name,amount in zip(list_stocks,notional_stocks):
        print(f'money invested in {name} : ${amount}')
    print('total money invested : ${}'.format(input_money))
    if delta_money >= 0 :
        print('money made : $%.2f' % delta_money)
    else :
        print('money loss : $%.2f' % abs(delta_money))
    print('total return of the portfolio : %.2f%% ' % (100 * tot_ret) )
    print(f'portfolio value at the end of {number_years} years : $%.2f' % output_money) 

    #######################################################################

    ### PLOT OUTPUT

    df_port['portfolio'].plot()
    plt.title('portfolio evolution')
    plt.show()
    df_daily_ret_cum[list_stocks].plot()
    plt.title('price evolution of the underlying stocks')
    plt.show()


if __name__ == '__main__':
    stock_simulation()
