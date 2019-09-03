#coding: latin-1

# NeoCortex is the core program to control Cheetahbot
# It handles basic USB-Serial comm with other modules and handles
# the basic operation of ShinkeyBot
#
# x) Transmit TCP/IP images through CameraStreamer.
# x) Captures sensor data from SensorimotorLogger
# x) Handles output to motor unit and sensorimotor commands through Proprioceptive
# x) Receives high-level commands from BotController.

import numpy as np
import cv2

import serial

import time
import datetime
from struct import *

import sys, os, select

import socket

import Proprioceptive as prop
import thread
import os
import sys
import platform
system_platform = platform.system()
if system_platform == "Darwin":
    import FFMPegStreamer as pcs
else:
    import H264Streamer as pcs
import SensorimotorLogger as senso
import MCast
import Surrogator as Surrogator

import fcntl
import struct

from Fps import Fps

# First create a witness token to guarantee only one instance running
if (os.access("running.wt", os.R_OK)):
    print >> sys.stderr, 'Another instance is running. Cancelling.'
    quit(1)

runningtoken = open('running.wt', 'w')
ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')

runningtoken.write(st)
runningtoken.close()

def get_ip_address(ifname):
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    try:
        ip = socket.inet_ntoa(fcntl.ioctl(
            s.fileno(),
            0x8915,  # SIOCGIFADDR
            struct.pack('256s', ifname[:15])
        )[20:24])
        return ip
    except:
        return ''

# Ok, so the first thing to do is to broadcast my own IP address.
dobroadcastip = True
dosomestreaming = True

# Get PiCamera stream and read everything in another thread.
vst = pcs.H264VideoStreamer()
if (dosomestreaming):
    try:
        vst.startAndConnect()
        pass
    except:
        pass

# Open connection to tilt sensor (@deprecated)
#hidraw = prop.setupsensor()
# Open serial connection to MotorUnit and Sensorimotor Arduinos.
def doserial():
    retries=1
    ssmr=None
    mtrn=None
    while (retries<5):
        try:
            if system_platform == "Darwin":
                [ssmr, mtrn] = prop.serialcomm('/dev/cu.usbmodem14101')
            else:
                [ssmr, mtrn] = prop.serialcomm()
            print 'Connection established'
            return [ssmr, mtrn]
        except Exception as e:
            print 'Error while establishing serial connection.'
            retries=retries+1

    return [ssmr, mtrn]

[ssmr, mtrn] = doserial()

if (ssmr == None and mtrn == None):
    quit()

# Initialize UDP Controller Server on port 10001 (ShinkeyBotController)
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = ('0.0.0.0', 10001)
print >> sys.stderr, 'Starting up Controller Server on %s port %s', server_address
sock.bind(server_address)

if (dobroadcastip):
    sock.setblocking(0)
    sock.settimeout(0.01)

noticer = MCast.Sender()

# Fixme push the network name inside the configuration file.
myip = get_ip_address('wlan0')

if (len(myip)>0):
    myip = myip
else:
    myip = 'None'

# Shinkeybot truly does nothing until it gets connected to ShinkeyBotController
def broadcastingme(dobroadcastip,noticer, sck,myipaddress):
    whenistarted = time.time()
    print 'Multicasting my own IP address:' + myipaddress
    while dobroadcastip:
        noticer.send()
        try:
            data, address = sck.recvfrom(1)
            if (len(data)>0):
                break
        except:
            data = None

        if (abs(time.time()-whenistarted)>60):
            print 'Giving up broadcasting ip... Lets get started.'
            break

broadcastingme(dobroadcastip,noticer,sock,myip)

from threading import Timer

def timeout():
    print 'Sending a multicast update of my own ip address:'+myip
    noticer.send()

# FIXME: Once running, the multicast breaks the UDP receiving socket.
t = Timer(500 * 60, timeout)
t.start()

if (dobroadcastip):
    sock.setblocking(1)
    sock.settimeout(0)

print 'Connection to Remote Controller established.'

def terminateme():
    try:
        t.cancel()
        print 'Thread successfully closed.'
    except Exception as e:
        print 'Exception while closing video stream thread.'
        traceback.print_exc(file=sys.stdout)

    os.remove('running.wt')
    print 'ShinkeyBot has stopped.'


if (ssmr == None and mtrn == None):
    terminateme()


tgt = -300

# Pan and tilt
visualpos = [60,150,90]

# Enables the sensor telemetry.  Arduinos will send telemetry data that will be
#  sent to listening servers.
sensesensor = False

# Connect remotely to any client that is waiting for sensor loggers.
sensorimotor = senso.Sensorimotor('sensorimotor',40,'fiiihhhhhhhhhhhh')
sensorimotor.start()
sensorimotor.init(ssmr)
sensorimotor.sensorlocalburst=100
sensorimotor.sensorburst=10
sensorimotor.updatefreq=5
sensorimotor.cleanbuffer(ssmr)

sur = Surrogator.Surrogator(sock)


target = [0,0,0]

speed=50

fps = Fps()
fps.tic()

ts = time.time()
st = datetime.datetime.fromtimestamp(ts).strftime('%Y-%m-%d-%H-%M-%S')
runninglog = open('../data/brainstem.'+st+'.dat', 'w')

whenreceivedcommand = time.time()

# Live
while(True):
    try:
        fps.steptoc()
        ts = int(time.time())
        runninglog.write(str(ts) + ',' + str(fps.fps) + '\n')
        #print "Estimated frames per second: {0}".format(fps.fps)
        data = ''
        # TCP/IP server is configured as non-blocking
        sur.getmessage()
        data, address = sur.data, sur.address

        # If someone asked for it, send sensor information.
        if (sensesensor):
            sens = sensorimotor.picksensorsample(ssmr)
            mots = None

            if (sens != None):
                # Check where to put the value
                sensorimotor.repack([0],[fps.fps])
                sensorimotor.send(sensorimotor.data)

        else:
            # Check why I am not receiving anything from a while and shift towards
            # IP broadcasting again  # FIXME
            if (abs(time.time()-whenreceivedcommand)>60000):
                print 'Sending a multicast of my own ip address:'+myip
                broadcastingme(dobroadcastip,noticer,sock,myip)
                

        if (sur.command != None and len(sur.command)>0):
            # Something was received
            whenreceivedcommand = time.time()

        if (sur.command == 'A'):
            if (len(sur.message)==5):
                # Sending the message that was received.
                ssmr.write(sur.message)
                sur.message = ''

        elif (sur.command == 'U'):
            if (data == '!'):
                # IP Address exchange.
                sensorimotor.ip = address[0]
                sensorimotor.restart()

                print "Reloading target ip for telemetry:"+sensorimotor.ip

                # Vst VideoStream should be likely restarted in order to check
                # if something else can be enabled.

            if (data=='1'):
                ssmr.write('A9018')
            elif (data=='2'):
                ssmr.write('A9082')
            elif (data=='3'):
                ssmr.write('A9170')
            if (data == 'Q'):
                # Activate/Deactivate sensor data.
                sensesensor = True
            elif (data == 'q'):
                sensesensor = False
            elif (data=='P'):
                ssmr.write('P')
            elif (data=='W'):
                ssmr.write('A3'+'{:3d}'.format(speed))
            elif (data=='S'):
                ssmr.write('A4'+'{:3d}'.format(speed))
            elif (data=='A'):
                ssmr.write('A1'+'{:3d}'.format(50))
            elif (data=='D'):
                ssmr.write('A2'+'{:3d}'.format(50))
            elif (data==' '):
                print("Stopping...")
                if (speed<120):
                    ssmr.write('A3010')
                    ssmr.write('A3000')
                    ssmr.write('A0000')
            elif (data=='H'):
                ssmr.write('=')
            elif (data==';'):
                speed = speed - 50
                if (speed<50):
                    speed = 50
                ssmr.write('A3'+'{:3d}'.format(speed))
            elif (data==','):
                speed = speed + 50
                if (speed>250):
                    speed = 250
            elif (data=='.'):
                speed = 50
            elif (data=='{'):
                # Camera left
                visualpos[0]=visualpos[0]+1;
                ssmr.write('A8'+'{:3d}'.format(visualpos[0]))
            elif (data=='}'):
                # Camera right
                visualpos[0]=visualpos[0]-1;
                ssmr.write('A8'+'{:3d}'.format(visualpos[0]))
            elif (data=='['):
                # Nose down
                visualpos[1]=visualpos[1]-1;
                ssmr.write('A7'+'{:3d}'.format(visualpos[1]))
            elif (data==']'):
                # Nose up
                visualpos[1]=visualpos[1]+1;
                ssmr.write('A7'+'{:3d}'.format(visualpos[1]))
            elif (data=='<'):
                # Nose down
                visualpos[2]=visualpos[2]-1;
                ssmr.write('A9'+'{:3d}'.format(visualpos[2]))
            elif (data=='>'):
                # Nose up
                visualpos[2]=visualpos[2]+1;
                ssmr.write('A9'+'{:3d}'.format(visualpos[2]))
            elif (data=='K'):
                ssmr.write('K')
            elif (data=='O'):
                ssmr.write('O')
            elif (data=='='):
                ssmr.write('=')
            elif (data=='R'):
                raise Exception('Restarting serial connection...')
            elif (data=='('):
                sensorimotor.sensorlocalburst = 100
            elif (data==')'):
                sensorimotor.sensorlocalburst = 10000
            elif (data=='X'):
                break
    except Exception as e:
        print "Error:" + e.message
        print "Waiting for serial connection to reestablish..."
        if (not ssmr == None):
            ssmr.close()
        if (not mtrn == None):
            mtrn.close()
        [ssmr, mtrn] = doserial()

        # Instruct the Sensorimotor Cortex to stop wandering.
        if (ssmr != None):
            sensorimotor.flush(ssmr)
            sensorimotor.cleanbuffer(ssmr)

vst.keeprunning = False
sur.keeprunning = False
time.sleep(2)

ssmr.write(' ')


#When everything done, release the capture
if (not ssmr == None):
    ssmr.close()
sock.close()
if (not mtrn == None):
    mtrn.close()

terminateme()
