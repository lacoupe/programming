from functions.salary_evolution_rates import wage_growth_sample, gen_ue_agenda
 

class Salary:
    
    def __init__(self, initial_wage, len_life):
        self.first_wage = initial_wage  # First year (t=0 to t=1) wage
        self.wage_t = 0  # Actual wage (t) (intitialized at 0 at t=0)
        self.growth_sample = wage_growth_sample(N=len_life)  # Simulation of wage growth
        self.ue_agenda_dict, self.ue_agenda_list = gen_ue_agenda(N=len_life)  # Simulation of unemployment periods
        self.wage_evolution = {0: {'Salary': 0, 'Growth': 'Start'},
                               1: {'Salary': initial_wage, 'Growth': 'First Salary'}}  # Dict keeping all wages (initialized with w_0, w_1)
        self.t = 0  # time pointer initialized at 0
        
        self.wage_agenda = self.compute_wage_agenda(N=len_life)
    
    def yearly_adjustments(self, t, w_rates):
        
        if t == 0:
            return  # at t=0, nothing happens as first wage will be paid at t=1
        if t == 1:
            self.t = 1
            self.wage_t = self.first_wage
            return  # at t=1, wage is equal to the initialized wage and no risk of unemployment
        
        self.t = t
        self.wage_evolution[t] = {}
        last_wage = self.wage_evolution.get(t - 1).get('Salary')
        
        if (t - 1) in self.ue_agenda_list:  # In case if it was an unemployment year
            self.wage_t = 0  # If this was an unemployment year, 0 salary
            
            self.wage_evolution[t]['Salary'] = self.wage_t  # Store 0 wage
            self.wage_evolution[t]['Growth'] = 'UE'  # UE = Unemployment
        else:
            if last_wage == 0:  # If last year was unemployment, go to last positive salary
                k = 2
                while last_wage == 0:
                    last_wage = self.wage_evolution.get(t - k).get('Salary')
                    k += 1
            evol_rate = w_rates[t - 1]  # Get the growth rate of the wage
            self.wage_t = last_wage * (1 + evol_rate)  # Compute new wage
            
            self.wage_evolution[t]['Salary'] = self.wage_t  # Store new wage
            self.wage_evolution[t]['Growth'] = evol_rate  # Store growth rate
        
    def compute_wage_agenda(self, N=65):
        
        for i in range(N + 1):
            self.yearly_adjustments(i, self.growth_sample)
        
        return self.wage_evolution
            
    def compute_salary_report(self, beg, end):
        
        timeline = range(beg, end + 1)
        
        print(80 * '-')
        print(80 * '-')
        print("{:<30}{:<20}{:<30}".format(' ', 'SALARY REPORT', ' '))
        print(80 * '-')
        print(80 * '-')
        print("{:<10}{:<20}{:<50}".format('Year', 'Salary', 'Evolution'))
        print(80 * '-')
        for i in timeline:
            w = '%.2f' % self.wage_agenda[i]['Salary']
            
            if isinstance(self.wage_agenda[i]['Growth'], str):
                if self.wage_agenda[i]['Growth'] == 'UE':
                    s = 'Unlucky: Unemployment period ...'
                else:
                    s = self.wage_agenda[i]['Growth']
            else:
                g = '%.2f' % (self.wage_agenda[i]['Growth'] * 100)
                
                if self.wage_agenda[i]['Growth'] > 0:
                    s = 'Cool ! Get increased by {}% wrt to last salary'.format(g)
                elif self.wage_agenda[i]['Growth'] == 0:
                    s = 'Your salary is the same!'
                else:
                    s = 'Unlucky ! Get decreased by {}% wrt to last salary'.format(g)

            print("{:<10}{:<20}{:<50}".format(i, w, s))
        
        print(80 * '-')
        print(80 * '-')

    def salary_single_report(self, t):
        
        sal_t = self.wage_agenda[t]['Salary']  # Salary we get at time t
        growth_t = self.wage_agenda[t]['Growth']  # Salary growth get at time t
        
        if growth_t == 'UE':
            info = 'Unlucky: Unemployment period ...'
        else:
            info = "At time %d you receive a salary of CHF %d, \n (growth rate : %s) " % (t, sal_t, growth_t)
        
        print('\n')
        print('------------------------------------------------------')
        print('---------------------SALARY INFOS---------------------')
        print('------------------------------------------------------')
        print('\n', info, '\n')
        print('------------------------------------------------------')


if __name__ == "__main__":

    w1 = Salary(6000, 40)
    w1.wage_agenda
    w1.compute_salary_report(0, 20)
    w1.salary_single_report(8)
