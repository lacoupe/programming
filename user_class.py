# -*- coding: utf-8 -*-
"""
Created on Tue May  4 15:14:45 2021

@author: Antoine
"""

from account_class import Account
from interest_rates import rate_evolution_sample
from salary_class_2 import Salary
from investment_class import Investment
from Roulette import roulette_game_intro

class user:

    ###############INITIALISATION FUNCTIONS###############

    
    def __init__(self, age, first_sal, first_cap):
        self.age = age #The age at which user start working
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
        
        e_inv =  Investment('Eatcoin', n + 1)
        t_inv = Investment('Teslo', n + 1)
        n_inv = Investment('Nestlo', n + 1)
        g_inv = Investment('Gold', n + 1)
        
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
        int_rates = rate_evolution_sample(N = self.len_life + 1)
        
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
        
        self.transfer_decision() #Ask for any money transfers
        self.casino_decision() #Ask for casino gambling
        
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
                    
        return self.t

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
        
        self.transfer_decision() #Ask for any money transfers
        self.casino_decision() #Ask for casino gambling

        #New Transactions?

        #INVESTMENT STUFFS
        for asset in [self.e_inv, self.t_inv, self.n_inv, self.g_inv]:
            asset.multi_year_adj(beg, n, disp=True)
            
        self.long_invest_decision() #Long transactions 
        self.short_invest_decision() #Short transactions
        
        for asset in [self.e_inv, self.t_inv, self.n_inv, self.g_inv]:
            asset.single_year_adj_2(self.t)

        return self.t        
        

    ###################PRINT FUNCTIONS###################


    def report_single_sav_dec(self, sal_t, frac_sav, frac_cons):
        """
        function which create a report on saving decisions
        """
        
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
        """
        function which create a report on saving decisions
        """
        string_frac_sav = str(frac_sav * 100) + '%'
        
        info = 'For the next %d periods, you decided to save %s of your salary'%(n, string_frac_sav)
        
        print('\n')
        print('------------------------------------------------------')
        print('----------------SAVING DECISIONS INFOS----------------')
        print('------------------------------------------------------')
        print('\n', info, '\n')
        print('------------------------------------------------------') 
        
    
    def portfolio_positions(self):
        """
        function which create a summary of user's positions instantaneously
        """
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
        """
        Actual buying function which will update portfolio positions and saving accounts balance
        when user want to buy assets (function called by related decision function long_invest_decision())
        
        loop parameter allows to ask again the user until he don't want to buy anything anymore'
        """
        
        #Display all assets available to user
        print('Assets available: Eatcoin, Teslo, Nestlo, Gold')
        stock = input('Which asset do you want to invest in ? Type exact name') #User chose one of those
        
        #Verify that user type a real asset name, if not he needs to update his choice
        while stock not in ['Eatcoin', 'Teslo', 'Nestlo', 'Gold']:
            stock = input('Type a valid asset name please ...')
        
        #Set the investment object which will be modified
        if stock == 'Eatcoin':
            asset = self.e_inv
        elif stock == 'Teslo':
            asset = self.t_inv
        elif stock == 'Nestlo':
            asset = self.n_inv
        elif stock == 'Gold':
            asset = self.g_inv

        print('Capital available: CHF ', self.s_account.balance_t) #The capital he has available for investments
        amt = float(input('How much do you want to invest in this asset ?'))
        while amt > self.s_account.balance_t or amt < 0 : #He needs to have enough money on saving account for investing
            amt = float(input('Enter a valid capital please ...'))

        self.s_account.instant_adjustment(self.t, -amt) #Make instantaneous ajustment to saving account
        asset.deposit(self.t, amt) #Increase the value of asset investment
        
        if loop == True: self.long_invest_decision() #Contine asking him for any new transaction

    def short_investment(self, loop = False):
        """
        Actual selling function which will update portfolio positions and saving accounts balance
        when user want to sell assets (function called by related decision function short_invest_decision())
        
        loop parameter allows to ask again the user until he don't want to sell anything anymore'
        """
        
        #Display all assets available to user
        print('Assets available: Eatcoin, Teslo, Nestlo, Gold')
        stock = input('Which asset do you want to sell ? Type exact name') #User chose one of those
        
        #Verify that user type a real asset name, if not he needs to update his choice
        while stock not in ['Eatcoin', 'Teslo', 'Nestlo', 'Gold']:
            stock = input('Type a valid asset name please ...')
        
        #Set the investment object which will be modified
        if stock == 'Eatcoin':
            asset = self.e_inv
        elif stock == 'Teslo':
            asset = self.t_inv
        elif stock == 'Nestlo':
            asset = self.n_inv
        elif stock == 'Gold':
            asset = self.g_inv
        
        #The actual value of the asset we instantly own 
        val = asset.balance_t + asset.net_movements_t #(need to add net_movements_t if other movements have been made without having been adjusted for till now)
        
        print('Owned asset value: CHF ', val)
        amt = float(input('How much do you want to sell in this asset ?'))
        while amt > val or amt < 0:
            amt = float(input('Enter a valid amount please ...'))

        self.s_account.instant_adjustment(self.t, amt) #Make instantaneous ajustment to saving account
        asset.withdraw(self.t, amt) #Withdraw the amount to related investment account
        
        if loop == True: self.short_invest_decision() #Contine asking him for any new transaction
    
    def long_invest_decision(self):
        """
        Decision function to ask user whether he wants to buy any assets
        calls function long_investment() if user want to invest
        """
     
        self.portfolio_positions() #Display his portfolio positions

        while True:
            try:
                on = input('Do you want to invest money ? yes/no ')
                if on not in ['yes', 'Yes', 'no', 'No'] :
                    raise ValueError
            except ValueError:
                print("Type yes or no to continue")
                continue
            else : 
                break

        if on in ['no', 'No']: #Doesn't want to do any transfer
            return
        else:
            self.long_investment(loop = True) #Will allow to ask again when this investment will be done
        
            
    def short_invest_decision(self):
        """
        Decision function to ask user whether he wants to sell any of his assets
        calls function short_investment() if user want to sell
        """

        while True:
            try:
                on = input('Do you want to sell some assets ? yes/no ')
                if on not in ['yes', 'Yes', 'no', 'No'] :
                    raise ValueError
            except ValueError:
                print("Type yes or no to continue")
                continue
            else : 
                break

        if on in ['no', 'No']: #Doesn't want to do any transfer
            return
        else:
            self.short_investment(loop = True) #Will allow to ask again when this investment will be done


    def transfer_decision(self):
        """
        Decision function to ask user whether he wants to make any transfers or not
        """
        
        while True:
            try:
                on = input('Do you want to make any account money transfer ? yes/no ')
                if on not in ['yes', 'Yes', 'no', 'No'] :
                    raise ValueError
            except ValueError:
                print("Type yes or no to continue")
                continue
            else : 
                break

        if on in ['no', 'No']: #Doesn't want to do any transfer
            return

        while True:
            try:
                kind = input('What transfer do you want to proceed? \n - Type 1: Current -> Saving \n - Type 2: Saving -> Current \nType 1 or 2 : ')
                if kind not in ['1', '2'] :
                    raise ValueError
            except ValueError:
                print("Type 1 or 2 to continue")
                continue
            else : 
                break

        #Call the actual transfer updating functions
        if kind == '1':
            self.transfer_type1_decision() 
        elif kind == '2':
            self.transfer_type2_decision()
        else:
            return
    
    def transfer_type1_decision(self):
        """
        This function will allow the user to make transfers of type Current to Saving account
        depending on his capital available on debited account
        """
        
        bal = self.c_account.balance_t #Available amount
        
        print('Amount available on Current Account : CHF %d'%bal)

        while True:
            try:
                amt = float(input('What amount do you want to transfer on your Saving Account : '))
                if amt<0 or amt > bal:
                    raise ValueError
            except ValueError:
                print("Transfer amount needs to be positive and your account balance need to allow it.")
                continue
            else : 
                break
         
        #Update accounts
        self.c_account.instant_adjustment(self.t, -amt)
        self.s_account.instant_adjustment(self.t, amt)

    
    def transfer_type2_decision(self):
        """
        This function will allow the user to make transfers of type Saving to Current account
        depending on his capital available on debited account
        """
        bal = self.s_account.balance_t #Available amount
        
        print('Amount available on Saving Account : CHF %d'%bal)

        while True:
            try:
                amt = float(input('What amount do you want to transfer on your Current Account : '))
                if amt<0 or amt > bal:
                    raise ValueError
            except ValueError:
                print("Transfer amount needs to be positive and your account balance need to allow it.")
                continue
            else : 
                break
        
        #Update accounts
        self.s_account.instant_adjustment(self.t, -amt) 
        self.c_account.instant_adjustment(self.t, amt)


    def casino_decision(self):
        """
        This is the casino decision function which will ask the user whether he wanna play (again) 
        and depending on his current account capital he'll be able to gamble.
        """

        bal = self.c_account.balance_t #Set up its initial current account balance (max gambling amount)

        #Ask him whether he want to play or not
        while True:
            try:
                on = input('Do you want to gamble at casino Roulette ? yes/no  ')
                if on not in ['yes', 'Yes', 'no', 'No'] :
                    raise ValueError
            except ValueError:
                print("Type yes or no to continue")
                continue
            else : 
                break

        if on in ['no', 'No']:
            return
        
        #He answered yes, therefore we move to virtual casino
        print('WELCOME TO CASINO ROULETTE !')
        print('------------------------------------------------------')
        print('(Amount available on current account : CHF %d)'%(bal))
        
        play = True #pointer allowing to know when to rerun the game and when user want to stop gambling
        
        while play == True: #While user want to play
            
            amount_played, amount_out = roulette_game_intro(bal) #Calling the function run the game and return the amount bet and the end amount
            
            if amount_played == 0: #If he didn't gamble no need to make accounts adjustment
                return
            if amount_out  == 0: #If he lost everything, withdraw amount played from account
                self.c_account.instant_adjustment(self.t, -amount_played)
            else: #If he won, deposit end amount on account
                self.c_account.instant_adjustment(self.t, amount_out - amount_played)
        
            bal = self.c_account.balance_t #update maximum amount he can gamble with
        
            #Ask him whether he want to play again or not
            while True:
                try:
                    again = input('Do you want to play again at casino Roulette ? yes/no  ')
                    if again not in ['yes', 'Yes', 'no', 'No'] :
                        raise ValueError
                except ValueError:
                    print("Type yes or no to continue")
                    continue
                else : 
                    break
            if again in ['no', 'No']: #Exit the loop
                play = False
            else :
                play = True #Continue the loop


####################TESTS######################

if __name__ == "__main__":
   
    
    antoine = user(25, 90000, 20000) 
    #antoine.set_sav_dec()
    antoine.run_single_cycle() 
    antoine.casino_decision()
    #antoine.run_cycle(10, 0.5, 0.4) 
    #antoine.run_single_cycle() 
    #antoine.transfer_decision()


