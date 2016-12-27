import Adafruit_PureIO.smbus as smbus

###############
## FUNCTIONS ##
###############

AXP209_ADDR = 0x34

# === generic === #

def ison(status,flags):
    return True if status & flags else False

# === power status === #

HAS_VBUS  = 1 << 5
HAS_ACIN  = 1 << 7
HAS_BATT  = 1 << 13
CHARGING  = 1 << 14

def power_status(pmu):
    return pmu.read_word_data(AXP209_ADDR, 0x00)

# === adc status === #

BATT_V = 1 << 7
BATT_C = 1 << 6
ACIN_V = 1 << 5
ACIN_C = 1 << 4
VBUS_V = 1 << 3
VBUS_C = 1 << 2
TEMP   = 1 << 15

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
    if not ison(power_status(pmu), CHARGING):
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

