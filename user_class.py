# -*- coding: utf-8 -*-
"""
Created on Tue May  4 15:14:45 2021

@author: Antoine
"""

from account_class import Account
from interest_rates import rate_evolution_sample
from salary_class_2 import Salary

class user:
    
    def __init__(self, t_0, first_sal, first_cap):
        self.age = t_0 #The age at which user start working
        self.len_life = 65 - self.age #Number of periods user will simulate up to retirement
        self.first_sal = first_sal #The first salary he'll get
        self.first_cap = first_cap #The capital he'll start his working life with
        
        #Time pointer
        self.t = 0 #Initialized at 0 when starting
        
        #Call initialization functions:
        ##Bank stuffs:
        self.c_account, self.s_account, self.int_rates = self.init_bank()
        ##Salary stuffs:
        self.wages = self.init_job()
        
        
    def init_bank(self):
        """
        function initializing the user's bank stuffs (accounts, interests)
        """
        #Create user's accounts, say saving and current:
        ##First account will be current account starting with 0 capital:
        c_account = Account('Current', 0)
        ##Second account will be saving account starting with initial capital:
        s_account = Account('Saving', self.first_cap)
        ##Next we need to generate the interest rates user will face all over his life
        int_rates = rate_evolution_sample(N = self.len_life)
        
        return c_account, s_account, int_rates


    def init_job(self):
        """
        function initializing the user's job stuffs (salary evolutions, unemployment)
        """
        wages = Salary(self.first_sal, self.len_life)
        
        return wages
        
    def set_sav_dec(self):
        
        frac_saving = 0.5
        frac_consuming = 0.5
        
        return frac_saving, frac_consuming
    
    def report_single_sav_dec(self, sal_t, frac_sav, frac_cons):
        
        frac_sal_sav = frac_sav * sal_t #Part of the salary we want to save
        frac_sal_cons = frac_cons * sal_t #Part of the salary we use for consumption
        
        string_frac_sav = str(frac_sav * 100) + '%'
        
        info = 'You decided to save %s of your salary: CHF %d'%(string_frac_sav, frac_sal_sav)
        
        print('\n')
        print('------------------------------------------------------')
        print('----------------SAVING DECISIONS INFOS----------------')
        print('------------------------------------------------------')
        print('\n', info, '\n')
        print('------------------------------------------------------') 
        

    
    def run_single_cycle(self):
        
        frac_saving = 0.5
        frac_consuming = 0.5
        
        self.t += 1     

        
        sal_t = self.wages.wage_agenda[self.t]['Salary'] #Salary we get at time t
        growth_t = self.wages.wage_agenda[self.t]['Growth'] #Salary growth get at time t
        
        frac_sal_sav = frac_saving * sal_t #Part of the salary we want to save
        frac_sal_cons = frac_consuming * sal_t #Part of the salary we use for consumption
        
        #Print Salary Report      
        self.wages.salary_single_report(self.t)
        
        #Print Saving Decision Report
        self.report_single_sav_dec(sal_t, frac_saving, frac_consuming)
        
        #Print Bank Report & update accounts
        print('\n')
        print('------------------------------------------------------')
        print('--------------------ACCOUNTS INFOS--------------------')
        print('------------------------------------------------------')
      
        self.c_account.deposit(sal_t) #Salary deposit
        self.c_account.withdraw(frac_sal_cons) #Consumption
        self.c_account.transfer(self.s_account, frac_sal_sav) #Savings transfer
        self.c_account.yearly_adjustments(self.t, self.int_rates, disp=True)
        self.s_account.yearly_adjustments(self.t, self.int_rates, disp=True)




####################TESTS######################

if __name__ == "__main__":
   
    
    antoine = user(25, 90000, 20000)
    antoine.run_single_cycle()        
    antoine.wages.wage_agenda[1]
