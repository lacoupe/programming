# -*- coding: utf-8 -*-
"""
Created on Fri May  7 10:47:20 2021

@author: Antoine
"""

from stock_class import Stock


class Investment:
    
    def __init__(self,name, n=65):
        self.name = name #Name of the asset you invest in
        self.asset = self.gen_asset(self.name, n) #Generate the asset process n years
        try:
            self.returns = self.asset.get_y_returns()
        except:
            print('Not a valid investment asset name !')
        
        self.balance_t = 0 #Initial investment you start simulation with at t = 0
        self.last_balance_t = 0 #Last simulation step balance (at t-dt)
        
        self.net_movements_t = 0 #making the sum of + & - transfers where portfolio is concerned
        
        self.hist = {} #Dictionary which will keep history of the account
        self.hist[0] = {'last_balance':0, 'return':0,'pnl': 0, 'balance':0, 'net_mov':0, 'adj_balance': 0}


        
    def gen_asset(self, name, n):
        
        #List of assets name
        asset_names = ['Eatcoin', 'Teslo', 'Nestlo', 'Gold']
    
        #Parameters of each assets
        eatcoin_param = ['Eatcoin', 'very_high', 'best cryptocurrency', n]
        teslo_param = ['Teslo', 'high', 'electric car company', n]
        nestlo_param = ['Nestlo', 'medium', 'milk company', n]
        gold_param = ['Gold', 'low', 'something that is precious', n]
        
        #Dictionary linking asset names and parameteres
        assets = {'Eatcoin': eatcoin_param, 'Teslo': teslo_param, 'Nestlo': nestlo_param, 'Gold': gold_param }
        
        #Generate the asset if asset asked exists
        if self.name not in asset_names:
            #print('Not a valid investment asset name !')
            return
            
        else:
            for name in asset_names:
                if self.name == name:
                    p = assets[name]
                    asset = Stock(p[0], p[1], p[2], p[3])
                    return asset
                else:
                    continue
                
    def deposit(self, t, amount, disp = True):
        
        bal = self.balance_t + self.net_movements_t
        
        self.net_movements_t += amount
        
        if disp:
            print('')
            print('Transaction Report')
            print('------------------------------------------------------')
            print('Asset concerned : %s'%(self.name))
            print('Balance before adjustment at t = %d : CHF %d'%(t, bal))
            print('Investment amount = %d : CHF %d'%(t, amount))
            print('Adjusted balance at t = %d : CHF %d'%(t, bal + amount))

        
        
    def withdraw(self, t, amount, disp = True):
        
        bal = self.balance_t + self.net_movements_t
        
        self.net_movements_t -= amount
        
        if disp:
           print('')
           print('Transaction Report')
           print('------------------------------------------------------')
           print('Asset concerned : %s'%(self.name))
           print('Balance before adjustment at t = %d : CHF %d'%(t, bal))
           print('Sale amount = %d : CHF %d'%(t, amount))
           print('Adjusted balance at t = %d : CHF %d'%(t, bal - amount))
                   
        
    def return_adjustment(self, t):
        if t==0:
            return
                             
        ret = self.returns[t] #ASset return over last year
        pnl = self.last_balance_t*ret  #Yearly P&L based on last year balance
        self.balance_t += pnl #Ajust Investment Value  
        
        self.hist[t] = {}
        
        self.hist[t]['last_balance'] = self.last_balance_t
        self.hist[t]['return'] = ret
        self.hist[t]['pnl'] = pnl
        self.hist[t]['balance'] = self.balance_t
        self.hist[t]['net_mov'] = 0
        self.hist[t]['adj_balance'] = self.balance_t


    def situation_report(self, t):
        if self.balance_t == 0: return
        
        name = self.name
        ret = self.returns[t]
        pnl = self.last_balance_t*ret
        
        print('')
        print('%s Investment:'%(name))
        print('------------------------------------------------------')
        print('Last year (t = {}) investment value was : CHF {}'.format(t-1, round(self.last_balance_t)))
        print('Yearly return realized : {}%'.format(round(ret*100, 4)))
        print('P&L : CHF {}'.format(round(pnl)))
        print('This year (t= {}) balance is : CHF {}'.format(t, round(self.balance_t)))
        print('------------------------------------------------------')

    def transac_report(self, t):
        if self.net_movements_t == 0: return
        print('')
        print('Transaction Report')
        print('------------------------------------------------------')
        print('Asset concerned : %s'%(self.name))
        print('Balance before adjustment at t = %d : CHF %d'%(t, self.balance_t))
        print('Net movements at t = %d : CHF %d'%(t, self.net_movements_t))
        print('Adjusted balance at t = %d : CHF %d'%(t, self.balance_t + self.net_movements_t))
        
    def compute_investment_report(self, beg, end):
        
        
        if self.hist[beg]['adj_balance']==0 and not beg == 0 :
            return
        
        timeline = range(beg, end + 1)
        
        title = 'ASSET INVESTMENT REPORT'
        subtitle = 'Asset Name : %s'%(self.name)
        
        print(95*'-')
        print(95*'-')
        print("{:<35}{:<25}{:<35}".format(' ',title,' '))
        print(95*'-')
        print(95*'-')
        print(subtitle)
        print(95*'-')        
        print("{:<5}{:<15}{:<15}{:<15}{:<15}{:<15}{:<15}".format('Year','Last Balance','Return', 'P&L', 'Balance', 'Net Mov.', 'Adj. Bal'))
        print(95*'-')
        
        
        for t in timeline :
            
            l_bal = round(self.hist[t]['last_balance'],2)
            ret = str(round(self.hist[t]['return']*100, 3)) + ' %'
            pnl = round(self.hist[t]['pnl'], 2)
            bal = round(self.hist[t]['balance'], 2)
            net_mov = round(self.hist[t]['net_mov'], 2)
            adj_bal = round(self.hist[t]['adj_balance'], 2)
            
            print("{:<5}{:<15}{:<15}{:<15}{:<15}{:<15}{:<15}".format(t, l_bal, ret, pnl, bal, net_mov, adj_bal))
        
        print(95*'-')
        print(95*'-')

    def single_year_adj_1(self, t, disp = True):
        if t==0: return
        
        #Adjust for returns
        self.return_adjustment(t)
        
        #Display informations about performance
        if disp: self.situation_report(t)
    
        #Ask user for possible transactions!!!!!!!!!!!!!!!!!!!
        
    def single_year_adj_2(self,t, disp = True):
        if t==0: return
        #Display informations about transactions
        #if disp: self.transac_report(t)
        
        #Adjust for transactions
        net_mov = self.net_movements_t #Net yearly withdrawals, deposits, need to adjust
        self.balance_t += net_mov #Adjust balance for movements
        
        #Store data
        self.hist[t]['net_mov'] = net_mov
        self.hist[t]['adj_balance'] = self.balance_t
        
        #Reset variables
        self.net_movements_t = 0
        self.last_balance_t = self.balance_t
    
    def multi_year_adj(self, beg, n, disp = True):
        
        timeline = range(beg, beg+n)
        
        for t in timeline:
            if t==0: continue    
                        
            self.single_year_adj_1(t, False)
            if not t == beg + n - 1:
                self.single_year_adj_2(t, False)
        
        if disp: self.compute_investment_report(beg, beg + n -1)

        
################TEST######################

if __name__ == "__main__":
                  
    test_inv = Investment('Teslo')
    test_inv.returns[:5]
    
    test_inv.single_year_adj_1(1)
    test_inv.deposit(1, 200)
    test_inv.single_year_adj_2(1)
    
    test_inv.single_year_adj_1(2)
    test_inv.single_year_adj_2(2)
    
    test_inv.single_year_adj_1(3)
    test_inv.withdraw(3, 50)
    test_inv.single_year_adj_2(3)
    
    test_inv.single_year_adj_1(4)
    test_inv.single_year_adj_2(4)
    
    test_inv.single_year_adj_1(5)
    test_inv.single_year_adj_2(5)
    
    test_inv.single_year_adj_1(6)
    test_inv.single_year_adj_2(6)
    
    test_inv.single_year_adj_1(7)
    test_inv.single_year_adj_2(7)
    
    test_inv.single_year_adj_1(8)
    test_inv.single_year_adj_2(8)
    
    test_inv.single_year_adj_1(9)
    test_inv.single_year_adj_2(9)
    
    test_inv.single_year_adj_1(10)
    test_inv.single_year_adj_2(10)
    
    test_inv.hist
    
    test_inv.compute_investment_report(1, 10)
    
    test_inv.multi_year_adj(11,10, disp = True)
    
