#!/usr/bin/python

import time, signal, sys
import CHIP_IO.GPIO as GPIO

def cleanup(sig, ctx):
    GPIO.output("XIO-P1", GPIO.HIGH)
    print "\nbye"
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)

GPIO.setup("XIO-P1", GPIO.OUT)

while 1:
    GPIO.output("XIO-P1", GPIO.HIGH)
    time.sleep(0.1)
    GPIO.output("XIO-P1", GPIO.LOW)
    time.sleep(0.1)

