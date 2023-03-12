 ###############################################
#
# Autor: Alex Merz
# Date: 03.03.2023
# Software: Main
# Board: Badger2040 (Pimoroni)
# Compiler: Raspberry Pi Pico from Thonny Tool
# Load Code: Push boot button and change interpretor port (Right lower corner)
#            Sometimes Thonny has to be restarted for that
#
###############################################
############################ Library
import badgeviewer
import imageviewer
import badger2040
import badger_os
import time
from machine import Pin, ADC

############################ Constant
BATTERY_MIN_LEVEL = 3.2 # Range: 2.0V-3.7V

############################ Variable
# Create a new Badger and set it to update FAST
display = badger2040.Badger2040()
display.update_speed(badger2040.UPDATE_FAST)

# Set up the ADCs for measuring battery voltage
vbat_adc = ADC(badger2040.PIN_BATTERY)
vref_adc = ADC(badger2040.PIN_1V2_REF)
vref_en = Pin(badger2040.PIN_VREF_POWER)
vref_en.init(Pin.OUT)
vref_en.value(0)

############################ Function: CheckBatterystatus
def CheckBatteryStatus():
    # Enable the onboard voltage reference
    vref_en.value(1)

    # Calculate the logic supply voltage, as will be lower that the usual 3.3V when running off low batteries
    vdd = 1.24 * (65535 / vref_adc.read_u16())
    vbat = (
        (vbat_adc.read_u16() / 65535) * 3 * vdd
    )  # 3 in this is a gain, not rounding of 3.3V

    # Disable the onboard voltage reference
    vref_en.value(0)

    # Print out the voltage
    print("Battery Voltage = ", vbat, "V", sep="")

    # Open popup if voltage is too low
    if vbat < BATTERY_MIN_LEVEL:
        badger_os.warning(display, "Battery low!!!")
        time.sleep(3)
    
############################ Init
print("Main script init started...")
display.led(255)

badgeviewer.Init()
imageviewer.Init()
CheckBatteryStatus()

print("...Main script init end")

############################ Main
print("Main script in run loop")

while True:
    badgeviewer.Run()
    imageviewer.Run()
    CheckBatteryStatus()