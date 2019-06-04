#coding: latin-1

import serial
import time
import datetime
from struct import *
import os

import socket
import sys

import Proprioceptive as prop

import Configuration

from Fps import Fps

import SensorimotorLogger as Senso

if __name__ == "__main__":
    [ssmr, mtrn] = prop.serialcomm('/dev/cu.usbmodem14101')

    # Weird, long values (4) should go first.
    #sensorimotor = Sensorimotor('motorneuron',26,'hhffffhhh')
    sensorimotor = Senso.Sensorimotor('sensorimotor',40,'ffffhhhhhhhhhhhh')
    sensorimotor.sensorlocalburst=100
    sensorimotor.sensorburst=10
    sensorimotor.updatefreq=10
    sensorimotor.ip = sys.argv[1]
    sensorimotor.start()
    sensorimotor.init(ssmr)
    print (sensorimotor.mapping)
    print (sensorimotor.length)
    sensorimotor.cleanbuffer(ssmr)

    fps = Fps()
    fps.tic()

    while True:
        fps.steptoc()
        sens = sensorimotor.picksensorsample(ssmr)
        mots = None
        if (sens != None):
            sensorimotor.repack([0],[fps.fps])
            sensorimotor.send(sensorimotor.data)
