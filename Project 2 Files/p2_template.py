## ----------------------------------------------------------------------------------------------------------
## TEMPLATE
## Please DO NOT change the naming convention within this template. Some changes may
## lead to your program not functioning as intended.

import sys, random
sys.path.append('../')

from Common_Libraries.p2_lib import *

import os
from Common_Libraries.repeating_timer_lib import repeating_timer

def update_sim ():
    try:
        arm.ping()
    except Exception as error_update_sim:
        print (error_update_sim)

arm = qarm()

update_thread = repeating_timer(2, update_sim)


## STUDENT CODE BEGINS
## ----------------------------------------------------------------------------------------------------------
## Example to rotate the base: arm.rotateBase(90)

#L- move arm
#R- gripper
#L&R- open drawer

home = [0.4064, 0.0, 0.4826]
pick_up = [0.5336, 0.0, 0.043]
threshold = 0.3
drawer_open = [False, False, False, 0, 0]

'''
Name: f_equal
Purpose: Checks if two floats are equal within a certain tolerance range
Inputs: actual value, value to be compared to
Output: boolean (True if floats are equal)
Author: Samuel Khzym, khzyms
'''
def f_equal(actual, expected, thresh):
    if abs(actual - expected) <= thresh: return True
    else: return False

'''
Name: left_up
Purpose: Checks if left arm is up past a certain threshold
Inputs: N/A
Output: boolean (True if left arm is up)
Author: Samuel Khzym, khzyms
'''
def left_up():
    if arm.emg_left() >= threshold: return True
    else: return False

'''
Name: right_up
Purpose: Checks if right arm is up past a certain threshold
Inputs: N/A
Output: boolean (True if right arm is up)
Author: Samuel Khzym, khzyms
'''
def right_up():
    if arm.emg_right() >= threshold: return True
    else: return False

'''
Name: get_state
Purpose: Gets the "state" of the arm emulators as a list of three boolean values
Inputs: N/A
Output: list of three booleans in the form [leftUp, rightUp, armsEqual]
Author: Samuel Khzym, khzyms
'''
def get_state():
    return [left_up(), right_up(), f_equal(arm.emg_left(), arm.emg_right(), 0.1), arm.emg_left(), arm.emg_right()]



def arms_locked_moving(prev_state, state):
    if not f_equal(prev_state[3], state[3], 0.001) and not f_equal(prev_state[4], state[4], 0.001): return True
    else: return False

'''
Name: at_location
Purpose: Determines if the arm is at a certain location
Inputs: target (list of three values represeinting XYZ coords)
Output: boolean value (True if arm is at specified target)
Author: Samuel Khzym, khzyms
'''
def at_location(target):
    pos = arm.effector_position()
    if (f_equal(pos[0], target[0], 0.0001)
        and f_equal(pos[1], target[1], 0.0001)
        and f_equal(pos[2], target[2], 0.0001)): return True
    else: return False

'''
Name: identify_autoclave_bin_location

Purpose:takes in an object identiy from 1-6, and determines what colour of autoclave, and
what opening the object needs to be moved to. Outputs that location data.

Inputs: object_identity

Output: autoclave_cords

Author: Alex Stewart, stewaa31
'''
def identify_autoclave_bin_location(object_identity):
    #var to hold the cordinates to the corresponding id.
    autoclave_cords = [0,0,0]

    #using if statement to determine what the inputted id's autoclave cordinates are.
    #small red
    if object_identity == 1:
        autoclave_cords = [-0.6078, 0.2517, 0.3784]
    #small green
    elif object_identity == 2:
        autoclave_cords = [0.0, -0.6563, 0.4139]
    #small blue
    elif object_identity == 3:
        autoclave_cords = [0.0, 0.6563, 0.4139]
    #large red
    elif object_identity == 4:
        autoclave_cords = [-0.3627, 0.1502, 0.3774]
    #large green
    elif object_identity == 5:
        autoclave_cords = [0.0, -0.4002, 0.412]
    #large blue
    elif object_identity == 6:
        autoclave_cords = [0.0, 0.4002, 0.412]
    #else return home cordinates
    else:
        autoclave_cords = [0.4064, 0.0, 0.4826]

    #returning autoclave_cords
    return(autoclave_cords)

'''
Name: move_end_effctor
Purpose: Cycles end effector between home, pickup, and dropoff locationbased on input data from the muscle emulators.
If at home, end effector moves to pickup. If at pickup, end effector moves to dropoff.
If at dropoff, arm returns home. If arm is in unidentifiable position, arm moves home.
Inputs: List of the previous state of the system, List of the current state of the system, Current dropoff location
Output: N/A
Author: Samuel Khzym, khzyms
'''
def move_end_effector(prev_state, state, dropoff):
    if prev_state[0] != state[0] and state[0] == True and arms_locked_moving(prev_state, state) == False:
        if at_location(home):
            arm.move_arm(*pick_up)
            return False
        elif at_location(pick_up):
            arm.move_arm(*dropoff)
            return False
        elif at_location(dropoff):
            arm.move_arm(*home)
            return True
        else:
            arm.move_arm(*home)
            return False

def open_autoclave_bin_drawer(prev_state, state, c_id):
    print(arms_locked_moving(prev_state, state))
    if arms_locked_moving(prev_state, state) and (state[0] == True or state[1] == True):
        if c_id < 3:
            print("Invalid container ID. Cannot open drawer")
        elif c_id == 4:
            arm.open_red_autoclave(drawer_open[0])
            drawer_open[0] = not drawer_open[0]
        elif c_id == 5:
            arm.open_green_autoclave(drawer_open[1])
            drawer_open[1] = not drawer_open[1]
        elif c_id == 6:
            arm.open_blue_autoclave(drawer_open[2])
            drawer_open[2] = not drawer_open[2]
            
def main():
    container_sequence = [i for i in range(1,7,1)]
    random.shuffle(container_sequence)
    prev_state = [False, False, False, 0, 0]
    finish_cycle = False
    
    #infinite loop for program execution
    for i in container_sequence:
        arm.spawn_cage(i)
        dropoff = identify_autoclave_bin_location(i)
        
        while not finish_cycle:
            state = get_state()
            finish_cycle = move_end_effector(prev_state, state, dropoff)
            open_autoclave_bin_drawer(prev_state, state, i)
            #time.sleep(.2)
            prev_state = state

        finish_cycle = False

if __name__ == "__main__":
    main()
