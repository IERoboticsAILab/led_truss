import time
import math
from rpi_ws281x import *

LED_COUNT      = 60         # Number of LED pixels.
LED_PIN        = 18         # GPIO pin connected to the pixels (18 uses PWM!).
LED_FREQ_HZ    = 800000     # LED signal frequency in hertz (usually 800khz)
LED_DMA        = 10         # DMA channel to use for generating a signal (try 10)
LED_BRIGHTNESS = 65         # Set to 0 for darkest and 255 for brightest
LED_INVERT     = False      # True to invert the signal (when using NPN transistor level shift)
LED_CHANNEL    = 0          # set to '1' for GPIOs 13, 19, 41, 45 or 53

strip = Adafruit_NeoPixel(LED_COUNT, LED_PIN, LED_FREQ_HZ, LED_DMA, LED_INVERT, LED_BRIGHTNESS, LED_CHANNEL)
strip.begin()

def activate_all():
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(255,255,255))
    strip.show()


def set_colour_all(colour):
    for i in range(LED_COUNT):
        strip.setPixelColor(i, colour)
    strip.show()


def clear_all():
    for i in range(LED_COUNT):
        strip.setPixelColor(i, Color(0,0,0))
    strip.show()

def glow(color, delay=0.05):
    #Fade In.
    for i in range (0, 256):
        r = int(math.floor((i / 256.0) * color.r))
        g = int(math.floor((i / 256.0) * color.g))
        b = int(math.floor((i / 256.0) * color.b))
        set_colour_all(Color(r, g, b))
        strip.show()
        time.sleep(delay)
    #Fade Out.
    for i in range (256, 0, -1):
        r = int(math.floor((i / 256.0) * color.r))
        g = int(math.floor((i / 256.0) * color.g))
        b = int(math.floor((i / 256.0) * color.b))
        set_colour_all(Color(r, g, b))
        strip.show()
        time.sleep(delay)

# Define functions which animate LEDs in various ways.
def colorWipe(color, wait_ms=50):
    """Wipe color across display a pixel at a time."""
    for i in range(strip.numPixels()):
        strip.setPixelColor(i, color)
        strip.show()
        time.sleep(wait_ms / 1000.0)

def theaterChase(color, wait_ms=50, iterations=10):
    """Movie theater light style chaser animation."""
    for j in range(iterations):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, color)
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)

def wheel(pos):
    """Generate rainbow colors across 0-255 positions."""
    if pos < 85:
        return Color(pos * 3, 255 - pos * 3, 0)
    elif pos < 170:
        pos -= 85
        return Color(255 - pos * 3, 0, pos * 3)
    else:
        pos -= 170
        return Color(0, pos * 3, 255 - pos * 3)


def rainbow(wait_ms=20, iterations=1):
    """Draw rainbow that fades across all pixels at once."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel((i + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def rainbowCycle(wait_ms=20, iterations=5):
    """Draw rainbow that uniformly distributes itself across all pixels."""
    for j in range(256 * iterations):
        for i in range(strip.numPixels()):
            strip.setPixelColor(i, wheel(
                (int(i * 256 / strip.numPixels()) + j) & 255))
        strip.show()
        time.sleep(wait_ms / 1000.0)


def theaterChaseRainbow(wait_ms=50):
    """Rainbow movie theater light style chaser animation."""
    for j in range(256):
        for q in range(3):
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, wheel((i + j) % 255))
            strip.show()
            time.sleep(wait_ms / 1000.0)
            for i in range(0, strip.numPixels(), 3):
                strip.setPixelColor(i + q, 0)

# pass in values from 0-1. overflows correctly (eg can go from .8->.2 across the edge)
def set_colour_range_percent(colour, start_percent, end_percent):
    start_index = int(LED_COUNT * start_percent)
    end_index = int(LED_COUNT * end_percent)

    index_range = end_index - start_index

    if end_index < start_index:
        index_range = LED_COUNT - end_index + start_index

    for i in range(index_range):
        strip.setPixelColor((start_index + i)%LED_COUNT, colour)

    strip.show()


def set_colour_range_exact(colour, start_index, end_index):
    index_range = end_index - start_index

    if end_index < start_index:
        index_range = LED_COUNT - end_index + start_index

    for i in range(index_range):
        strip.setPixelColor((start_index + i)%LED_COUNT, colour)

    strip.show()


#args in seconds
def angry_mode(delay = 0.05, duration = 30, width = 1):
    clear_all()

    index = 0
    
    while duration > 0:
        strip.setPixelColor((index - width) % LED_COUNT, Color(0,0,0))
        strip.setPixelColor(index, Color(255,0,0))
        strip.show()
        index = (index + 1) % LED_COUNT
        duration -= delay
        time.sleep(delay)

