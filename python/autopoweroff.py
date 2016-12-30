#!/usr/bin/python

#############
## IMPORTS ##
#############

import time, signal, sys, syslog, os, lockfile.pidlockfile
import Adafruit_PureIO.smbus as smbus

#import daemon, systemd.daemon

###############
## CONSTANTS ##
###############

DAEMONNAME    = "autopoweroffd"
AXP209_ADDR   = 0x34
AXP209_STATUS = 0x00
HAS_ACIN      = 1 << 7
HAS_VBUS      = 1 << 5

TIMEOUT = 20 # grace period before power off, in seconds

###############
## FUNCTIONS ##
###############

def bye(sig, ctx):
    syslog.syslog("signal %d caught, terminating ..." % sig)
    i2cbus.close()
    sys.exit(0)

def run():
    syslog.syslog("run")
    countdown = TIMEOUT
    period    = 5

#    systemd.daemon.notify("READY=1")

    while 1:
        if (i2cbus.read_word_data(AXP209_ADDR, AXP209_STATUS) & (HAS_ACIN | HAS_VBUS)): # ACIN or VBUS power is up
            if (countdown != TIMEOUT):
                syslog.syslog("power is back on (%ds from timeout)" % countdown)
                period = 5
                countdown = TIMEOUT
        else: # ACIN power is down
            if (countdown == TIMEOUT):
                syslog.syslog("power out detected")
                period = 1
            countdown -= 1
        if (countdown == 0):
            syslog.syslog("timeout reached, shutting down ...")
            i2cbus.close()
            os.system("init 0")
        time.sleep(period)

##########
## MAIN ##
##########

signal.signal(signal.SIGINT, bye)
signal.signal(signal.SIGTERM, bye)

syslog.openlog(DAEMONNAME, syslog.LOG_PID, syslog.LOG_DAEMON)
syslog.syslog("init")

i2cbus = smbus.SMBus(0)
syslog.syslog("device=%s" % i2cbus._device)

pidfile = lockfile.pidlockfile.PIDLockFile("/run/%s.pid" % DAEMONNAME)

run()

"""
context = daemon.DaemonContext(
    signal_map        = { signal.SIGINT:bye, signal.SIGTERM:bye, signal.SIGHUP:bye },
    working_directory = "/var/local",
    umask             = 0o002,
    pidfile           = pidfile,
    files_preserve    = [i2cbus._device]
)

with context:
    run()
"""
