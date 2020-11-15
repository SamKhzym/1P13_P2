import sys
sys.path.append('../')
import time
from Common_Libraries.p0_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim ():
    try:
        my_qbot.ping()
    except Exception as error_update_sim:
        print (error_update_sim)


speed = 0.1 # in m/s
my_qbot = qbot(speed)
update_thread = repeating_timer(2, update_sim)

#---------------------------------------------------------------------------------
# STUDENT CODE BEGINS
#---------------------------------------------------------------------------------

#TIME CONTROLLED

method = "distance"

my_qbot = qbot(speed)

t0 = time.time()

if method=="distance":
    my_qbot.travel_forward(0.3)
    my_qbot.rotate(-95)

    my_qbot.travel_forward(0.2)
    my_qbot.rotate(-95)

    my_qbot.travel_forward(0.3)
    my_qbot.rotate(-100)

    my_qbot.travel_forward(0.2)
    my_qbot.rotate(-95)

    my_qbot.travel_forward(0.9)

else:
    my_qbot.forward(5)
    my_qbot.rotate(-95)

    my_qbot.forward(7)
    my_qbot.rotate(-95)

    my_qbot.forward(10)
    my_qbot.rotate(-95)

    my_qbot.forward(7)
    my_qbot.rotate(-95)

    my_qbot.forward(5)

t1 = time.time()

print("Elapsed time " + str(t1-t0))




