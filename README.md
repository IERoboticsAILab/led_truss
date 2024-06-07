# Project
This is a research project for the IE Robotics Lab exploring accessible, non-invasive solutions to telepresence. Multiple LED strips will be installed on the OptiTrack truss with a programmable interface for interactive displays. Moreover, the intent is to connect the LEDs to basic human monitoring, such as a Fitbit, to interact with real-time biological data such as heart rate, blood pressure, etc, to act as a representation of mood and emotion.

# Hardware setup
This project uses WS2813 fully addressable LED strips. You will need a Raspberry Pi, the LEDs, some jumper wires, and a breadboard is recommended for ease of use.

1. Connect the GROUND pin on the LEDs to the GROUND pin on the Raspberry Pi.
2. Connect **both** data pins, D0 and D1, on the LEDs to a data pin on the raspberyy pi (recommended GPIO18).
3. Connect the VOLTAGE pin on the LEDs to the 5V pin on the Raspberry Pi.
4. pip install the `rpi_ws281x` library onto the Raspberry Pi.
5. Run python code on the Raspberry Pi to control the LEDs as outline in the [provided helper library](main.py) and the section below.

## Connecting strips together
Only the first LED strip needs to be connected to the Rasperry Pi, subsequent ones can be connected to each other. To attach a new LED strip to the sequence:
1. Remove plastic coating at end of strip and clear space around pins.
2. Connect strip to Raspberry Pi as shown above.
3. Solder, tape, or wire the pins from the cleared end of that strip to the normal connection end of a new LED strip.
4. Increase the `LED_COUNT` variable in the setup below the total number of combined LEDs on both strips.
5. Use as normal.

# Software setup
The WS2813 LEDs are very easy to use.
First, you need to run through some basic setup:

```
from rpi_ws281x import *

LED_COUNT      = 30         # Number of LED pixels.
LED_PIN        = 18         # GPIO pin connected to the pixels (18 uses PWM).
LED_FREQ_HZ    = 800000     # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10         # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 65         # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False      # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0          # set to '1' for GPIOs 13, 19, 41, 45 or 53

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()
```

<br>

Next, use the library's `setPixelColor(index, color)` and `show()` functions to control the LED strip. For example:
```
strip.setPixelColor(15, Color(0,0,255))
strip.show()
```
This code snippet will set the 16th (it's 0-indexed) LED light in the strip to fully blue.

<br>

This can be easily combined with loops to effect multiple LEDs at the same time:
```
for i in range(LED_COUNT):
  strip.setPixelColor(i, Color(255,255,255))
strip.show()
```
This snippet makes every LED on the strip completely white.

<br>

To turn an LED off, set the color to black:
```
strip.setPixelColor(15, Color(0,0,0))
strip.show()
```
