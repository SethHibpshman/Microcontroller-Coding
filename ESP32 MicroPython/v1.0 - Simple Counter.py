from machine import Pin, SoftI2C
import ssd1306
from time import sleep, ticks_ms, ticks_diff

# <><><><><><><><><><><>
# OLED SETUP
# <><><><><><><><><><><>
# Defining which pins to use for i2c.
# Defining what our oled is, it's resolution, and communication protocal.
i2c = SoftI2C(scl=Pin(46), sda=Pin(21))
oled = ssd1306.SSD1306_I2C(128, 64, i2c)

# <><><><><><><><><><><>
# BUTTON SETUP
# <><><><><><><><><><><>
# GPIO 7 & 16 are wired to a button input and the button output goes to ground.
btn1 = Pin(7, Pin.IN, Pin.PULL_UP)
btn2 = Pin(16, Pin.IN, Pin.PULL_UP)

# <><><><><><><><><><><>
# CENTERED TEXT HELPER
# <><><><><><><><><><><>
# Create a function called 'draw_centered' where the inputs are a string ('text'), what x value to center it on, and the y value to place it.
# Calculate the pixel width of the text by counting the characters with 'len(text)' and multiply by 8 (pixels per character) to get the real pixel width.
# To find the x value of where to write the text, find the center of where you want to write it ('center_x') and subtract half the width of the text (so it is centered).
# 'oled.text(text, x, y)' Code to finally draw the text.
def draw_centered(text, center_x, y):
    width = len(text) * 8
    x = center_x - (width // 2)
    oled.text(text, x, y)

# <><><><><><><><><><><>
# DRAW PLAYERS (WITH optional COUNTERS)
# <><><><><><><><><><><>
# Define a function called 'draw_players' where it's inputs are 'score1', 'score2' , and 'countdown'. The 'None' part means that it isn't drawn unless a value is provided.
# 'oled.fill(0)' clears the screen.
def draw_players(score1=None, score2=None, countdown=None):
    oled.fill(0)
    # Draw the following strings centered on the given x-values and at the given y-values.
    draw_centered("Player", 32, 0)
    draw_centered("#1", 32, 10)
    draw_centered("Player", 96, 0)
    draw_centered("#2", 96, 10)

    # If any of the inputs of the above function is defined, draw them using the draw_centered function after the input is converted into a string.
    if countdown is not None:
        draw_centered(str(countdown), 64, 30)
    else:
        if score1 is not None:
            draw_centered(str(score1), 32, 30)
        if score2 is not None:
            draw_centered(str(score2), 96, 30)

    oled.show()

# <><><><><><><><><><><>
# START COUNTDOWN FUNCTION
# <><><><><><><><><><><>
# Define a function called 'start_countdown' that has no inputs.
# An interative function. First go i=3, second go, i=2, third go i=1.
# Use the draw_players function to draw the countdown on the screen.
# Wait 1 second before going to the next iteration of the function for i.
# After countdown is done, print "Start!".
def start_countdown():
    for i in [3, 2, 1]:
        draw_players(countdown=i)
        sleep(1)
    draw_players(countdown="Start!")
    sleep(0.5)

# <><><><><><><><><><><>
# MAIN GAME LOOP
# <><><><><><><><><><><>
# Define a function called 'game_loop' with no inputs.
# global turns the classes 'last_btn1' and 'last_btn2' into global variables so they can be used by other functions.
# Set 'score1' and 'score2' to 0.
# Set 'lastbtn1' and 'last_btn2' to be equal to the value of the corresponding button.
# Use the draw_players function to draw the value of 'score1' and 'score2' on the screen.

# 'both_pressed_time' used to track how long both buttons are pressed at the same time.

# The while True creates a loop to where the game continues until intervention.
def game_loop():
    global last_btn1, last_btn2
    score1 = 0
    score2 = 0
    last_btn1 = btn1.value()
    last_btn2 = btn2.value()
    draw_players(score1, score2)
    
    both_pressed_time = None

    while True:
        current_btn1 = btn1.value()
        current_btn2 = btn2.value()

        # <><><><><><><><><><><>
        # RESET LOGIC (both buttons held 2s)
        # <><><><><><><><><><><>
        #  The buttons equal 0 when held because of the 'Pin.PULL_UP'.
        # If the 'both_pressed_time' was previously None when both are being pressed at the same time, record how long they are being pressed.
        # If the buttons have been held for 2 seconds, return (or restart the game).
        # If it does not reach 2 seconds, the state of both_pressed_time will still equal None and not change.
        if current_btn1 == 0 and current_btn2 == 0:
            if both_pressed_time is None:
                both_pressed_time = ticks_ms()
            elif ticks_diff(ticks_ms(), both_pressed_time) >= 2000:
                # Restart the game
                return
        else:
            both_pressed_time = None

        # <><><><><><><><><><><>
        # SCORE INCREMENT (on release)
        # <><><><><><><><><><><>
        #  If the button is released, increase the score by 1.
        #  Draw the score increase.
        if last_btn1 == 0 and current_btn1 == 1:
            score1 += 1
            draw_players(score1, score2)
        if last_btn2 == 0 and current_btn2 == 1:
            score2 += 1
            draw_players(score1, score2)
        
        # Define the last button press as the one that was just pressed.
        last_btn1 = current_btn1
        last_btn2 = current_btn2
        sleep(0.05)

# <><><><><><><><><><><>
# PROGRAM LOOP
# <><><><><><><><><><><>
# Start the countdown. After the countdown, start the game.
while True:
    start_countdown()
    game_loop()
