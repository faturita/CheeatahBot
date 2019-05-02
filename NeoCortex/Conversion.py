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

print (moveleg(0,80))
print (moveleg(1,84))
print (moveleg(2,156))
print (moveleg(3,152))
print (moveleg(4,126))
print (moveleg(5,125))
print (moveleg(6,130))
print (moveleg(7,105))
