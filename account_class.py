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
        
        self.hist = {} #Dictionary which will keep history of the account
        
        if self.name == 'Saving':
            self.hist[0] = {'last_balance':0, 'int_rate':0, 'int_payment':0, 'net_mov':0, 'balance': initial_amount }
        elif self.name == 'Current':
            self.hist[0] = {'last_balance':0, 'int_rate':0, 'int_payment':0, 'net_mov':0, 'balance': 0 }

    def yearly_adjustments(self, t, rates, disp = True):
        
        if t==0:
            return
        
        if self.name == 'Saving':
                        
            int_rate = rates[t-1]
            fut_int_rate = rates[t]
            int_payment = self.last_balance_t*int_rate  #Yearly interest rates payment based on last year balance
    
            net_mov = self.net_movements_t #Net yearly withdrawals, deposits, transfers need to adjust
            
            #adjust balance for interests and movements:
            self.balance_t += (int_payment + net_mov)
            
            #Report
            if disp: self.single_report(t, net_mov, int_rate, int_payment, fut_int_rate)
            
            #store data    
            self.hist[t] = {'last_balance':self.last_balance_t,
                            'int_rate': int_rate,
                            'int_payment': int_payment,
                            'net_mov': net_mov, 
                            'balance': self.balance_t }

            
            
        elif self.name == 'Current':
                        
            net_mov = self.net_movements_t #Net yearly withdrawals, deposits, transfers need to adjust
            
            #adjust balance for interests and movements:
            self.balance_t += net_mov
            
            #Report
            if disp: self.single_report(t, net_mov)
            
            #store data    
            self.hist[t] = {'last_balance':self.last_balance_t,
                            'int_rate': 0,
                            'int_payment': 0,
                            'net_mov': net_mov, 
                            'balance': self.balance_t }


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
        
        

    def single_report(self, t, net_mov,int_rate = 0, int_payment = 0, fut_int_rate = 0):
        """
        When called, this function generates a report about all informations about the accounts e.g. :
            - Last year balance
            - Interests (Only for saving account)
            - Net Movements (Deposit-Withdrawals)
            - Current Balance
        """
        
        
        if self.name == 'Saving':
            print('')
            print('SAVING ACCOUNT:')
            print('------------------------------------------------------')
            print('Last year (t = {}) balance was : CHF {}'.format(t-1, round(self.last_balance_t)))
            print('Interest rate was : {}%'.format(round(int_rate*100, 4)))
            print('Interests received/paid on last year : CHF {}'.format(round(int_payment)))
            print('Net movements on last year : CHF {}'.format(net_mov))
            print('This year (t= {}) balance is : CHF {}'.format(t, round(self.balance_t)))
            print('')
            print('------------------------------------------------------')
            print('Interest rates for this coming year is: {}%'.format(round(fut_int_rate*100, 4)))
            print('------------------------------------------------------')

        
        elif self.name == 'Current':
            print('')
            print('CURRENT ACCOUNT:')
            print('------------------------------------------------------')
            print('Last year (t = {}) balance was : CHF {}'.format(t-1, round(self.last_balance_t)))
            print('Net movements on last year : CHF {}'.format(net_mov))
            print('This year (t= {}) balance is : CHF {}'.format(t, self.balance_t))

        
        
    def compute_account_report(self, beg, end):
        
        timeline = range(beg, end + 1)
        if self.name =='Saving':
            title = 'SAVING ACCCOUNT REPORT'
        elif self.name == 'Current':
            title = 'CURRENT ACCOUNT REPORT'
        
        
        
        print(80*'-')
        print(80*'-')
        print("{:<30}{:<20}{:<30}".format(' ',title,' '))
        print(80*'-')
        print(80*'-')
        print("{:<5}{:<15}{:<15}{:<15}{:<15}{:<15}".format('Year','Last Balance','Int. Rate', 'Int. Payment', 'Net Movements', 'Current Balance'))
        print(80*'-')
        
        
        for t in timeline :
            
            l_bal = round(self.hist[t]['last_balance'],2)
            i_rate = str(round(self.hist[t]['int_rate']*100, 3)) + ' %'
            i_pay = round(self.hist[t]['int_payment'], 2)
            net_mov = round(self.hist[t]['net_mov'], 2)
            c_bal = round(self.hist[t]['balance'], 2)
            
            print("{:<5}{:<15}{:<15}{:<15}{:<15}{:<15}".format(t, l_bal, i_rate, i_pay, net_mov, c_bal))
        
        print(80*'-')
        print(80*'-')

    
    def transfer(self, other, amount):
        self.withdraw(amount)
        other.deposit(amount)


################TEST######################

if __name__ == "__main__":

    test_rates = rate_evolution_sample()
    
    print(test_rates[0:2])    
    
    a1 = Account('Current', 20000)
    a2 = Account('Saving', 20000)
    
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

    a2.hist
    a2.compute_account_report(0,1)
