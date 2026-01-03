from machine import Pin, PWM
from time import sleep

frequency = 5000 # Can be from 0 to 78125Hz, 5000Hz is used to control LED brightness?
led = PWM(Pin(5), frequency) # Define 'led' as pin 5 with the frequency object.

# Duty cycle can be from 0 to 1024. 0 is 0% brightness and 1024 is 100% brightness.
while True:
  for duty_cycle in range(0, 1024):
    led.duty(duty_cycle) # define the duty cycle of the led class
    sleep(0.005)