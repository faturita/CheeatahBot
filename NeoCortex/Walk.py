#coding: latin-1

# https://wiki.dfrobot.com/Veyron_Servo_Driver__24-Channel___SKU_DRI0029_

import numpy as np
import cv2

import serial

import time
from struct import *

import sys, os, select

import socket

import thread
import Proprioceptive as prop

state = [0,0,0,0,0,0,0,0]

HIP_FRONT_RIGHT=3
HIP_FRONT_LEFT=2
HIP_BACK_RIGHT=1
HIP_BACK_LEFT=0

KNEE_FRONT_RIGHT=4
KNEE_FRONT_LEFT=5
KNEE_BACK_RIGHT=7
KNEE_BACK_LEFT=6

def sgn(val):
    if (val >= 0):
        return 1
    else:
        return -1

def moveleg(joint,angle):
    microseconds=0
    if (joint == 0):
        min=750
        max=2200
    elif (joint == 1):
        min=-2200
        max=-750
    elif (joint == 2):
        min=750
        max=2200
    elif (joint == 3):
        min=-2200
        max=-750
    elif (joint == 4):
        min=690
        max=2300
    elif (joint == 5):
        min=-2300
        max=-690
    elif (joint == 6):
        min = 690
        max=2300
    elif (joint == 7):
        min=-2500
        max=-690

    microseconds = (min + angle * 1.0 * (max - min) / 180.0) * sgn(min)

    microseconds = int(microseconds)

    print (microseconds)
    state[joint] = angle

    cmd = '#'+'{:1d}'.format(joint)+' '+'P'+'{:03d}'.format(microseconds)+' '+'S4000'
    return cmd

def domoveleg(mtrn,leg, angle, delay=1):
    mtrn.write(moveleg(leg,angle))
    mtrn.write(chr(13))
    time.sleep(delay)

def stand(mtrn):
    mtrn.write(moveleg(HIP_BACK_LEFT,140))
    mtrn.write(moveleg(HIP_BACK_RIGHT,140))
    mtrn.write(moveleg(HIP_FRONT_LEFT,150))
    mtrn.write(moveleg(HIP_FRONT_RIGHT,150))
    mtrn.write(moveleg(KNEE_FRONT_LEFT,100))
    mtrn.write(moveleg(KNEE_FRONT_RIGHT,90))
    mtrn.write(moveleg(KNEE_BACK_LEFT,155))
    mtrn.write(moveleg(KNEE_BACK_RIGHT,155))
    mtrn.write(chr(13))
    time.sleep(1)


def step(mtrn,j1,j2):
    val = state[j1]
    domoveleg(mtrn,j1,0)
    domoveleg(mtrn,j2,state[j2]-10)
    domoveleg(mtrn,j1,val)
    domoveleg(mtrn,j2,state[j2]+20)

def stepfast(mtrn,j1,j2):
    val = state[j1]
    domoveleg(mtrn,j1,val-10        ,0.5)
    domoveleg(mtrn,j2,state[j2]-10  ,0.5)
    domoveleg(mtrn,j1,val           ,0.5)
    domoveleg(mtrn,j2,state[j2]+10  ,0.5)


mtrn = serial.Serial(port='/dev/cu.usbmodem1411',timeout=0, baudrate=9600);

mtrn.read(250);

time.sleep(2)
mtrn.read(250)

#mtrn.write('A3250')
time.sleep(0.2) # This time depends on the weight
#mtrn.write('A3000')

# if (False):
#     for i in range(1,5):
#         mtrn.write('#0 P750 S40000 #1 P2200 S40000 #2 P1800 S40000 #3 P1250 S40000')
#         mtrn.write(chr(13))
#         time.sleep(1)
#         mtrn.write('#0 P2200 S40000 #1 P750 S40000 #2 P1250 S40000 #3 P1800 S40000')
#         mtrn.write(chr(13))
#         time.sleep(1)
#
#
# for i in range(1,5):
#     mtrn.write('#0 P1400 S40000 #1 P1350 S40000 #2 P2000 S40000 #3 P1050 S40000')
#     mtrn.write(chr(13))
#     time.sleep(1)
#     mtrn.write('#4 P1800 S40000 #5 P1200 S40000 #6 P1800 S40000 #7 P1400 S40000')
#     mtrn.write(chr(13))
#     time.sleep(1)
#
# # Move front left
# for i in range(1,5):
#     mtrn.write('#5 P2300 S4000 #2 P2200 S4000')
#     mtrn.write(chr(13))
#     time.sleep(1)
#     mtrn.write('#2 P1700 S4000')
#     mtrn.write(chr(13))
#     time.sleep(1)
#     mtrn.write('#5 P1200 S4000')
#     mtrn.write(chr(13))
#     time.sleep(1)
#
# # Move the rest forward
# for i in range(1,2):
#     mtrn.write('#0 P1600 S400 #1 P1250 S400 #3 P850 S000')
#     mtrn.write(chr(13))
#     time.sleep(1)
#
# #Move
# for i in range(1,5):
#     mtrn.write('#7 P2400 S4000 #1 P1100 S4000')
#     mtrn.write(chr(13))
#     time.sleep(1)
#     mtrn.write('#1 P1350 S4000')
#     mtrn.write(chr(13))
#     time.sleep(1)
#     mtrn.write('#7 P1400 S4000')
#     mtrn.write(chr(13))
#     time.sleep(1)
#
# print (moveleg(0,80))
# print (moveleg(1,84))
# print (moveleg(2,156))
# print (moveleg(3,152))
# print (moveleg(4,126))
# print (moveleg(5,125))
# print (moveleg(6,130))
# print (moveleg(7,105))
#
# #mtrn.write(moveleg(0,80)+moveleg(1,84)+moveleg(2,156)+moveleg(3,152))
# #mtrn.write(moveleg(4,126)+moveleg(5,125)+moveleg(6,130)+moveleg(7,105))
# #mtrn.write(chr(13))
#
# for i in range(1,5):
#     mtrn.write('#0 P1400 S40000 #1 P1350 S40000 #2 P2000 S40000 #3 P1050 S40000')
#     mtrn.write(chr(13))
#     time.sleep(1)
#     mtrn.write('#4 P1600 S40000 #5 P1300 S40000 #6 P1800 S40000 #7 P1400 S40000')
#     mtrn.write(chr(13))
#     time.sleep(1)

def dowalk(mtrn):
    stepfast(mtrn,KNEE_BACK_RIGHT,HIP_BACK_RIGHT)
    stepfast(mtrn,KNEE_BACK_LEFT,HIP_BACK_LEFT)

stand(mtrn)
step(mtrn,KNEE_FRONT_LEFT,HIP_FRONT_LEFT)
stepfast(mtrn,KNEE_BACK_RIGHT,HIP_BACK_RIGHT)
step(mtrn,KNEE_FRONT_RIGHT,HIP_FRONT_RIGHT)
stepfast(mtrn,KNEE_BACK_LEFT,HIP_BACK_LEFT)
stand(mtrn)

time.sleep(4)
mtrn.close()
