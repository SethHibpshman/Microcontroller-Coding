# Importing the Pin class from the machine module.
# Importing the sleep class from the time module.
from machine import Pin
from time import sleep

# Defining 'led' with the following attributes (Pin number, pin mode, pull, value).
# Pin number = the GPIO number on the board that we are interacting with.
# Pin mode = the mode we set this pin to be (can be input, output, or open-drain).
  # Pin.IN = treated as input
  # Pin.OUT = treated as output
  # Pin.OPEN_DRAIN = idk
# Pull = idk
# Value = can be '1', '0', 'True', or 'False'. '0' means off, '1' means on.
# Statement = 'led' is pin 2 on the board and it is an output pin.
led = Pin(2, Pin.OUT)

# while something is always true is an easy way to make a loop.
  # now taking the value from the led object we defined earlier, we can change it with 'led.value(state)'.
    # led.value(state) = state can be the goal state or logical operators like 'not'.
  # sleep(<# in seconds>) is just a wait, halt, or delay function.
while True:
  led.value(not led.value())
  sleep(1)
