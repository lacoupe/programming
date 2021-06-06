import pandas as pd


# INTRODUCTION; GAME DESCRIPTION; RULES; OPTIONS; ...


def intro():
    
    print('')
    print('---------------------------------------------------------------------------')
    print('-----------------Welcome to the Wealth Management Planner------------------')
    print('---------------------------------------------------------------------------')
    print('')
    print('Decription')
    print('---------------------------------------------------------------------------')
    print(" - This game aims to simulate user's wealth evolution along his life")
    print(" - The simulated timeline goes from user's first job to retirement")
    print(" - The goal is making decisions to reach retirement as rich as possible")
    print(" - Following terminal instructions, you'll be facing different choices")
    print(" - The largest your terminal window is, the better it is!")
    print('')
    print('Here we go ! Please follow the instructions on the terminal')
    print('---------------------------------------------------------------------------')
    
    
def simulate_salary(sec, exp, ed):
    
    sectors = ['Banking and Insurance', 'Accounting', 'Human Ressources',
               'IT', 'Law', 'Education', 'Healthcare', 'Industrial', 'Real Estate',
               'Public Services', 'Hospitality', 'Consulting and Management', 'Energy and utilities']
    
    sal = [111432, 92904, 64824, 107820, 92904, 102840, 80820, 77232, 81120, 99096, 52944, 117768, 98388]
    
    Salaries = pd.DataFrame(
        {'Sector': sectors,
         'Starting Salary': sal})
    Salaries.set_index('Sector', inplace=True)
    
    agent_salary = Salaries.loc[sec][0]

    if exp == 0:
        agent_salary = agent_salary
    elif 1 <= exp <= 3:
        agent_salary += 1000
    elif exp <= 5:
        agent_salary += 2000
    elif exp <= 10:
        agent_salary += 3000
    else:
        agent_salary += 4000
    
    if ed == 0:
        agent_salary = agent_salary
    elif 0 < ed <= 3:
        agent_salary += 1000
    elif 3 < ed <= 5:
        agent_salary += 2000
    else:
        agent_salary += 3000

    return agent_salary


def get_info_salary():
    
    sectors = ['Banking and Insurance', 'Accounting', 'Human Ressources', 'IT', 'Law', 'Education', 'Healthcare',
               'Industrial', 'Real Estate', 'Public Services', 'Hospitality',
               'Consulting and Management', 'Energy and utilities']
    
    print('')
    print('First Salary Simulator')
    print('---------------------------------------------------------------------------')
    print('')
    print('We will begin by asking you some questions to better know you \nand simulate your potential first salary')

    # Age question
    while True:
        try:
            age = int(input("How old are you ? Enter a positive number "))
            if age <= 0:
                raise ValueError
            if age > 64:
                raise ValueError

        except ValueError:
            print("This is not a valid age. Age must be integer betweem 1 and 64.")
            continue
        else:
            break
    
    # Education question
    while True:
        try:
            ed = int(input("How many years of education do you have after High School ? "))
            if ed < 0:
                raise ValueError("Your input is not a valid number. Please, enter a positive and integer number.")
        except ValueError:
            print("Your input is not a valid number. Please, enter a positive and integer number.")
            continue
        else:
            break
    
    # Experience question
    while True:
        try:
            exp = float(input("How many years of work experience do you already have ? Enter a positive number "))
            if exp < 0:
                raise ValueError("Please, enter a positive number")
        except ValueError:
            print("Please, enter a positive number")
            continue
        else:
            break

    # Sector question
    print('\nAmong the following sectors :\n')
    for s in sectors:
        print(' - ', s)
    while True:
        try:
            sec = input('In which sector do you work/will you work ? Enter exact name: ')
            if sec not in sectors:
                raise ValueError("Please, choose among the sectors listed: ")
        except ValueError:
            print("Please, choose among the sectors listed: ")
            continue
        else:
            break

    agent_salary = simulate_salary(sec, exp, ed)
    end_t = 65 - age

    print('')
    print('---------------------------------------------------------------------------')
    print('Thanks for the informations ! ')
    print('Today we are at time t = 0, you are %d years old' % (age))
    print('You will reach retirement at time t = %d when you will be %d years old!' % (end_t, 65))
    print('---------------------------------------------------------------------------')
    print('')
    print('---------------------------------------------------------------------------')
    print('1st Salary Simulation done: \nin one year, at t = 1, you will be paid CHF ', agent_salary)
    print('---------------------------------------------------------------------------')

    return age, agent_salary, end_t


def get_info_capital():
    
    while True:
        try:
            capital_q = str(input("Do you have a starting capital (Yes/No) ? "))
            if capital_q not in ('Yes', 'yes', 'No', 'no'):
                raise ValueError('Please, answer by Yes or No:')
        except ValueError:
            print('Please, answer by Yes or No')
            continue
        else:
            break

    while True:
        try:
            if capital_q in ('No', 'no'):
                capital_0 = 0
            if capital_q in ('Yes', 'yes'):
                capital_0 = float(input("How much is your starting capital ? "))
                if capital_0 < 0:
                    raise ValueError("Please, enter a positive number: ")
        except ValueError:
            print("Please, enter a positive number: ")
            continue
        else:
            break

    print('')
    print('---------------------------------------------------------------------------')
    print('Thanks again for the informations ! ')
    print('You start the game with an initial amount on your saving account of : CHF %d' % (capital_0))

    return capital_0


def first_simulation():
    print('')
    print('---------------------------------------------------------------------------')
    print('First Year Simulation (t = 0 -> t = 1)')
    print('---------------------------------------------------------------------------')
    
    while True:
        try:
            frac_s = float(input('First things first, chose the fraction of salary you want to save \n(e.g. If you want to save 20% type 0.2) '))
            frac_c = float(input('Second, chose the fraction of salary you want to consume \n(e.g. If you want to save 20% type 0.2) '))
            if frac_s > 1 or frac_c > 1 or frac_s < 0 or frac_c < 0:
                raise ValueError
            if frac_s + frac_c > 1:
                raise ValueError
        except ValueError:
            print("Please, valid fraction between 0 and 1 (e.g. 0.1, 0.25, ...) \nYou can't consume and save more than what you warn (sum <= 1)")
            continue
        else:
            break
        
    while True:
        try:
            go = input('Alright, are you ready to start playing with your life ? If yes type ok ')
            if not go == 'ok':
                raise ValueError("Please, enter a fraction between 0 and 1 (e.g. 0.1, 0.25, ...")
        except ValueError:
            print("To continue the game type ok")
            continue
        else:
            break
    
    return frac_s, frac_c


def simulation_len_q(t, end_t):
    
    max_l = end_t - t  # Maximum number of periods you can simulate up to retirement
    
    print('')
    print('---------------------------------------------------------------------------')
    print('Next simulation preparation')
    print('---------------------------------------------------------------------------')
    print('')
    print(' -Today you are at time %d' % (t))
    print(' -Remember that you will reach retirement at time %d' % (end_t))
    print(' -This therefore leaves %d years to simulate' % (max_l))
    print('')
    while True:
        try:
            length = int(input('Chose the number of years you want to simulate from now: '))
            if length < 1 or length > max_l:
                raise ValueError
        except ValueError:
            print("Please, enter a valide number of years (integer between 1 and %d))" % (max_l))
            continue
        else:
            break
        
    while True:
        try:
            frac_s = float(input('Chose the fraction of salary you want to save \n(e.g. If you want to save 20% type 0.2) '))
            frac_c = float(input('Chose the fraction of salary you want to consume \n(e.g. If you want to save 20% type 0.2) '))
            if frac_s > 1 or frac_c > 1 or frac_s < 0 or frac_c < 0:
                raise ValueError
            if frac_s + frac_c > 1:
                raise ValueError
        except ValueError:
            print("Please, valid fraction between 0 and 1 (e.g. 0.1, 0.25, ...) \nYou can't consume and save more than what you warn (sum <= 1)")
            continue
        else:
            break
        
    while True:
        try:
            go = input('Alright, ready to step %d year(s) in future ? If yes type "ok": ' % (l))
            if not go == 'ok':
                raise ValueError
        except ValueError:
            print("To continue the game type ok")
            continue
        else:
            break
        
    return l, frac_s, frac_c


def end_word():
    
    print('')
    print('---------------------------------------------------------------------------')
    print('-------------CONGRATULATION YOU JUST REACHED RETIREMENT AGE !--------------')
    print('---------------------------------------------------------------------------')
    print('')
    print("Let's see your final situation:")
    print('---------------------------------------------------------------------------')
    

if __name__ == "__main__":
    
    get_info_capital()
    l, frac_s, frac_c = first_simulation()
    simulation_len_q(1, 40)
