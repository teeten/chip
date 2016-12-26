#!/usr/bin/python

import time
import subprocess

def axp(addr):
    p = subprocess.Popen(
      ["/usr/sbin/i2cget", "-f", "-y", "0", "0x34", addr],
      stdout=subprocess.PIPE
    )
    out, err = p.communicate()
    return int(out, 0)

while 1:
    acin_current = axp("0x58") << 4 | axp("0x59")
    vbus_current = axp("0x5c") << 4 | axp("0x5d")
    batt_current = axp("0x7c") << 4 | axp("0x7d")
    chrg_current = axp("0x7a") << 4 | axp("0x7b")
    print "ACIN=%04d VBUS=%04d BATT=%04d CHRG=%04d" % (acin_current, vbus_current, batt_current, chrg_current)
    time.sleep(2)


