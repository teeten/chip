#!/usr/bin/python

import time, signal, sys
import Adafruit_PureIO.smbus as smbus

###############
## FUNCTIONS ##
###############

AXP209_ADDR = 0x34

# === generic === #

def ison(status,flags):
    return True if status & flags else False

# === power status === #

PWR_HAS_VBUS  = 1 << 5
PWR_HAS_ACIN  = 1 << 7
PWR_HAS_BATT  = 1 << 13
PWR_CHARGING  = 1 << 14

def power_status(pmu):
    return pmu.read_word_data(AXP209_ADDR, 0x00)

# === adc status === #

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

# === adc inputs measurements === #

def acin_voltage(pmu): # 12-bits
    w = pmu.read_word_data(AXP209_ADDR, 0x56)
    return (((w & 0x00ff) << 4) | (w & 0x0f00) >> 8) * 0.0017

def acin_current(pmu): # 12-bits
    w = pmu.read_word_data(AXP209_ADDR, 0x58)
    return (((w & 0x00ff) << 4) | (w & 0x0f00) >> 8) * 0.000625

def vbus_voltage(pmu): # 12-bits
    w = pmu.read_word_data(AXP209_ADDR, 0x5a)
    return (((w & 0x00ff) << 4) | (w & 0x0f00) >> 8) * 0.0017

def vbus_current(pmu): # 12-bits
    w = pmu.read_word_data(AXP209_ADDR, 0x5c)
    return (((w & 0x00ff) << 4) | (w & 0x0f00) >> 8) * 0.000375

# === adc battery measurements === #

def batt_voltage(pmu): # 12-bits
    w = pmu.read_word_data(AXP209_ADDR, 0x78)
    return (((w & 0x00ff) << 4) | (w & 0x0f00) >> 8) * 0.0011

def batt_current(pmu):
    if not ison(power_status(pmu), PWR_CHARGING):
        w = pmu.read_word_data(AXP209_ADDR, 0x7c) # 13-bits
        return (((w & 0x00ff) << 5) | (w & 0x1f00) >> 8) * 0.0005
    else:
        w = pmu.read_word_data(AXP209_ADDR, 0x7a) # 12-bits
        return (((w & 0x00ff) << 4) | (w & 0x0f00) >> 8) * -0.0005

def batt_gauge(pmu):
    return pmu.read_byte_data(AXP209_ADDR, 0xb9)

def internal_temperature(pmu): # 12-bits
    w = pmu.read_word_data(AXP209_ADDR, 0x5e)
    return -144.7 + 0.1 * (((w & 0x00ff) << 4) | (w & 0x0f00) >> 8)

##########
## MAIN ##
##########

axp209 = smbus.SMBus(0, dangerous=True)

adc_enable(axp209, ADC_BATT_V | ADC_BATT_C | ADC_ACIN_V | ADC_ACIN_C | ADC_VBUS_V | ADC_VBUS_C)

adc = adc_status(axp209)

print("ADC status=%s BV=%s BC=%s AV=%s AC=%s VV=%s VC=%s" % (bin(adc),
    ison(adc, ADC_BATT_V),
    ison(adc, ADC_BATT_C),
    ison(adc, ADC_ACIN_V),
    ison(adc, ADC_ACIN_C),
    ison(adc, ADC_VBUS_V),
    ison(adc, ADC_VBUS_C)))

pwr = power_status(axp209)

print("POWER status=%s VBUS=%s ACIN=%s BATT=%s CHARGING=%s\n" % (bin(pwr),
    ison(pwr, PWR_HAS_VBUS),
    ison(pwr, PWR_HAS_ACIN),
    ison(pwr, PWR_HAS_BATT),
    ison(pwr, PWR_CHARGING)))

print("Temperature       = %1.1f" % internal_temperature(axp209))
print("ACIN voltage      = %1.4f" % acin_voltage(axp209))
print("ACIN current      = %1.4f" % acin_current(axp209))
print("VBUS voltage      = %1.4f" % vbus_voltage(axp209))
print("VBUS current      = %1.4f" % vbus_current(axp209))
print("Battery gauge     = %d%%"  % batt_gauge(axp209))
print("Battery voltage   = %1.4f" % batt_voltage(axp209))
print("Battery current   = %1.4f" % batt_current(axp209))

axp209.close()

