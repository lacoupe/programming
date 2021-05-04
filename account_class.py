# -*- coding: utf-8 -*-
"""
Created on Mon Apr 19 15:09:40 2021

@author: Antoine
"""

from interest_rates import rate_evolution_sample


class Account:
    
    def __init__(self,name,initial_amount):
        self.name = name #Name/Type of the account : Current Account, Saving Account, ...
        self.balance_t = initial_amount #Initial amount you start simulation with at t = 0
        self.first_balance = initial_amount #Initial amount you start simulation with at t = 0
        self.last_balance_t = initial_amount #Last simulation step balance (at t-dt)
        
        self.net_movements_t = 0 #making the sum of + & - transfers where account is concerned
        
    
    def yearly_adjustments(self, t, rates):
        
        if t==0:
            return
        
        if self.name == 'Saving':
            
            print('SAVING ACCOUNT:')
            
            int_rate = rates[t-1]
            int_payment = self.last_balance_t*int_rate  #Yearly interest rates payment based on last year balance
            print('Interests received/paid on last year (t = {} to t = {}) : CHF {}'.format(t-1, t, int_payment))
    
            net_mov = self.net_movements_t #Net yearly withdrawals, deposits, transfers need to adjust
            print('Net movements on last year (t = {} to t = {}) : CHF {}'.format(t-1, t, net_mov))
            
            #adjust balance for interests and movements:
            self.balance_t += (int_payment + net_mov)
            
            print('Last year (t = {}) balance was : CHF {} \nThis year ( t= {}) balance is : CHF {}'.format(t-1, self.last_balance_t, t, self.balance_t))
        
        elif self.name == 'Current':
            
            print('CURRENT ACCOUNT:')
            
            net_mov = self.net_movements_t #Net yearly withdrawals, deposits, transfers need to adjust
            print('Net movements on last year (t = {} to t = {}) : CHF {}'.format(t-1, t, net_mov))
            
            #adjust balance for interests and movements:
            self.balance_t += net_mov
            
            print('Last year (t = {}) balance was : CHF {} \nThis year ( t= {}) balance is : CHF {}'.format(t-1, self.last_balance_t, t, self.balance_t))

            
        
        #Reset movements balance to zero for the new coming year
        self.net_movements_t = 0 
        
        #Store new current balance as last balance for next period computations
        self.last_balance_t = self.balance_t
        
     
        
    def deposit(self, amount):
        self.net_movements_t += amount
            
    def withdraw(self, amount):
        self.net_movements_t -= amount
            
    def info(self):
        s = "Account name : %s \nBalance : %s" % (self.name, self.balance_t)
        print(s)
    
    def transfer(self, other, amount):
        self.withdraw(amount)
        other.deposit(amount)


################TEST######################

if __name__ == "__main__":

    test_rates = rate_evolution_sample()
    
    print(test_rates[0:2])    
    
    a1 = Account('Current', 20000)
    a2 = Account('Spare', 20000)
    
    a1.info()
    a2.info()
    
    
    #at t=1 : (1) withdraw 100 and deposit 200 -> Net = +100
    a1.withdraw(100)
    a1.deposit(200)
    
    a1.yearly_adjustments(1, test_rates)
    a2.yearly_adjustments(1, test_rates)
    
    
    #at t=2 : (1) transfers 300 ton (2) and withdraw 200 --> Net = -500 AND a2 deposit 100 --> Net = +400
    a1.withdraw(200)
    a1.transfer(a2,300)
    a2.deposit(100)
    
    a1.yearly_adjustments(2, test_rates)
    a2.yearly_adjustments(2, test_rates)

