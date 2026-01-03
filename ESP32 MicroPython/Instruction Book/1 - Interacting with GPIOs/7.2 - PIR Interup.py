from machine import Pin
from time import sleep

motion = False

def handle_interrupt(pin):
    global motion
    motion = True   # only set a flag

led = Pin(12, Pin.OUT)
pir = Pin(14, Pin.IN, Pin.PULL_DOWN)

pir.irq(trigger=Pin.IRQ_RISING, handler=handle_interrupt)

while True:
    if motion:
        motion = False      # reset immediately
        print("Motion detected!")
        led.value(1)
        sleep(5)            # shorter delay
        led.value(0)
        print('Motion stopped!')
    sleep(0.1)              # small idle delay
