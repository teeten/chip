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

# === generic === #

def ison(status,flags):
    return True if status & flags else False

# === power status === #

PWR_HAS_ACIN  = 1 << 7
PWR_HAS_VBUS  = 1 << 5
PWR_HAS_BATT  = 1 << 13
PWR_BATT_FULL = 1 << 14
PWR_BATT_CHRG = 1 << 2

def power_status(pmu):
    return pmu.read_word_data(AXP209_ADDR, 0x00)

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

def adc_enable(pmu, flags):
    st = (adc_status(pmu) | flags) & 0xff
    pmu.write_byte_data(AXP209_ADDR, 0x82, st)
    return st

def adc_disable(pmu, flags):
    st = (adc_status(pmu) & ~flags) & 0xff
    pmu.write_byte_data(AXP209_ADDR, 0x82, st)
    return st

def has_vbus(pmu):
    return True if power_status(pmu) & (1 << 5) else False

def has_acin(pmu):
    return True if power_status(pmu) & (1 << 7) else False

def has_batt(pmu):
    return True if power_mode(pmu) & (1 << 5) else False

def batt_voltage(pmu): # 12-bits
    w = pmu.read_word_data(AXP209_ADDR, 0x78)
    return (((w & 0x00ff) << 4) | (w & 0x0f00) >> 8) * 0.0011

def batt_current(pmu):
    if not ison(power_status(pmu), PWR_BATT_FULL):
        w = pmu.read_word_data(AXP209_ADDR, 0x7c)
        return (((w & 0x00ff) << 5) | (w & 0x1f00) >> 8) * 0.0005
    else:
        w = pmu.read_word_data(AXP209_ADDR, 0x7a)
        return (((w & 0x00ff) << 4) | (w & 0x0f00) >> 8) * -0.0005

def batt_gauge(pmu):
    return pmu.read_byte_data(AXP209_ADDR, 0xb9)

# === display === #

def show_status(status):
    print("ADC status=%s BV=%s BC=%s AV=%s AC=%s VV=%s VC=%s" % (bin(status),
        ison(status, ADC_BATT_V),
        ison(status, ADC_BATT_C),
        ison(status, ADC_ACIN_V),
        ison(status, ADC_ACIN_C),
        ison(status, ADC_VBUS_V),
        ison(status, ADC_VBUS_C)))

##########
## MAIN ##
##########

signal.signal(signal.SIGINT, cleanup)

axp209 = smbus.SMBus(0, dangerous=True)

pwr = power_status(axp209)

print("POWER_STATUS = %s" % bin(pwr))
print("\tVBUS=%s" % ison(pwr, PWR_HAS_VBUS))
print("\tACIN=%s" % ison(pwr, PWR_HAS_ACIN))
print("\tBATT=%s FULL=%s CHARGING=%s\n" % (ison(pwr, PWR_HAS_BATT), not ison(pwr, PWR_BATT_FULL), ison(pwr, PWR_HAS_BATT)))

show_status(adc_status(axp209))
adc_enable(axp209, ADC_BATT_C)
adc_disable(axp209, ADC_VBUS_C | ADC_VBUS_V)
show_status(adc_status(axp209))

print("Battery voltage   = %1.4f" % batt_voltage(axp209))
print("Battery gauge     = %d%%"  % batt_gauge(axp209))
print("Battery current   = %1.4f" % batt_current(axp209))

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

