#!/usr/bin/python

import sys
import time
import subprocess

MAXCOUNT  = 20
countdown = MAXCOUNT
period    = 5
ts0       = time.time()

def axp(addr):
    p = subprocess.Popen(
      ["/usr/sbin/i2cget", "-f", "-y", "0", "0x34", addr],
      stdout=subprocess.PIPE
    )
    out, err = p.communicate()
    return int(out, 0)

while 1:

    ts = time.time() - ts0
    time.sleep(period)
    acin_current = axp("0x58") << 4 | axp("0x59")
    vbus_current = axp("0x5c") << 4 | axp("0x5d")
    batt_current = axp("0x7c") << 4 | axp("0x7d")

    print "TIME=%06d ACIN=%04d VBUS=%04d BATT=%04d COUNT=%d" % (ts, acin_current, vbus_current, batt_current, countdown)

    if (countdown == 0):
        print "shutdown"
        sys.exit(0)

    if (vbus_current > 200):
        period = 1
        countdown -= 1
    else:
        period = 5
        countdown = MAXCOUNT


