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

length = 36
unpackcode = 'iiihhhhhhhhhhhh'

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

sent = sockcmd.sendto('Q', server_address)

print '>'

state = 0

dst = [0,0,0]

t = Asynctimer()
t.set(10)
delay=10

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

    distance = new_values[2]
    angle = new_values[13]

    print (distance)
    print (angle)

    if (angle==10 and distance>0):
        dst[0] = distance
    elif ((angle>=85 and angle<=95) and distance>0):
        dst[1] = distance
    elif (angle>115 and distance>0):
        dst[2] = distance

    print dst

    if (state == 0 and t.check()):
        sendmulticommand('1',2)

        if (angle<30):
            state = 1
            t.set(delay)
    elif (state == 1 and t.check()):
        sendmulticommand('K',2)
        state = 2
        t.set(delay)
    elif (state == 2 and t.check()):
        sendmulticommand('2',2)

        if (angle>=89 and angle<=91):
            state = 3
            t.set(delay)
    elif (state == 3 and t.check()):
        sendmulticommand('K',2)
        state = 4
        t.set(delay)

    elif (state == 4 and t.check()):
        sendmulticommand('3',2)

        if (angle>160):
            state = 5
            t.set(delay)
    elif (state == 5 and t.check()):
        sendmulticommand('K',2)
        state = 0
        t.set(delay)


    # if (state == 0 and t.check()):
    #     sendmulticommand('<',7)
    #
    #     if (angle<30):
    #         state = 1
    #         t.set(delay)
    # elif (state == 1 and t.check()):
    #     sendmulticommand('K',2)
    #     state = 2
    #     t.set(delay)
    # elif (state == 2 and t.check()):
    #     sendmulticommand('>',7)
    #
    #     if (angle<85):
    #         sendmulticommand('>',2)
    #
    #     if (angle>95):
    #         sendmulticommand('<',2)
    #
    #     if (angle>85 and angle<95):
    #         state = 3
    #         t.set(delay)
    # elif (state == 3 and t.check()):
    #     sendmulticommand('K',2)
    #     state = 4
    #     t.set(delay)
    #
    # elif (state == 4 and t.check()):
    #     sendmulticommand('>',7)
    #
    #     if (angle>140):
    #         state = 5
    #         t.set(delay)
    # elif (state == 5 and t.check()):
    #     sendmulticommand('K',2)
    #     state = 0
    #     t.set(delay)

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

sock.close()
