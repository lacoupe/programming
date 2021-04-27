# %%

import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import datetime
from sys import exit
from stock_class import Stock


# def create_price(mu = 0.2, sigma = 0.2, years = 1, lam = 1, m = -0.1, v = 0.1):
#     """
#     This function simulates the evolution of a stock price
#     """
#     days = 365
#     N = years*days
#     dt = 1/days
#     zt_stock = np.random.normal(0, np.sqrt(dt), size = N)  # randomness of the stock price
#     zt_jump = np.random.normal(m, v, size = N)  # randomness of the intensity and direction of the jump
#     nt = np.random.poisson(lam * dt, size = N)  # randomness of jump occurence 

#     return np.exp(np.cumsum((mu-sigma**2/2) * dt + sigma * zt_stock) + np.multiply(nt,zt_jump).cumsum(axis = 0) )

# class Stock():

#     def __init__(self, name, risk, description):
#         self.name = name
#         self.risk = risk
#         self.description = description
#         if risk == 'high':
#             self.sigma = 0.4
#         elif risk == 'medium':
#             self.sigma = 0.2
#         elif risk == 'low':
#             self.sigma = 0.05
#         elif risk == 'very_high':
#             self.sigma = 0.7
#         self.price = create_price(sigma = self.sigma)

#     def info(self):
#         print('Information of the stock :')
#         print(f'name : {self.name}')
#         print(f'risk : {self.risk}')
#         print(f'volatility: {self.sigma}')
#         print(f'description : {self.description}')



def run():

    #######################################################################

    years = 1
    number_days = years * 365

    eatcoin_desc = 'best cryptocurrency'
    teslo_desc = 'electric car company'
    nestlo_desc = 'milk company'
    gold_desc = 'something that is precious'

    eatcoin = Stock('Gritecoin','very_high', eatcoin_desc)
    teslo = Stock('Teslo','high', teslo_desc)
    nestlo = Stock('Nestlo','medium', nestlo_desc)
    gold = Stock('Gold','low',gold_desc)
    

    today = datetime.datetime.today() # datetime simulation
    date_list = [today + datetime.timedelta(days=x) for x in range(number_days)] 
    d = {eatcoin.name : eatcoin.price , teslo.name : teslo.price, \
     nestlo.name : nestlo.price, gold.name : gold.price}
    df_price = pd.DataFrame(data = d, index = date_list)

    df_daily_ret = df_price.pct_change(1).fillna(0) # dataframe of the daily returns
    df_daily_ret_cum = 100*(df_daily_ret+1).cumprod().dropna(how='all')

    print('stocks available :', end = ' ')
    for stock_name in d.keys():
        if stock_name == list(d.keys())[-1]:
            print(stock_name)
        else :
            print(stock_name, end = ', ')

    capital = 10000
    print(f'capital available : ${capital}')

    #######################################################################

    ### input of the user

    list_input = []
    for i in range(len(d)):
        stock = input('stock name : ("ok" to end)')
        if stock == 'ok': # the user write "ok" if he does want to invest in more stocks
            break
        else:
            amount = input('amount of money :')
            capital = capital - int(amount)
            if capital <0:
                print('not enough cash')
                exit('il manque de la moula sur le compte')
            else :
                list_input.append(stock)
                list_input.append(amount)

            print(f'capital available : ${capital}')
    print(list_input)

    # list_input = ['Gold', '5000', 'Eatcoin', '5000'] # pre_list for practice without typing input

    #######################################################################

    list_stocks = [ list_input[i] for i in range(0,len(list_input),2) ]
    notional_stocks = np.array( [ int(list_input[i]) for i in range(1,len(list_input),2) ] )
    input_money = sum(notional_stocks)
    weight_stocks = notional_stocks/input_money

    df_weights = pd.DataFrame(index = df_price.index, columns = list_stocks )
    for i,item in enumerate(list_stocks):
        df_weights[item] = weight_stocks[i]

    df_port = pd.DataFrame()
    df_port['total_return'] = (df_daily_ret[list_stocks]*df_weights).sum(axis = 1)
    df_port['portfolio'] = input_money*((df_port['total_return']).cumsum()+1)

    #######################################################################

    tot_ret = (df_port.portfolio.iloc[-1]-df_port.portfolio.iloc[0])/df_port.portfolio.iloc[0]
    output_money = (1+tot_ret) * input_money
    delta_money = output_money - input_money

    #######################################################################

    for name,amount in zip(list_stocks,notional_stocks):
        print(f'money invested in {name} : ${amount}')
    print('total money invested : ${}'.format(input_money))
    if delta_money >= 0 :
        print('money made : $%.2f' % delta_money)
    else :
        print('money loss : $%.2f' % abs(delta_money))
    print('total return of the portfolio : %.2f%% ' % (100 * tot_ret) )
    print(f'portfolio value at the end of {years} years : $%.2f' % output_money) 

    #######################################################################

    df_port['portfolio'].plot()
    plt.title('portfolio evolution')
    plt.show()
    df_daily_ret_cum[list_stocks].plot()
    plt.title('price evolution of the underlying stocks')
    plt.show()


if __name__ == '__main__':
    run()

# %%
