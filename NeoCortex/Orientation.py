#coding: latin-1
import numpy as np
import cv2

import socket

import time

import MCast

import Configuration
import ConfigMe

import os

import datetime
from struct import *

import sys, select

import Queue

from TelemetryDictionary import telemetrydirs

class Cmd:
    def __init__(self,cmd,dl):
        self.cmd = cmd
        self.delay = dl

class Asynctimer:
    def set(self,delay):
        self.delay = delay
        self.counter = 0
    def check(self):
        self.counter = self.counter + 1
        if (self.counter>self.delay):
            return True
        else:
            return False


socktelemetry = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
svaddress = ('0.0.0.0', Configuration.telemetryport)
print >> sys.stderr, 'starting up on %s port %s', svaddress

socktelemetry.bind(svaddress)
#socktelemetry.setblocking(0)
#socktelemetry.settimeout(0.01)

length = 40
unpackcode = 'fiiihhhhhhhhhhhh'

sockcmd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

lastip = ConfigMe.readconfig("config.ini")
server_address = (lastip, Configuration.controlport)

def sendmulticommand(cmd,times):
    for i in range(1,times):
        sent = sockcmd.sendto(cmd, server_address)

# Let the Brainstem release the robot.
for i in range(1,100):
    sent = sockcmd.sendto(' ', server_address)

time.sleep(10)

for i in range(1,2):
    print('Letting know Bot that I want telemetry.')
    sent = sockcmd.sendto('!', server_address)

sent = sockcmd.sendto('UQ000', server_address)

print '>'

state = 0

dst = [0,0,0]

olddst = dst

t = Asynctimer()
t.set(10)
delay=10

sd = Asynctimer()
sd.set(20)

q = Queue.Queue()

accencoder1 = 0
accencoder2 = 0

while (True):

    data, address = socktelemetry.recvfrom(length)
    myByte = 'E'
    if myByte == 'E' and len(data)>0 and len(data) == length:
        # is  a valid message struct
        new_values = unpack(unpackcode,data)
        #new_values = unpack('ffffffhhhhhhhhhh', data)
        print str(new_values)


    # Analyze incoming data...
    data = ''

    distance = new_values[3]
    angle = new_values[14]

    print (distance)
    print (angle)

    if (angle<30 and distance>0):
        dst[0] = distance
    elif ((angle>=79 and angle<=90) and distance>0):
        dst[1] = distance
    elif (angle>115 and distance>0):
        dst[2] = distance

    print dst

    print(new_values[telemetrydirs['encoder1']])
    print(new_values[telemetrydirs['encoder2']])

    if ((new_values[telemetrydirs['encoder1']]<0 and new_values[telemetrydirs['encoder2']]>0) or (new_values[telemetrydirs['encoder1']]>0 and new_values[telemetrydirs['encoder2']]<0)):
        accencoder1 = accencoder1 + new_values[telemetrydirs['encoder1']]
        accencoder2 = accencoder2 + new_values[telemetrydirs['encoder2']]

    print((accencoder1 % 2300)*360.0/2299)
    print((accencoder2 % 2300)*360.0/2299)

    # if (dst[1] < 20):
    #     sendmulticommand('US000',2)
    # else:
    #     sendmulticommand('U 000',2)

    if (len(data)>0 and t.check()):
        # Determine action command and send it.
        sent = sockcmd.sendto(data, server_address)

    if (data.startswith('!')):
      print "Letting know Bot that I want streaming...."

    if (data.startswith('X')):
      break

print "Insisting...."
for i in range(1,100):
    sent = sockcmd.sendto(data, server_address)

sockcmd.close()
