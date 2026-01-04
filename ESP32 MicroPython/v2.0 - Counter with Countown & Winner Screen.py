from machine import Pin, SoftI2C
import ssd1306
from time import sleep, ticks_ms, ticks_diff
import urandom

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
# DRAW PLAYERS
# <><><><><><><><><><><>
# Define a function called 'draw_players' where it's inputs are 'score1', 'score2' , and 'countdown'. The 'None' part means that it isn't drawn unless a value is provided.
# 'oled.fill(0)' clears the screen.
def draw_players(score1=None, score2=None, countdown=None):
    oled.fill(0)
    # Draw the following strings centered on the given x-values and at the given y-values.
    draw_centered("Player", 32, 12)
    draw_centered("#1", 32, 22)
    draw_centered("Player", 96, 12)
    draw_centered("#2", 96, 22)

    # If any of the inputs of the above function is defined, draw them using the draw_centered function after the input is converted into a string.
    if countdown is not None:
        draw_centered(str(countdown), 64, 42)
    else:
        if score1 is not None:
            draw_centered(str(score1), 32, 42)
        if score2 is not None:
            draw_centered(str(score2), 96, 42)

# <><><><><><><><><><><>
# DRAW TIMER
# <><><><><><><><><><><>
# Define a function called 'draw_timer' that has the input of 'seconds_left'.
# Convert to string then draw the countdown timer at the center/top of the screen.
def draw_timer(seconds_left):
    draw_centered(str(seconds_left), 64, 0)

# <><><><><><><><><><><>
# START COUNTDOWN FUNCTION
# <><><><><><><><><><><>
# Define a function called 'start_countdown' that has no inputs.
# An iterative function. First go i=3, second go, i=2, third go i=1.
# Use the draw_players function to draw the countdown on the screen.
# Wait 1 second before going to the next iteration of the function for i.
# After countdown is done, print "Start!".
def start_countdown():
    for i in [3, 2, 1]:
        draw_players(countdown=i)
        oled.show()
        sleep(1)
    draw_players(countdown="Start!")
    oled.show()
    sleep(0.5)

# <><><><><><><><><><><>
# MAIN GAME LOOP
# <><><><><><><><><><><>
# Define a function called 'game_loop' with no inputs.
# global turns the classes 'last_btn1' and 'last_btn2' into global variables so they can be used by other functions.
# Set 'score1' and 'score2' to 0.
# Set 'lastbtn1' and 'last_btn2' to be equal to the value of the corresponding button.
# Use the draw_players function to draw the value of 'score1' and 'score2' on the screen.
def game_loop():
    global last_btn1, last_btn2
    score1 = 0
    score2 = 0
    last_btn1 = btn1.value()
    last_btn2 = btn2.value()
    draw_players(score1, score2)
    draw_timer(10)
    oled.show()
    
    both_pressed_time = None
    start_time = ticks_ms()
    duration = 10000
    last_timer = None

    while True:
        current_btn1 = btn1.value()
        current_btn2 = btn2.value()

        # RESET LOGIC
        if current_btn1 == 0 and current_btn2 == 0: # Buttons are 0 when pressed down. If both buttons are pressed...
            if both_pressed_time is None: # and if the 'button_pressed_time' is not currently being counted..
                both_pressed_time = ticks_ms() # Count the time.
            elif ticks_diff(ticks_ms(), both_pressed_time) >= 2000: # If it reaches 2 seconds...
                return # reset the game.
        else:
            both_pressed_time = None # If it didn't reach 2 seconds, nothing happens.

        # SCORING
        if last_btn1 == 0 and current_btn1 == 1:
            score1 += 1
            draw_players(score1, score2)
            draw_timer(last_timer if last_timer is not None else 10)
            oled.show()
        if last_btn2 == 0 and current_btn2 == 1:
            score2 += 1
            draw_players(score1, score2)
            draw_timer(last_timer if last_timer is not None else 10)
            oled.show()

        last_btn1 = current_btn1
        last_btn2 = current_btn2

        # TIMER LOGIC
        elapsed = ticks_diff(ticks_ms(), start_time) # Calculates how much time has passed since the timer started.
        if elapsed >= duration: # Ends the timer if the amount of time passed is greater that the duration that was defined previously. 
            break

        seconds_left = 10 - (elapsed // 1000) # Converts elapsed ms to seconds and subtracts that from 10 to get seconds left.
        if seconds_left != last_timer: # Once the seconds in the countdown changes, redraw everything and set the last_timer to equal the 'seconds_left'.
            draw_players(score1, score2)
            draw_timer(seconds_left)
            oled.show()
            last_timer = seconds_left

        sleep(0.01)

    # WINNER ANIMATION
    winner_animation(score1, score2) # Once kicked out of the game loop, start the winner animation with the inputs of the scores.

# <><><><><><><><><><><>
# WINNER ANIMATION FUNCTION
# <><><><><><><><><><><>
# Define a function called 'winner_animation' that has the inputs of 'score1' and 'score2'.
# Clear the screen.
# If 'score1' is higher than 'score2' the, winner text says Player #1 won and the 'final_score' is defined by 'score1'. The opposite is true for Player #2.
# If there is a Tie, it will display that. Doesn't matter what score we pick to display because they are the same.
def winner_animation(score1, score2):
    oled.fill(0)
    if score1 > score2:
        winner_text = "Player #1 won!"
        final_score = score1
    elif score2 > score1:
        winner_text = "Player #2 won!"
        final_score = score2
    else:
        winner_text = "Tie!"
        final_score = score1

    # SPARKLES
    # 'sparkle_dots' is a list that holds the x-value, y-value, and life left for each sparkle.
    # Defines the 'max_life' to be 10 frames. This will be used later to apply to 'all sparkle_dots'.
    sparkle_dots = [] 
    max_life = 10
    both_pressed_time = None

    while True:
        # Exit condition: both buttons held for 2s
        if btn1.value() == 0 and btn2.value() == 0:
            if both_pressed_time is None:
                both_pressed_time = ticks_ms()
            elif ticks_diff(ticks_ms(), both_pressed_time) >= 2000:
                return
        else:
            both_pressed_time = None

        # ADDING NEW SPARKLES
        for _ in range(2):  # Create a loop that runs twice (2 new dots).
            sparkle_dots.append({ # Add a new item to the sparkle_dots list.
                'x': urandom.getrandbits(7), # The x-value is a number between 0-127 (2^7).
                'y': urandom.getrandbits(6), # The y-value is a number between 0-63 (2^6).
                'life': max_life # 'max_life" was previously defined as 10 frames.
            })

        # DRAW IMPORTANT THINGS ON SCREEN
        oled.fill(0) # Clear screen.
        draw_centered(winner_text, 64, 20) # Draw 'winner_text' 
        draw_centered(f"({final_score} presses)", 64, 35) # f = formatted string literal. Just replaces {final_score} with the 'final_score'.

        # DRAW DOTS & DECREASE LIFE
        for dot in sparkle_dots: # For each listed item in this list...
            oled.pixel(dot['x'], dot['y'], 1) # Draw an 'oled.pixel' for the x and y-values. 1 makes the pixel on.
            dot['life'] -= 1 # The life of the dot is decreased by 1.

        # REMOVE DEAD DOTS
        sparkle_dots = [dot for dot in sparkle_dots if dot['life'] > 0] # Go throught the 'sparkle_dot' list and only keep entries where the life is above 0.

        oled.show()
        sleep(0.05)

# <><><><><><><><><><><>
# PROGRAM LOOP
# <><><><><><><><><><><>
# Start the countdown. After the countdown, start the game.
while True:
    start_countdown()
    game_loop()