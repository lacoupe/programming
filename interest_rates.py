# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 15:29:27 2021

@author: Antoine
"""

from math import sqrt
import numpy as np
import matplotlib.pyplot as plt

def next_rate(rt, k, theta, sigma, dt = 1 ):
    
    e = np.random.normal()
    
    delta_rt = k*(theta-rt)*dt+sigma*sqrt(dt)*e
    
    return rt + delta_rt


def rate_evolution_sample(r0 = 0.001, k = 0.2, theta = 0.045, sigma = 0.01, dt = 1, N = 65):

    """
    VARSICEK MODEL (c.f. https://yilifinhub.com/interest-rate-vasicek-model-simulation/)

    Parameters
    ----------
    r0 : float
        1-year current interest rate at time t = 0, r(0)
    k : float
        Speed of long-run interest rate mean convergence.
    theta :  float
        Actual long-run interest rate mean --> (RANDOM OR NOT ?).
    sigma : float
        Interest rate volatility around long-run mean (variability)--> (RANDOM OR NOT ?).
    dt : int
        Time delta, default : 1 year
    N : int
        Number of sample points we want to create, default : 65 years

    Returns
    -------
    List of simulated 1-year interest rate evolution sample over N year : [r(0), r(1), ..., r(N)]
    Plot of the evolution

    """
    
    rates = []
    
    for i in range(N):
                
        if i == 0:
            last_r = r0
        else:
            last_r = rates[i-1]
            
        rdt = next_rate(last_r, k, theta, sigma)
        
        rates.append(rdt)
    
    plt.plot(rates)
    return rates

if __name__ == "__main__":
    
    rate_evolution_sample()
