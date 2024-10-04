
import random

def get_cup_current():
    return random.gauss(500e-9, 5e-9)
    
def get_screen_current():
    return random.gauss(32e-6, 1e-7)