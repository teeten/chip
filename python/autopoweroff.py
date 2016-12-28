#!/usr/bin/python

import time, signal, sys, syslog, os
import Adafruit_PureIO.smbus as smbus
import t10_axp209 as pmu

def bye(sig, ctx):
    syslog.syslog("signal %d caught, terminating ..." % sig)
    axp209.close()
    sys.exit(0)

syslog.openlog("autopoweroffd", syslog.LOG_PID, syslog.LOG_DAEMON)
syslog.syslog("init")

signal.signal(signal.SIGINT, bye)
signal.signal(signal.SIGTERM, bye)

MAXCOUNT  = 20
countdown = MAXCOUNT
period    = 5
axp209    = smbus.SMBus(0)

syslog.syslog("start")

while 1:
    power_out = not pmu.ison(pmu.power_status(axp209), pmu.HAS_ACIN)
    if (countdown == 0):
        syslog.syslog("timeout reached, shutting down ...")
        axp209.close()
        os.system("init 0")
    if (power_out):
        if (countdown == MAXCOUNT):
            syslog.syslog("power out detected")
            period = 1
        countdown -= 1
    else:
        if (countdown != MAXCOUNT):
            syslog.syslog("power is back on (%ds from timeout)" % countdown)
            period = 5
            countdown = MAXCOUNT
    time.sleep(period)
