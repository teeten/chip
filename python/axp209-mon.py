#!/usr/bin/python

import time, signal, sys
from axp209 import AXP209

def cleanup(sig, ctx):
    print "\nbye"
    axp.close()
    sys.exit(0)

signal.signal(signal.SIGINT, cleanup)

"""
POWER_INPUT_STATUS_REG = 0x00
POWER_OPERATING_MODE_REG = 0x01
CHARGE_CONTROL_REG = 0x33
CHARGE_CONTROL2_REG = 0x34
ADC_ENABLE1_REG = 0x82
INTERNAL_TEMPERATURE_MSB_REG = 0x5e
INTERNAL_TEMPERATURE_LSB_REG = 0x5f
BATTERY_VOLTAGE_MSB_REG = 0x78
BATTERY_VOLTAGE_LSB_REG = 0x79
BATTERY_CHARGE_CURRENT_MSB_REG = 0x7a
BATTERY_CHARGE_CURRENT_LSB_REG = 0x7b
BATTERY_DISCHARGE_CURRENT_MSB_REG = 0x7c
BATTERY_DISCHARGE_CURRENT_LSB_REG = 0x7d
GPIO0_FEATURE_SET_REG = 0x90
GPIO1_FEATURE_SET_REG = 0x92
GPIO2_FEATURE_SET_REG = 0x93
BATTERY_GAUGE_REG = 0xb9
"""

axp = AXP209()

while 1:
    print("EN=%02x PW=%02x/%02x BV=%1.4f [%d%%] BC=%1.1f/%1.1f TEMP=%4.1f ACIN=%1.1f VBUS=%1.1f" % (
        axp.adc_enable1.asbyte,
        axp.power_input_status.asbyte,
        axp.power_operating_mode.asbyte,
        axp.battery_voltage,
        axp.battery_gauge,
        axp.battery_charge_current,
        axp.battery_discharge_current,
        axp.internal_temperature,
        0, 0 ))
    time.sleep(1)

