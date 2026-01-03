from machine import TouchPad, Pin
from time import sleep

touch_pin = TouchPad(Pin(1)) # Pin 1 on my board.

while True:
  touch_value = touch_pin.read()
  print(touch_value)
  sleep(0.5)
