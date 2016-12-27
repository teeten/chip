#!/usr/bin/python

import time, signal, sys
import Adafruit_PureIO.smbus as smbus
import t10_axp209 as pmu

def cleanup(sig, ctx):
    print "\nbye"
    axp209.close()
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)

MAXCOUNT  = 20
countdown = MAXCOUNT
period    = 5
axp209    = smbus.SMBus(0, dangerous=False)
ts0       = time.time()

while 1:
    ts = time.time() - ts0
 
    power_out = not pmu.ison(pmu.power_status(axp209), pmu.HAS_ACIN)
    print("TIME=%04d POWER_OUT=%s COUNT=%d" % (ts, power_out, countdown))

    if (countdown == 0):
        axp209.close()
        print "shutdown"
        sys.exit(0)

    if (power_out):
        period = 1
        countdown -= 1
    else:
        period = 5
        countdown = MAXCOUNT

    time.sleep(period)
