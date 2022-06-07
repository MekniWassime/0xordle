import random
from datetime import datetime

def get_hex_of_the_day(): ## generates a new hex everyday
    nbr_of_days = (datetime.now() - datetime(2020,1,1)).days
    random.seed(nbr_of_days)
    daily_hex = ""
    for i in range(6):
        char = str(hex(random.randint(0, 15)))
        daily_hex += char.split('x')[1]
    return daily_hex