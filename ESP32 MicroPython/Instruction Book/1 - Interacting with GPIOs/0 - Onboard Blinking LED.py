import machine
import neopixel
import time

# Configuration for onboard RGB LED
PIN = 48         # GPIO driving the NeoPixel
NUM_PIXELS = 1   # Only 1 LED

# Initialize NeoPixel
LED = neopixel.NeoPixel(machine.Pin(PIN), NUM_PIXELS)

while True:
    # Turn LED ON
    LED[0] = (0, 0, 0)  # Define color with LED[0] = (#, #, #)
    LED.write()
    time.sleep(1)
    # Turn LED ON
    LED[0] = (10, 0, 0)  # Define color with LED[0] = (#, #, #)
    LED.write()
    time.sleep(1)
        # Turn LED ON
    LED[0] = (0, 10, 0)  # Define color with LED[0] = (#, #, #)
    LED.write()
    time.sleep(1)
        # Turn LED ON
    LED[0] = (0, 0, 10)  # Define color with LED[0] = (#, #, #)
    LED.write()
    time.sleep(1)
        # Turn LED ON
    LED[0] = (10, 10, 10)  # Define color with LED[0] = (#, #, #)
    LED.write()
    time.sleep(1)
