#coding: latin-1

# NeoCortex is the core program to control ShinkeyBot
# It handles basic USB-Serial comm with other modules and handles
# the basic operation of ShinkeyBot
#
# x) Transmit TCP/IP images through CameraStreamer.
# x) Captures sensor data from SensorimotorLogger
# x) Handles output to motor unit and sensorimotor commands through Proprioceptive
# x) Receives high-level commands from ShinkeyBotController.

import numpy as np
import cv2

import serial

import time
from struct import *

import sys, os, select

import socket

import thread
import Proprioceptive as prop

ANKLE_FRONT_RIGHT=3
ANKLE_FRONT_LEFT=2
ANKLE_BACK_RIGHT=1
ANKLE_BACK_LEFT=0

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

    cmd = '#'+'{:1d}'.format(joint)+' '+'P'+'{:03d}'.format(microseconds)+' '+'S4000'
    return cmd


mtrn = serial.Serial(port='/dev/cu.usbmodem1431',timeout=0, baudrate=9600);

mtrn.read(250);

time.sleep(2)
mtrn.read(250)

#mtrn.write('A3250')
time.sleep(0.2) # This time depends on the weight
#mtrn.write('A3000')

if (False):
    for i in range(1,5):
        mtrn.write('#0 P750 S40000 #1 P2200 S40000 #2 P1800 S40000 #3 P1250 S40000')
        mtrn.write(chr(13))
        time.sleep(1)
        mtrn.write('#0 P2200 S40000 #1 P750 S40000 #2 P1250 S40000 #3 P1800 S40000')
        mtrn.write(chr(13))
        time.sleep(1)


for i in range(1,5):
    mtrn.write('#0 P1400 S40000 #1 P1350 S40000 #2 P2000 S40000 #3 P1050 S40000')
    mtrn.write(chr(13))
    time.sleep(1)
    mtrn.write('#4 P1800 S40000 #5 P1200 S40000 #6 P1800 S40000 #7 P1400 S40000')
    mtrn.write(chr(13))
    time.sleep(1)

# Move front left
for i in range(1,5):
    mtrn.write('#5 P2300 S4000 #2 P2200 S4000')
    mtrn.write(chr(13))
    time.sleep(1)
    mtrn.write('#2 P1700 S4000')
    mtrn.write(chr(13))
    time.sleep(1)
    mtrn.write('#5 P1200 S4000')
    mtrn.write(chr(13))
    time.sleep(1)

# Move the rest forward
for i in range(1,2):
    mtrn.write('#0 P1600 S400 #1 P1250 S400 #3 P850 S000')
    mtrn.write(chr(13))
    time.sleep(1)

# Move
for i in range(1,5):
    mtrn.write('#7 P2400 S4000 #1 750 S4000')
    mtrn.write(chr(13))
    time.sleep(1)
    mtrn.write('#1 P2000 S4000')
    mtrn.write(chr(13))
    time.sleep(1)
    mtrn.write('#7 P1400 S4000')
    mtrn.write(chr(13))
    time.sleep(1)

print (moveleg(0,80))
print (moveleg(1,84))
print (moveleg(2,156))
print (moveleg(3,152))
print (moveleg(4,126))
print (moveleg(5,125))
print (moveleg(6,130))
print (moveleg(7,105))


time.sleep(4)
mtrn.close()
