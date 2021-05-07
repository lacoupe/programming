import numpy as np


def create_price(mu=0.2, sigma=0.2, years=1, lam=1, m=-0.1, v=0.1):
    """
    This function simulates the evolution of a stock price
    """
    days = 365
    N = years * days
    dt = 1 / days
    zt_stock = np.random.normal(0, np.sqrt(dt), size=N)  # randomness of the stock price
    zt_jump = np.random.normal(m, v, size=N)  # randomness of the intensity and direction of the jump
    nt = np.random.poisson(lam * dt, size=N)  # randomness of jump occurence

    return np.exp(np.cumsum((mu - sigma**2 / 2) * dt + sigma * zt_stock) + np.multiply(nt, zt_jump).cumsum(axis=0))


class Stock:

    def __init__(self, name, risk, description, number_years):
        self.name = name
        self.risk = risk
        self.description = description
        self.years = number_years

        if risk == 'very_high':
            self.mu = 0.3
            self.sigma = 0.6
            self.lam = 10
            self.m = 0
            self.v = 0.2
        elif risk == 'high':
            self.mu = 0.2
            self.sigma = 0.4
            self.lam = 2
            self.m = -0.1
            self.v = 0.1
        elif risk == 'medium':
            self.mu = 0.15
            self.sigma = 0.2
            self.lam = 1
            self.m = -0.05
            self.v = 0.1
        elif risk == 'low':
            self.mu = 0.1
            self.sigma = 0.05
            self.lam = 0.2
            self.m = 0
            self.v = 0.05
        
        self.price = create_price(mu=self.mu, sigma=self.sigma, years=self.years, lam=self.lam, m=self.m, v=self.v)

        self.d_price = create_price(mu=self.mu, sigma=self.sigma, years=self.years, lam=self.lam, m=self.m, v=self.v)
        self.y_price = []
        self.y_return = [0]

        for y in range(self.years):
            self.y_price.append(self.d_price[y * 365])
            if y == 0:
                continue
            else:
                last_y_price = self.y_price[y - 1]
                current_y_price = self.y_price[y]
                self.y_return.append((current_y_price / last_y_price) - 1)

    def info(self):
        print('Information of the stock :')
        print(f'name : {self.name}')
        print(f'risk : {self.risk}')
        print(f'volatility: {self.sigma}')
        print(f'description : {self.description}')
