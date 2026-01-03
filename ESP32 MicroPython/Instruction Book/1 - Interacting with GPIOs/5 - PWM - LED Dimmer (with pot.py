# Import Pin (for GPIO), PWM (for brightness control), and ADC (for analog reading)
from machine import Pin, PWM, ADC

# Import sleep to pause the program
from time import sleep


# Create a PWM object on pin 5 (this pin drives the LED)
# freq=5000 sets the PWM frequency to 5000 Hz
led = PWM(Pin(5), freq=5000)


# Create an ADC object on pin 4 (this pin reads the potentiometer)
pot = ADC(Pin(4))

# Set ADC attenuation so it can read voltages up to ~3.3V
pot.atten(ADC.ATTN_11DB)


# This loop runs forever
while True:

    # Read the potentiometer value
    # On ESP32 this gives a number from 0 to 4095
    pot_value = pot.read()

    # Convert the ADC range (0–4095) to PWM range (0–1023)
    # >> 2 means "divide by 4"
    duty = pot_value >> 2


    # Safety check: make sure duty is not below 0
    if duty < 0:
        duty = 0

    # Safety check: make sure duty is not above 1023
    elif duty > 1023:
        duty = 1023


    # Set the LED brightness using the PWM duty cycle
    led.duty(duty)

    # Print the raw ADC value and the PWM duty value
    print(pot_value, duty)

    # Wait 0.1 seconds before running the loop again
    sleep(0.1)
