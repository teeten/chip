#!/usr/bin/python

import time, signal, sys
import Adafruit_PureIO.smbus as smbus

###############
## FUNCTIONS ##
###############

def cleanup(sig, ctx):
    print "\nbye"
    axp209.close()
    sys.exit(0)

AXP209_ADDR = 0x34

def power_status(pmu):
    return pmu.read_byte_data(AXP209_ADDR, 0x00)

def power_mode(pmu):
    return pmu.read_byte_data(AXP209_ADDR, 0x01)

# === ADC === #

ADC_BATT_V = 1 << 7
ADC_BATT_C = 1 << 6
ADC_ACIN_V = 1 << 5
ADC_ACIN_C = 1 << 4
ADC_VBUS_V = 1 << 3
ADC_VBUS_C = 1 << 2
ADC_TEMP   = 1 << 15

def adc_status(pmu):
    return pmu.read_word_data(AXP209_ADDR, 0x82)

def ison(status,flags):
    return True if status & flags else False

def adc_enable(pmu, flags):
    st = (adc_status(pmu) | flags) & 0xff
    pmu.write_byte_data(AXP209_ADDR, 0x82, st)
    return st

def has_vbus(pmu):
    return True if power_status(pmu) & (1 << 5) else False

def has_acin(pmu):
    return True if power_status(pmu) & (1 << 7) else False

def has_batt(pmu):
    return True if power_mode(pmu) & (1 << 5) else False

def batt_charging(pmu):
    return True if power_mode(pmu) & (1 << 6) else False

def batt_voltage(pmu): # 12-bits
    w = pmu.read_word_data(AXP209_ADDR, 0x78)
    return (((w & 0x00ff) << 4) | (w & 0x0f00) >> 8) * 0.0011

def batt_discharge(pmu): # 13-bits
    w = pmu.read_word_data(AXP209_ADDR, 0x7c)
    return (((w & 0x00ff) << 5) | (w & 0x1f00) >> 8) * 0.0005

##########
## MAIN ##
##########

signal.signal(signal.SIGINT, cleanup)

axp209 = smbus.SMBus(0, dangerous=True)

st = adc_status(axp209)

print("ADC status=%s BV=%s BC=%s AV=%s AC=%s VV=%s VC=%s" % (bin(st),
    ison(st, ADC_BATT_V),
    ison(st, ADC_BATT_C),
    ison(st, ADC_ACIN_V),
    ison(st, ADC_ACIN_C),
    ison(st, ADC_VBUS_V),
    ison(st, ADC_VBUS_C)))

adc_enable(axp209, ADC_BATT_C)

print("ADC status=%s" % bin(adc_status(axp209)))

print("POWER_STATUS = %s" % bin(power_status(axp209)))
print("\tVBUS=%s" % has_vbus(axp209))
print("\tACIN=%s" % has_acin(axp209))

print("POWER_MODE   = %s" % bin(power_mode(axp209)))
print("\tBATT=%s" % has_batt(axp209))
print("\tCHRG=%s" % batt_charging(axp209))

print("Battery voltage   = %1.4f" % batt_voltage(axp209))
print("Battery discharge = %1.4f" % batt_discharge(axp209))

axp209.close()
sys.exit(0)

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

