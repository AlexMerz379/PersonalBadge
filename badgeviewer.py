###############################################
#
# Autor: Alex Merz
# Date: 03.03.2023
# Software: BadgeViewer
# Board: Badger2040 (Pimoroni)
# Compiler: Raspberry Pi Pico from Thonny Tool
# Load Code: Push boot button and change interpretor port (Right lower corner)
#            Sometimes Thonny has to be restarted for that
#
###############################################
############################ Library
import time
import badger2040
import badger_os

############################ Constants
############
# External files
############
USER_TXT_FILE = "badge/badge.txt"
USER_IMAGE_FILE = "badge/badge.bin"

############
# System limit
############
WIDTH = badger2040.WIDTH
HEIGHT = badger2040.HEIGHT

############
# Image Box (Right)
############
IMAGE_WIDTH = 104
BADGE_IMAGE = bytearray(int(IMAGE_WIDTH * HEIGHT / 8))

############
# Detail Box (Left down)
############
DETAILS_HEIGHT = 60
DETAILS_TEXT_SIZE = 0.5
DETAILS_TEXT_POS_OFFSET = 8 # Dependent on DETAILS_TEXT_SIZE
DETAIL_NBR_LINES = 4
DETAIL_TITEL = 'Specialist for'
DETAIL_SPACING = 10

############
# Company Box (Left up)
############
COMPANY_HEIGHT = 30
COMPANY_TEXT_SIZE = 0.6

############
# Name Box (Left middle)
############
NAME_HEIGHT = HEIGHT - COMPANY_HEIGHT - DETAILS_HEIGHT - 2
NAME_PADDING = 20

############
# General data
############
TEXT_WIDTH = WIDTH - IMAGE_WIDTH - 1
LEFT_PADDING = 5

DEFAULT_TEXT = """My Company
H. Muster
-Watching bird
-Sleeping
-Eating"""

############################ Variable
company = "Test"
name = "Test"
detail1 = "Test"
detail2 = "Test"
detail3 = "Test"

############################ Function: TrunCateString
# Reduce the size of a string until it fits within a given width
def TrunCateString(text, text_size, width):
    while True:
        length = display.measure_text(text, text_size)
        if length > 0 and length > width:
            text = text[:-1]
        else:
            text += ""
            return text

############################ Function: ImageBox
def ImageBox():
    ############
    # Draw image
    ############
    display.image(BADGE_IMAGE, IMAGE_WIDTH, HEIGHT, WIDTH - IMAGE_WIDTH, 0)
    
    ############
    # Draw border
    ############
    display.pen(0)
    display.thickness(1)
    display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - 1, 0)
    display.line(WIDTH - IMAGE_WIDTH, 0, WIDTH - IMAGE_WIDTH, HEIGHT - 1)
    display.line(WIDTH - IMAGE_WIDTH, HEIGHT - 1, WIDTH - 1, HEIGHT - 1)
    display.line(WIDTH - 1, 0, WIDTH - 1, HEIGHT - 1)

############################ Function: CompanyBox
def CompanyBox():
    ############
    # Draw Box
    ############
    # Uncomment this if a white background is wanted behind the company
    # display.pen(15)
    # display.rectangle(1, 1, TEXT_WIDTH, COMPANY_HEIGHT - 1)
    
    ############
    # Draw Text
    ############
    display.pen(15)  # Change this to 0 if a white background is used
    display.font("sans")
    display.thickness(2)
    display.text(company, LEFT_PADDING, (COMPANY_HEIGHT // 2) + 1, COMPANY_TEXT_SIZE)
    
############################ Function: NameBox
def NameBox():
    ############
    # Draw Box
    ############
    display.pen(15)
    display.thickness(1)
    display.rectangle(1, COMPANY_HEIGHT + 1, TEXT_WIDTH, NAME_HEIGHT)
    
    ############
    # Draw Box
    ############
    display.pen(0)
    display.font("sans")
    display.thickness(4)
    name_size = 2.0  # A sensible starting scale
    while True:
        name_length = display.measure_text(name, name_size)
        if name_length >= (TEXT_WIDTH - NAME_PADDING) and name_size >= 0.1:
            name_size -= 0.01
        else:
            display.text(name, (TEXT_WIDTH - name_length) // 2, (NAME_HEIGHT // 2) + COMPANY_HEIGHT + 3, name_size)
            break

############################ Function: DetailBox
def DetailBox():
    ############
    # Draw Box
    ############
    display.pen(15) # Color
    display.thickness(1)
    hight_zero_origin = HEIGHT - DETAILS_HEIGHT
    display.rectangle(1, hight_zero_origin, TEXT_WIDTH, DETAILS_HEIGHT - 1)
    
    ############
    # Titel (First line)
    ############
    display.pen(0) # Color
    display.font("sans")
    display.thickness(2)
    
    hight_zero_origin = hight_zero_origin + DETAILS_TEXT_POS_OFFSET
    display.text(DETAIL_TITEL, LEFT_PADDING, hight_zero_origin, DETAILS_TEXT_SIZE)
    
    ############
    # Detail 1 (Second line)
    ############
    display.thickness(1)
    
    hight_pos = hight_zero_origin + (DETAILS_HEIGHT // DETAIL_NBR_LINES)
    display.text(detail1, LEFT_PADDING, hight_pos, DETAILS_TEXT_SIZE)
    
    ############
    # Detail 2 (Third line)
    ############
    hight_pos = hight_zero_origin + (DETAILS_HEIGHT // DETAIL_NBR_LINES) * 2
    display.text(detail2, LEFT_PADDING, hight_pos, DETAILS_TEXT_SIZE)
    
    ############
    # Detail 3 (Fourth line)
    ############
    hight_pos = hight_zero_origin + (DETAILS_HEIGHT // DETAIL_NBR_LINES) * 3
    display.text(detail3, LEFT_PADDING, hight_pos, DETAILS_TEXT_SIZE)
    
############################ Function: GenerateBadge
def GenerateBadge():
    ############
    # Clear previous data
    ############
    display.pen(0)
    display.clear()
    
    ############
    # Load all boxes
    ############
    ImageBox()
    CompanyBox()
    NameBox()
    DetailBox()
    
    ############
    # Update display and stop refresh
    # Do not us this or it will shut down everything and will start all over after a button push
    ############
    display.update()
    #display.halt() # Save power

############################ Init
def Init():
    print("Badge script init startet...")
        
    ############
    # Import user text file
    ############
    try:
        badge = open(USER_TXT_FILE, "r")
    except OSError:
        with open(USER_TXT_FILE, "w") as f:
            f.write(DEFAULT_TEXT)
            f.flush()
        badge = open(USER_TXT_FILE, "r")

    ############
    # Import user image
    ############
    global BADGE_IMAGE
    global USER_IMAGE_FILE
    
    try:
        open(USER_IMAGE_FILE, "rb").readinto(BADGE_IMAGE)
    except OSError:
        try:
            import badge_image
            BADGE_IMAGE = bytearray(badge_image.data())
            del badge_image
        except ImportError:
            pass

    ############
    # Initialize display
    ############
    global display
    display = badger2040.Badger2040()
    display.update_speed(badger2040.UPDATE_NORMAL)
    display.led(255)

    ############
    # Read the file
    ############
    global company
    global name
    global detail1
    global detail2
    global detail3
    
    company = badge.readline()
    name = badge.readline()
    detail1 = badge.readline()
    detail2 = badge.readline()
    detail3 = badge.readline()

    ############
    # Check if given text is short enough
    ############
    company = TrunCateString(company, COMPANY_TEXT_SIZE, TEXT_WIDTH)
    detail1 = TrunCateString(detail1, DETAILS_TEXT_SIZE, TEXT_WIDTH)
    detail2 = TrunCateString(detail2, DETAILS_TEXT_SIZE, TEXT_WIDTH)
    detail3 = TrunCateString(detail3, DETAILS_TEXT_SIZE, TEXT_WIDTH)
    
    print("...Badge script init end") 

############################ Main
def Run():
    print("Badge script run started...")
    GenerateBadge()

    runInLoop = True

    while runInLoop:
        ############
        # Check if a button was pushed
        ############
        if display.pressed(badger2040.BUTTON_A) or display.pressed(badger2040.BUTTON_C) or display.pressed(badger2040.BUTTON_UP) or display.pressed(badger2040.BUTTON_DOWN):
            print("Exit badge script and run imageviewer")
            runInLoop = False

        ############
        # Sleep Mode
        #
        # Halt the Badger to save power, it will wake up if any of the front buttons are pressed
        # Do not us this or it will shut down everything and will start all over after a button push
        ############
        #display.halt()

    print("...Badge script run end")