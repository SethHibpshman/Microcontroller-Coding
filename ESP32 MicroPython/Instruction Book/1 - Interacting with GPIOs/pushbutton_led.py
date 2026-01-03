from machine import Pin
from time import sleep

# define led class as pin 5 where it is treated as an output.
# define button class as pin 4 where it is treated as an input.
led = Pin(5, Pin.OUT)
button = Pin(4, Pin.IN)

# while True creates loop.
# set the value of the led class to the value of the button class.
# why sleep? maybe to slow down the code?
while True:
  led.value(button.value())
  sleep(0.1)