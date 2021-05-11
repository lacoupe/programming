# -*- coding: utf-8 -*-
"""
Created on Tue May  4 15:14:45 2021

@author: Antoine
"""

from account_class import Account
from interest_rates import rate_evolution_sample
from salary_class_2 import Salary
from investment_class import Investment

class user:

    ###############INITIALISATION FUNCTIONS###############

    
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
        ##Stocks stuffs
        self.e_inv, self.t_inv, self.n_inv, self.g_inv  = self.init_stocks()
     
    def init_stocks(self):
        """
        function initializing the stocks available to user and their processes
        """
        
        n = self.len_life
        
        e_inv =  Investment('Eatcoin', n)
        t_inv = Investment('Teslo', n)
        n_inv = Investment('Nestlo', n)
        g_inv = Investment('Gold', n)
        
        return e_inv, t_inv, n_inv, g_inv
        
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


    ###################CYCLES FUNCTIONS###################

    
    def run_single_cycle(self, frac_saving = 0.5, frac_consuming = 0.5):
        """
        This function is here to run a single cycle (User want to simulate one year only)
        Calls all needed classes methods to update salary, accounts, ...
        Create some single periods reports
        """
        
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
        
        #BANK STUFFS
        #Print Bank Report & update accounts
        print('\n')
        print('------------------------------------------------------')
        print('--------------------ACCOUNTS INFOS--------------------')
        print('------------------------------------------------------')
      
        self.c_account.deposit(sal_t) #Salary deposit
        self.c_account.withdraw(frac_sal_cons) #Consumption
        self.c_account.transfer(self.s_account, frac_sal_sav) #Savings transfer
        self.c_account.yearly_adjustments(self.t, self.int_rates, disp=True) #Current Account Updates and report
        self.s_account.yearly_adjustments(self.t, self.int_rates, disp=True) #Saving Account Updates and report
        
        #INVESTMENTS STUFFS
        #For each asset, update invest. value by P&L, print report
        for asset in [self.e_inv, self.t_inv, self.n_inv, self.g_inv]:
            asset.single_year_adj_1(self.t)
        #Ask for possible new investments/sales depending on performance we display
        self.long_invest_decision() #Long transactions 
        self.short_invest_decision() #Short transactions
        #Update investments depending on new transactions
        for asset in [self.e_inv, self.t_inv, self.n_inv, self.g_inv]:
            asset.single_year_adj_2(self.t)

    def run_cycle(self, n, frac_sav, frac_cons):
        """
        This function is here to run multiple cycle (User want to simulate multiple years)
        Calls all needed classes methods to update salary, accounts, ...
        Create some multiple periods reports
        """
        
        beg = self.t + 1 #First period to update
        end = beg + n - 1 #Last period to update
        
        #Print Salary Report      
        self.wages.compute_salary_report(beg, end)
        
        #Print Saving Decision Report
        self.report_multiple_sav_dec(n, frac_sav, frac_cons)
        
        for p in range(n): #Make n period updates 
        
            self.t += 1 # Update time pointer
    
            sal_t = self.wages.wage_agenda[self.t]['Salary'] #Salary we get at time t
            growth_t = self.wages.wage_agenda[self.t]['Growth'] #Salary growth get at time t
            
            frac_sal_sav = frac_sav * sal_t #Part of the salary we want to save
            frac_sal_cons = frac_cons * sal_t #Part of the salary we use for consumption
            
            #BANK STUFFS
            self.c_account.deposit(sal_t) #Salary deposit
            self.c_account.withdraw(frac_sal_cons) #Consumption
            self.c_account.transfer(self.s_account, frac_sal_sav) #Savings transfer
            self.c_account.yearly_adjustments(self.t, self.int_rates, disp=False) #Current Account Updates and report
            self.s_account.yearly_adjustments(self.t, self.int_rates, disp=False) #Saving Account Updates and report
            
            
        #Print Accounts Reports
        self.c_account.compute_account_report(beg, end)
        self.s_account.compute_account_report(beg, end)
        #New Transactions?

        #INVESTMENT STUFFS
        for asset in [self.e_inv, self.t_inv, self.n_inv, self.g_inv]:
            asset.multi_year_adj(beg, n, disp=True)
            
        self.long_invest_decision() #Long transactions 
        self.short_invest_decision() #Short transactions
        
        for asset in [self.e_inv, self.t_inv, self.n_inv, self.g_inv]:
            asset.single_year_adj_2(self.t)

        
    ###################PRINT FUNCTIONS###################


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
        
    def report_multiple_sav_dec(self, n, frac_sav, frac_cons):
        
        string_frac_sav = str(frac_sav * 100) + '%'
        
        info = 'For the next %d periods, you decided to save %s of your salary'%(n, string_frac_sav)
        
        print('\n')
        print('------------------------------------------------------')
        print('----------------SAVING DECISIONS INFOS----------------')
        print('------------------------------------------------------')
        print('\n', info, '\n')
        print('------------------------------------------------------') 
        
    
    def portfolio_positions(self):
        
        print('\n')
        print('------------------------------------------------------')
        print('-----------------PORTFOLIO POSITIONS------------------')
        print('------------------------------------------------------')
        print('Eatcoin : CHF ', self.e_inv.balance_t + self.e_inv.net_movements_t)
        print('------------------------------------------------------')
        print('Teslo : CHF ', self.t_inv.balance_t + self.t_inv.net_movements_t)
        print('------------------------------------------------------')
        print('Nestlo : CHF ', self.n_inv.balance_t + self.n_inv.net_movements_t)
        print('------------------------------------------------------')
        print('Gold : CHF ', self.g_inv.balance_t + self.g_inv.net_movements_t)
        print('------------------------------------------------------')



    ##################DECISION FUNCTIONS##################

    def set_sav_dec(self):
        
        #saving_q = 'What will be the fraction of your salary you want to save every year ? \n(format : type 0.5 if you want to save 50% of your salary)'
        #frac_sav = input(saving_q)
        
        #consuming_q = 'What will be the fraction of your salary you want to consume every year ? \n(format : type 0.5 if you want to consume 50% of your salary)'
        #frac_cons = input(consuming_q)
        
        frac_sav = 0.5
        frac_cons = 0.5
        
        return frac_sav, frac_cons
    
    def long_investment(self, loop = False):
        
        print('Assets available: Eatcoin, Teslo, Nestlo, Gold')
        stock = input('Which asset do you want to invest in ? Type exact name')
            
        while stock not in ['Eatcoin', 'Teslo', 'Nestlo', 'Gold']:
            stock = input('Type a valid asset name please ...')
        
        if stock == 'Eatcoin':
            asset = self.e_inv
        elif stock == 'Teslo':
            asset = self.t_inv
        elif stock == 'Nestlo':
            asset = self.n_inv
        elif stock == 'Gold':
            asset = self.g_inv

        print('Capital available: CHF ', self.s_account.balance_t)
        amt = float(input('How much do you want to invest in this asset ?'))
        while amt > self.s_account.balance_t:
            amt = float(input('Enter a valid capital please ...'))

        self.s_account.instant_adjustment(self.t, -amt)
        asset.deposit(self.t, amt)
        
        if loop == True: self.long_invest_decision()

    def short_investment(self, loop = False):
        
        print('Assets available: Eatcoin, Teslo, Nestlo, Gold')
        stock = input('Which asset do you want to sell ? Type exact name')
            
        while stock not in ['Eatcoin', 'Teslo', 'Nestlo', 'Gold']:
            stock = input('Type a valid asset name please ...')
        
        if stock == 'Eatcoin':
            asset = self.e_inv
        elif stock == 'Teslo':
            asset = self.t_inv
        elif stock == 'Nestlo':
            asset = self.n_inv
        elif stock == 'Gold':
            asset = self.g_inv
        
        val = asset.balance_t + asset.net_movements_t
        
        print('Owned asset value: CHF ', val)
        amt = float(input('How much do you want to sell in this asset ?'))
        while amt > val:
            amt = float(input('Enter a valid amount please ...'))

        self.s_account.instant_adjustment(self.t, amt)
        asset.withdraw(self.t, amt)
        
        if loop == True: self.short_invest_decision()
    
    def long_invest_decision(self):
        
        self.portfolio_positions()
        
        on = input('Do you want to invest money ? yes/no')
        
        if on == 'yes':         
            self.long_investment(loop = True)
        else:
            return
            
    def short_invest_decision(self):

        on = input('Do you want to sell some assets ? yes/no')
        
        if on == 'yes':         
            self.short_investment(loop = True)
        else:
            return


####################TESTS######################

if __name__ == "__main__":
   
    
    antoine = user(25, 90000, 20000) 
    antoine.set_sav_dec()
    antoine.run_single_cycle() 
    antoine.run_cycle(10, 0.5, 0.4) 
    #antoine.run_single_cycle() 
