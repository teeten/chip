#!/usr/bin/python

import time, signal, sys
import CHIP_IO.GPIO as GPIO
from axp209 import AXP209

def cleanup(sig, ctx):
    GPIO.output("XIO-P1", GPIO.HIGH)
    print "\nbye"
    axp.close()
    GPIO.cleanup()
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)

MAXCOUNT  = 20
countdown = MAXCOUNT
period    = 5
ts0       = time.time()

GPIO.setup("XIO-P1", GPIO.OUT)
GPIO.output("XIO-P1", GPIO.HIGH)

while 1:
    time.sleep(period)

    axp = AXP209()
    ts = time.time() - ts0
    
    print "TIME=%f S=%d ACIN=%f VBUS=%f BATT=%f DCHG=%f COUNT=%d" % (ts, axp.power_input_status.acin_available, 0, 0, 0, 0, countdown)

    if (countdown == 0):
        print "shutdown"
        cleanup()
        sys.exit(0)

    if (axp.power_input_status.acin_available == 0): # no power
        period = 1
        countdown -= 1
        GPIO.output("XIO-P1", GPIO.HIGH)
        time.sleep(0.1)
        GPIO.output("XIO-P1", GPIO.LOW)

    else:
        GPIO.output("XIO-P1", GPIO.HIGH)
        period = 5
        countdown = MAXCOUNT

