## ----------------------------------------------------------------------------------------------------------
## TEMPLATE
## Please DO NOT change the naming convention within this template. Some changes may
## lead to your program not functioning as intended.

import sys
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
drop_off = [0.3, 0.3, 0.3]
pick_up = [0.5336, 0.0, 0.043]
threshold = 0.3

def f_equal(actual, expected, thresh):
    if abs(actual - expected) <= thresh: return True
    else: return False

def left_up():
    if arm.emg_left() >= threshold: return True
    else: return False

def right_up():
    if arm.emg_right() >= threshold: return True
    else: return False

def get_state():
    if left_up() and right_up() and f_equal(arm.emg_left(), arm.emg_right(), 0.001):
        

def at_location(target):
    pos = arm.effector_position()
    if (f_equal(pos[0], target[0], 0.0001)
        and f_equal(pos[1], target[1], 0.0001)
        and f_equal(pos[2], target[2], 0.0001)): return True
    else: return False

def move_end_effctor(num):
    """if at_location(home): arm.move_arm(*pick_up)
    if at_location(pick_up): arm.move_arm(*drop_off)
    if at_location(drop_off): arm.move_arm(*home)"""

    if num==0: arm.move_arm(*pick_up)
    if num==1: arm.move_arm(*drop_off)
    if num==2: arm.move_arm(*home)

while True:
    if left_up():
        num = int(input())
        move_end_effctor(num)
        time.sleep(2)
        print(at_location(home), at_location(pick_up), at_location(drop_off))
