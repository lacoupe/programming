

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from stock_class import Stock


def stock_simulation():

    # DATA

    number_years = 1

    eatcoin_desc = 'best cryptocurrency'
    teslo_desc = 'electric car company'
    nestlo_desc = 'milk company'
    gold_desc = 'something that is precious'

    eatcoin = Stock('Eatcoin', 'very_high', eatcoin_desc, number_years)
    teslo = Stock('Teslo', 'high', teslo_desc, number_years)
    nestlo = Stock('Nestlo', 'medium', nestlo_desc, number_years)
    gold = Stock('Gold', 'low', gold_desc, number_years)
    
    number_days = number_years * 365
    today = datetime.datetime.today()  # datetime simulation
    date_list = [today + datetime.timedelta(days=x) for x in range(number_days)]
    d_price = {eatcoin.name: eatcoin.price, teslo.name: teslo.price,
               nestlo.name: nestlo.price, gold.name: gold.price}
    df_price = pd.DataFrame(data=d_price, index=date_list)

    d_desc = {eatcoin.name: eatcoin.description, teslo.name: teslo.description,
              nestlo.name: nestlo.description, gold.name: gold.description}

    df_daily_ret = df_price.pct_change(1).fillna(0)  # dataframe of the daily returns
    df_daily_ret_cum = 100 * (df_daily_ret + 1).cumprod().dropna(how='all')

    #######################################################################

    # INPUT COMMAND
    
    temp_list = list(d_price.keys())

    print('\n' + '*' * 60 + '\n' + 'BIENVENIDO AL JUEGO DE LA BOLSA! Try not to loose money :) ')
    print('The stocks available in this simulation are :', end=' ')
    for stock_name in temp_list:
        if stock_name == temp_list[-1]:
            print(stock_name)
        else:
            print(stock_name, end=', ')
    i = 0
    while True:
        try:
            if i == 0:
                choice = str(input('Do you want an info on a particular stock ? (yes/no) '))
            else:
                choice = str(input('Do you want another info on another particular stock ? (yes/no) '))
            if choice not in ('yes', 'no'):
                raise ValueError
            if choice == 'yes':
                stock_name = str(input('On which particular stock? : '))
                print(d_desc[stock_name])
                i += 1
                continue
            if choice == 'no':
                break
        except ValueError:
            print('Enter "yes" or "no" with no capital letter ')
            continue

    list_stocks = []
    notional_stocks = []
    temp_list = list(d_price.keys())
    capital = 10000
    
    while True:
        print('stocks available :', end=' ')
        for stock_name in temp_list:
            if stock_name == temp_list[-1]:
                print(stock_name)
            else:
                print(stock_name, end=', ')
        print(f'capital available : ${capital}')
        try:
            stock = str(input('stock name : ("ok" to end) '))
            if stock == 'ok':  # the user write "ok" if he does not want to invest more
                print('*' * 50)
                break
            if stock not in temp_list:
                raise ValueError
        except ValueError:
            print('ERROR! Enter a valid stock name :')
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
                    print('ERROR! Enter a positive amount, short selling not allowed')
                    continue
                elif capital < amount:
                    print('ERROR! You have not enough cash')
                    continue
                else:
                    print('ERROR! Enter a valid number')
                
            else:
                list_stocks.append(stock)
                notional_stocks.append(amount)
                capital = capital - amount
                temp_list.remove(stock)
                break
        if capital == 0:
            print('*' * 50)
            break
    
    #######################################################################

    # PORTFOLIO

    notional_stocks = np.array(notional_stocks)
    input_money = sum(notional_stocks)
    weight_stocks = notional_stocks / input_money

    df_weights = pd.DataFrame(index=df_price.index, columns=list_stocks)
    for i, item in enumerate(list_stocks):
        df_weights[item] = weight_stocks[i]

    df_port = pd.DataFrame()
    df_port['total_return'] = (df_daily_ret[list_stocks] * df_weights).sum(axis=1)
    df_port['portfolio'] = input_money * ((df_port['total_return'] + 1).cumprod())

    tot_ret = (df_port.portfolio.iloc[-1] - df_port.portfolio.iloc[0]) / df_port.portfolio.iloc[0]
    output_money = (1 + tot_ret) * input_money
    delta_money = output_money - input_money

    #######################################################################

    # PRINT OUTPUT

    for name, amount in zip(list_stocks, notional_stocks):
        print(f'money invested in {name} : ${amount}')
    print('total money invested : ${}'.format(input_money))
    if delta_money >= 0:
        print('money made : $%.2f' % delta_money)
    else :
        print('money loss : $%.2f' % abs(delta_money))
    print('total return of the portfolio : %.2f%% ' % (100 * tot_ret))
    print(f'portfolio value at the end of {number_years} years : $%.2f' % output_money)

    #######################################################################

    # PLOT OUTPUT

    df_port['portfolio'].plot()
    plt.title('portfolio evolution')
    plt.show()
    df_daily_ret_cum[list_stocks].plot()
    plt.title('price evolution of the underlying stocks')
    plt.show()


if __name__ == '__main__':
    stock_simulation()

# %%
