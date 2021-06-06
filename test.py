from functions import interactions
from modules.user import User


time = 0

# Start the game
interactions.intro()

# Get informations needed to start simulations
age, salary_1, end_t = interactions.get_info_salary()
cap_0 = interactions.get_info_capital()

# Initialize the game parameters
player = User(age, salary_1, cap_0)

# First year simulation
frac_s, frac_c = interactions.first_simulation()
time = player.run_single_cycle(frac_s, frac_c, first_sim=True)

while time < end_t:
    length, frac_s, frac_c = interactions.simulation_len_q(time, end_t)
    if length == 1:
        player.run_single_cycle(frac_s, frac_c)
    else:
        player.run_cycle(length, frac_s, frac_c)
    
    time += length

interactions.end_word()
player.end_report()
player.end_reports_decision()
