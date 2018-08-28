#coding: latin-1
import numpy as np
import cv2

import socket
import sys

import time

import MCast

import Configuration
import ConfigParser
import io

import os


socktelemetry = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
svaddress = ('0.0.0.0', Configuration.telemetryport)
print >> sys.stderr, 'starting up on %s port %s', svaddress

socktelemetry.bind(svaddress)
length = 36
unpackcode = 'iiihhhhhhhhhhhh'

sockcmd = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

server_address = ('10.17.64.215', Configuration.controlport)

# Let the Brainstem release the robot.
for i in range(1,100):
    sent = sockcmd.sendto(' ', server_address)

time.sleep(10)

for i in range(1,2):
    print('Letting know Bot that I want telemetry.')
    sent = sockcmd.sendto('!', server_address)

sent = sockcmd.sendto('Q', server_address)

while (True):
    print '>'

    data, address = socktelemetry.recvfrom(length)
    myByte = 'E'
    if myByte == 'E' and len(data)>0 and len(data) == length:
        # is  a valid message struct
        new_values = unpack(unpackcode,data)
        #new_values = unpack('ffffffhhhhhhhhhh', data)
        print str(new_values)

    # Analyze incoming data...
    data = ''


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
