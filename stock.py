import numpy as np
import matplotlib.pyplot as plt
import pandas as pd


def create_price(mu, sigma, years, S0, lam, m, v):
    days = 365
    N = years*days
    dt = 1/days
    zt_stock = np.random.normal(0, np.sqrt(dt), size = N)  # randomness of the stock price
    zt_jump = np.random.normal(m, v, size = N)  # randomness of the intensity and direction of the jump
    nt = np.random.poisson(lam * dt, size = N)  # randomness of jump occurence 
    return S0 * np.exp(np.cumsum((mu-sigma**2/2) * dt + sigma * zt_stock)+ np.multiply(nt,zt_jump).cumsum(axis = 0) )

def run():
    price_A = create_price(0.1,0.2,20, 100, 1,0, 0.15)
    price_B = create_price(0.1,0.2,20, 100, 1,0, 0.15)
    price_C = create_price(0.1,0.2,20, 100, 1,0, 0.15)

    d = {'stockA' : price_A , 'stockB' : price_B, 'stockC' : price_C}
    df_price = pd.DataFrame(data = d)
    df_daily_ret = df_price.pct_change(1).fillna(0)

    df_daily_ret_cum = (df_daily_ret+1).cumprod().dropna(how='all')
    print('stocks available :', list(d.keys()))
    print('capital available :')
    list_input = input('write the stocks you wanna invest in, followed by the respective notional amount : ').split()
    list_stocks = [ list_input[i] for i in range(0,len(list_input),2) ]
    notional_stocks = np.array( [ int(list_input[i]) for i in range(1,len(list_input),2) ] )
    input_money = sum(notional_stocks)
    weight_stocks = notional_stocks/sum(notional_stocks)/input_money

    df_weight = pd.DataFrame(index = df_price.index, columns = list_stocks )
    for i,item in enumerate(list_stocks):
        df_weight[item] = weight_stocks[i]

    df_port = pd.DataFrame()
    df_port['total_return'] = (df_daily_ret[list_stocks]*df_weight).sum(axis = 1)
    df_port['portfolio'] = (df_port['total_return']).cumsum()+1

    tot_ret = (df_port.portfolio.iloc[-1]-df_port.portfolio.iloc[0])/df_port.portfolio.iloc[0]
    output_money = (1+tot_ret) * input_money
    delta_money = output_money - input_money
    if delta_money >= 0 :
        print('money made :', delta_money)
    else :
        print('money loss :', abs(delta_money))
    print('total return of the portfolio ', 100 * tot_ret , '%')
    print('equity capital at the end of the period : ', output_money)
    df_port['portfolio'].plot()

if __name__ == '__main__':
    run()