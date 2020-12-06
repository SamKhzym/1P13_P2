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

#If the LEFT ARM is above threshold value, move_end_effector() function is called
#If the RIGHT ARM is above threshold value, control_gripper() function is called
#If the LEFT ARM AND RIGHT ARM are EQUAL and above threshold value, open_autoclave_bin_drawer() function is called

#Initializes global variables
home = [0.4064, 0.0, 0.4826]
pick_up = [0.5336, 0.0, 0.043]
threshold = 0.3
drawer_open = [False, False, False]
state = [False, False, False, 0, 0]
prev_state = [False, False, False, 0, 0]

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
Purpose: Gets the "state" of the arm emulators as a list of three boolean values and two doubles
Inputs: N/A
Output: list (three booleans and two doubles in the form [leftUp, rightUp, armsEqual, left_value, right_value])
Author: Samuel Khzym, khzyms
'''
def get_state():
    return [left_up(), right_up(), f_equal(arm.emg_left(), arm.emg_right(), 0.1), arm.emg_left(), arm.emg_right()]

'''
Name: arms_locked_moving
Purpose: Determines if the both arms are moving at the same time, thus implying they are locked
Inputs: prev_state (list- state of the previous scan of the system), state (list- state of the current scan of the system)
Output: boolean (True if arms are locked and moving, False if not)
Author: Samuel Khzym, khzyms
'''
def arms_locked_moving(prev_state, state):
    if not f_equal(prev_state[3], state[3], 0.001) and not f_equal(prev_state[4], state[4], 0.001): return True
    else: return False

'''
Name: at_location
Purpose: Determines if the arm is at a certain location
Inputs: target (list- three values representing XYZ coords)
Output: boolean (True if arm is at specified target)
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

Purpose:takes in an object identity from 1-6, and determines what colour of autoclave, and
what opening the object needs to be moved to. Outputs that location data.

Inputs: object_identity (int- container ID)

Output: list (x,y,z values of autoclave_coords)

Author: Alex Stewart, stewaa31
'''
def identify_autoclave_bin_location(object_identity):
    #var to hold the coordinates to the corresponding id.
    autoclave_coords = [0,0,0]

    #using if statement to determine what the inputted id's autoclave coordinates are.
    #small red
    if object_identity == 1:
    #small green
    elif object_identity == 2:
    #small blue
    elif object_identity == 3:
    #large red
    elif object_identity == 4:
        autoclave_coords = [-0.37, 0.17, 0.314]
    #large green
    elif object_identity == 5:
        autoclave_coords = [0.0, -0.405, 0.312]
        autoclave_coords = [0.0, -0.4002, 0.312]
    #large blue
    elif object_identity == 6:
        autoclave_coords = [0.0, 0.405, 0.312]
        autoclave_coords = [0.0, 0.395, 0.312]
    #else return home cordinates
    else:
        autoclave_coords = [0.4064, 0.0, 0.4826]

    #returning autoclave_cords
    return(autoclave_coords)

'''
Name: move_end_effctor
Purpose: Cycles end effector between home, pickup, and dropoff locationbased on input data from the muscle emulators.
If at home, end effector moves to pickup. If at pickup, end effector moves to dropoff.
If at dropoff, arm returns home. If arm is in unidentifiable position, arm moves home.
Inputs: dropoff (list- Current dropoff location)
Output: boolean (True if arm moves from dropoff to home to complete a cycle, False if not)
Author: Samuel Khzym, khzyms
'''
def move_end_effector(dropoff):

    global state
    global prev_state

    #Updates the global variable containing the state of the muscle sensor emulators
    state = get_state()
    
    if (prev_state[0] != state[0] and state[0] == True
        and arms_locked_moving(prev_state, state) == False and state[2] == False):

        #If at home, move to pickup
        if at_location(home):
            arm.move_arm(*pick_up)
            return False

        #If at pickup, move arm up to avoid bumping into autoclaves, then go to dropoff
        elif at_location(pick_up):
            arm.rotate_shoulder(-45)
            time.sleep(1)
            time.sleep(1)
            arm.move_arm(*dropoff)
            arm.move_arm(dropoff[0], dropoff[1], dropoff[2])
            return False

        #If at dropoff, move to home
        elif at_location(dropoff):
            arm.move_arm(*home)
            return True

        #If not at any of these locations, return the arm home
        else:
            arm.move_arm(*home)
            return False

'''
Name: control_gripper

Purpose: Opens/Closes the gripper based on the state of the muscle emulator values

Inputs: grip_open (boolean- current state of the gripper, False if closed, True if open)

Output: boolean (True if gripper is open, False if closed)

Author: Alex Stewart, stewaa31
'''
def control_gripper(grip_open):

    global state
    global prev_state
    
    #checking if the right arm was just moved up, and that both arms are not up.
    if (state[1] != prev_state[1] and state[1] == True and state[2] == False
        and arms_locked_moving(prev_state, state) == False):

        #arm is in position, see what the gripper position is, change to opposite
        if grip_open:

            #gripper is open so setting gripper close

            #sending back if the gripper is open, True or False
            #just closed, so False
            return(False)
        else:
            #gripper is closed, so setting gripper open

            #sending back if the gripper is open, True or False
            #just opened, so True
            return(True)

    #else just return the sent gripper position
    return(grip_open)

'''
Name: open_autoclave_bin_drawer
Purpose: Opens or closes the autoclave bin drawer corresponding with the proper container and colour
Inputs: c_id (int- Current container ID)
Output: N/A
Author: Samuel Khzym, khzyms
'''
def open_autoclave_bin_drawer(c_id):
    
    global state
    global prev_state

    #Execute if both arms are moving at the same time and both arms are currently above the threshold
    if (arms_locked_moving(prev_state, state) and state[0] == True and state[1] == True and prev_state[0] == False
        or state[2] == True and state[1] == True and state[0] == True and prev_state[0] == False):

        #If the container is small, print a short error message to console
        if c_id < 3:
            print("Invalid container ID. Cannot open drawer")

        #If the container is large, change the internal state of the system to indicate the change in state of
        #the drawer and set the drawer to that new state
        elif c_id == 4:
            drawer_open[0] = not drawer_open[0]
            arm.open_red_autoclave(drawer_open[0])
        elif c_id == 5:
            drawer_open[1] = not drawer_open[1]
            arm.open_green_autoclave(drawer_open[1])
        elif c_id == 6:
            drawer_open[2] = not drawer_open[2]
            arm.open_blue_autoclave(drawer_open[2])

    #Saves the current state to the prev_state global variable to be used for comparison in the next iteration
    prev_state = state

'''
Name: main
Purpose: Executes main program
Inputs: N/A
Output: N/A
Author: Samuel Khzym, khzyms; Alex Stewart
'''
def main():
    #boolean value that holds whether the current container's execution cycle is complete (default set to False)
    finish_cycle = False
    
    #boolean value that holds whether gripper is open (default set to True as program starts with gripper open)
    grip_open = True

    #Creates a random list of integers between 1 and 6
    container_sequence = [i for i in range(1,7,1)]
    random.shuffle(container_sequence)

    for i in container_sequence:

        #i = 1

        #Spawns container based on randomized ID, gets coords for dropoff location of that container
        arm.spawn_cage(i)
        dropoff = identify_autoclave_bin_location(i)

        #infinite loop for program execution
        finish_cycle = False
        while not finish_cycle:

            #Moves the end effector to the proper location if the left arm changes state to up
            finish_cycle = move_end_effector(dropoff)
            
            #opening/closing the gripper if only the right arm is up
            grip_open = control_gripper(grip_open)

            #Opens autoclave drawer if both hands are moving and their state changes to up
            open_autoclave_bin_drawer(i)

#Calls main function
if __name__ == "__main__":
    main()
