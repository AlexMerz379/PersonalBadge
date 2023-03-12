###############################################
#
# Autor: Alex Merz
# Date: 03.03.2023
# Software: Image viewer
# Board: Badger2040 (Pimoroni)
# Compiler: Raspberry Pi Pico from Thonny Tool
# Load Code: Push boot button and change interpretor port (Right lower corner)
#            Sometimes Thonny has to be restarted for that.
#			 Images must be 296x128 pixel with 1bit colour depth
#
###############################################
############################ Library
import os
import sys
import time
import badger2040
from badger2040 import HEIGHT
import badger_os

############################ Constants
OVERLAY_BORDER = 40
OVERLAY_SPACING = 20
OVERLAY_TEXT_SIZE = 0.5

TOTAL_IMAGES = 0

############################ Variable
display = 0
image = 0
state = 0
changed = 0
IMAGES = 0

############################ Function: ShowImage
def ShowImage(n):
    file = IMAGES[n]
    name = file.split(".")[0]
    open("images/{}".format(file), "r").readinto(image)
    display.image(image)

    if state["show_info"]:
        for i in range(TOTAL_IMAGES):
            x = 286
            y = int((128 / 2) - (TOTAL_IMAGES * 10 / 2) + (i * 10))
            display.pen(0)
            display.rectangle(x, y, 8, 8)
            if state["current_image"] != i:
                display.pen(15)
                display.rectangle(x + 1, y + 1, 6, 6)

    display.update()

############################ Init
def Init():
    print("Imageviewer script init started...")     
        
    ############
    # Initialize display
    ############
    global display
    # Turn the act LED on as soon as possible
    display = badger2040.Badger2040()
    display.led(255)

    ############
    # Load all images
    ############
    global image
    global state
    global IMAGES
    global TOTAL_IMAGES
    try:
        IMAGES = [f for f in os.listdir("/images") if f.endswith(".bin")]
        TOTAL_IMAGES = len(IMAGES)
    except OSError:
        pass

    image = bytearray(int(296 * 128 / 8))

    state = {
        "current_image": 0,
        "show_info": False
    }

    ############
    # Check if there is one image loaded
    ############
    global changed
    
    if TOTAL_IMAGES == 0:
        display.pen(15)
        display.clear()
        badger_os.warning(display, "To run this demo, create an /images directory on your device and upload some 1bit 296x128 pixel images.")
        time.sleep(4.0)
        sys.exit()

    badger_os.state_load("image", state)

    changed = not badger2040.woken_by_button()
    
    print("...Imageviewer script init end") 

############################ Main
def Run():
    print("Imageviewer script run started...")
    global display
    global changed
    global state
    global TOTAL_IMAGES
    
    runInLoop = True
    actualTimeStamp = time.time()
    state["current_image"] = 0
    state["show_info"] = False

    while runInLoop:
        ############
        # Show info bar on the right side
        ############
        if display.pressed(badger2040.BUTTON_A) and display.pressed(badger2040.BUTTON_C):
            print("Enable/Disable info bar")
            state["show_info"] = not state["show_info"]
            changed = True
        
        ############
        # Next image
        ############
        if display.pressed(badger2040.BUTTON_C) or display.pressed(badger2040.BUTTON_UP):
            print("Next project")
            changed = True
            if state["current_image"] > 0:
                state["current_image"] -= 1
            else:
                state["current_image"] = TOTAL_IMAGES - 1
                
        ############
        # Previous image
        ############
        if display.pressed(badger2040.BUTTON_A) or display.pressed(badger2040.BUTTON_DOWN):
            print("Previous project")
            changed = True
            if state["current_image"] < TOTAL_IMAGES - 1:
                state["current_image"] += 1
            else:
                state["current_image"] = 0
                
        ############
        # Cancel show of project and go back to main script
        ############
        if display.pressed(badger2040.BUTTON_B):
            print("Cancel project view and run main script")
            runInLoop = False

        ############
        # Autoscroll
        ############
        # Someone pushed a button give a delay before starting the autoscrolling again
        if changed:
            actualTimeStamp = time.time() + 20
            
        # Check if next autoscroll should be started
        if (time.time() - actualTimeStamp) > 8:
            print("Autoscroll")
            actualTimeStamp = time.time()
            changed = True
            if state["current_image"] > 0:
                state["current_image"] -= 1
            else:
                state["current_image"] = TOTAL_IMAGES - 1

        ############
        # Update display
        ############
        if changed:
            badger_os.state_save("image", state)
            ShowImage(state["current_image"])
            changed = False

        ############
        # Sleep Mode
        #
        # Halt the Badger to save power, it will wake up if any of the front buttons are pressed
        # Do not use it if autoscrolling should be possible
        ############
        #display.halt()
        
    print("...Imageviewer script run end")