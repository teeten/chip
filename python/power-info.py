#!/usr/bin/python

import Adafruit_PureIO.smbus as smbus
import t10_axp209 as pmu

##########
## MAIN ##
##########

axp209 = smbus.SMBus(0, dangerous=True)

pmu.adc_enable(axp209, pmu.BATT_V | pmu.BATT_C | pmu.ACIN_V | pmu.ACIN_C | pmu.VBUS_V | pmu.VBUS_C)

adc = pmu.adc_status(axp209)

print("ADC status=%s BV=%s BC=%s AV=%s AC=%s VV=%s VC=%s" % (bin(adc),
    pmu.ison(adc, pmu.BATT_V),
    pmu.ison(adc, pmu.BATT_C),
    pmu.ison(adc, pmu.ACIN_V),
    pmu.ison(adc, pmu.ACIN_C),
    pmu.ison(adc, pmu.VBUS_V),
    pmu.ison(adc, pmu.VBUS_C)))

pwr = pmu.power_status(axp209)

print("POWER status=%s VBUS=%s ACIN=%s BATT=%s CHARGING=%s\n" % (bin(pwr),
    pmu.ison(pwr, pmu.HAS_VBUS),
    pmu.ison(pwr, pmu.HAS_ACIN),
    pmu.ison(pwr, pmu.HAS_BATT),
    pmu.ison(pwr, pmu.CHARGING)))

print("Temperature       = %1.1f" % pmu.internal_temperature(axp209))
print("ACIN voltage      = %1.4f" % pmu.acin_voltage(axp209))
print("ACIN current      = %1.4f" % pmu.acin_current(axp209))
print("VBUS voltage      = %1.4f" % pmu.vbus_voltage(axp209))
print("VBUS current      = %1.4f" % pmu.vbus_current(axp209))
print("Battery gauge     = %d%%"  % pmu.batt_gauge(axp209))
print("Battery voltage   = %1.4f" % pmu.batt_voltage(axp209))
print("Battery current   = %1.4f" % pmu.batt_current(axp209))

axp209.close()

