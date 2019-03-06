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

mtrn = serial.Serial(port='/dev/cu.usbmodem1431',timeout=0, baudrate=9600);

mtrn.read(250);

time.sleep(2)
mtrn.read(250)

#mtrn.write('A3250')
time.sleep(0.2) # This time depends on the weight
#mtrn.write('A3000')
for i in range(1,5):
    mtrn.write('#0 P750 S40000 #1 P2200 S40000 #2 P1800 S40000 #3 P1250 S40000')
    mtrn.write(chr(13))
    time.sleep(1)
    mtrn.write('#0 P2200 S40000 #1 P750 S40000 #2 P1250 S40000 #3 P1800 S40000')
    mtrn.write(chr(13))
    time.sleep(1)

time.sleep(4)
mtrn.close()
