import numpy as np


def create_price(mu = 0.2, sigma = 0.2, years = 1, lam = 1, m = -0.1, v = 0.1):
    """
    This function simulates the evolution of a stock price
    """
    days = 365
    N = years*days
    dt = 1/days
    zt_stock = np.random.normal(0, np.sqrt(dt), size = N)  # randomness of the stock price
    zt_jump = np.random.normal(m, v, size = N)  # randomness of the intensity and direction of the jump
    nt = np.random.poisson(lam * dt, size = N)  # randomness of jump occurence 

    return np.exp(np.cumsum((mu-sigma**2/2) * dt + sigma * zt_stock) + np.multiply(nt,zt_jump).cumsum(axis = 0) )

class Stock():

    def __init__(self, name, risk, description):
        self.name = name
        self.risk = risk
        self.description = description
        if risk == 'high':
            self.sigma = 0.4
        elif risk == 'medium':
            self.sigma = 0.2
        elif risk == 'low':
            self.sigma = 0.05
        elif risk == 'very_high':
            self.sigma = 0.7
        self.price = create_price(sigma = self.sigma)

    def info(self):
        print('Information of the stock :')
        print(f'name : {self.name}')
        print(f'risk : {self.risk}')
        print(f'volatility: {self.sigma}')
        print(f'description : {self.description}')