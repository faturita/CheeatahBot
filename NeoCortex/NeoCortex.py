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

    if (angle<85 and distance>0):
        dst[0] = distance
    elif ((angle>85 or angle<95) and distance>0):
        dst[1] = distance
    elif (angle>95 and distance>0):
        dst[2] = distance

    if (dst[0]>0 and dst[1]>0 and dst[2]>0):
        print dst

    if (state == 0):
        sendmulticommand('<',4)

        if (angle<40):
            state = 1
    elif (state == 1):
        sendmulticommand('K',5)
        state = 2
    elif (state == 2):
        sendmulticommand('>',4)

        if (angle>120):
            state = 3
    elif (state == 3):
        sendmulticommand('K',5)
        state = 0

    if (len(data)>0):
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
