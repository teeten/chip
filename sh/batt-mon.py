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
    print "BATT=%d" % (axp("0x58") << 4 | axp("0x59"))
    time.sleep(2)
