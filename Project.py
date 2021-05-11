
import interactions
from user_class import user

#Start the game
interactions.intro()

#Get informations needed to start simulations
age, salary_1 = interactions.get_info_salary()
cap_0 = interactions.get_info_capital()

#Initialize the game parameters
player = user(age, salary_1, cap_0)

#First year simulation
player.run_single_cycle(interactions.first_simulation())
