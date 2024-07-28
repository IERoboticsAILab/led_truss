import time
import math
import random
from rpi_ws281x import *

class truss:
    def __init__(self, count=1800, freq=800000, dma=10, brightness=65):
        self.LED_COUNT      = count      # Number of LED pixels.
        self.LED_PIN        = None       # GPIO pin connected to the pixels (18 uses PWM!).
        self.LED_FREQ_HZ    = freq       # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA        = dma        # DMA channel to use for generating a signal (try 10)
        self.LED_BRIGHTNESS = brightness # Set to 0 for darkest and 255 for brightest
        self.LED_INVERT     = False      # True to invert the signal (when using NPN transistor level shift)
        self.LED_CHANNEL    = None       # set to '1' for GPIOs 13, 19, 41, 45 or 53

        self.strip1 = Adafruit_NeoPixel(int(self.LED_COUNT/2), 
                                  18, 
                                  self.LED_FREQ_HZ, 
                                  self.LED_DMA, 
                                  self.LED_INVERT, 
                                  self.LED_BRIGHTNESS, 
                                  0)

        self.strip2 = Adafruit_NeoPixel(int(self.LED_COUNT/2), 
                                  13, 
                                  self.LED_FREQ_HZ, 
                                  self.LED_DMA, 
                                  self.LED_INVERT, 
                                  self.LED_BRIGHTNESS, 
                                  1)


        self.strip1.begin()
        self.strip2.begin()

    # Auxiliary Functions
    def set_pixel_color(self, pixel_index, color):
        if pixel_index < (self.LED_COUNT/2):
            pixel_index_new = int(((self.LED_COUNT/2) - 1) - pixel_index)
            self.strip1.setPixelColor(pixel_index_new, color)
        else: 
            pixel_index_new = int(pixel_index - (self.LED_COUNT/2))
            self.strip2.setPixelColor(pixel_index_new, color)
                
    def show(self):
        self.strip1.show()
        self.strip2.show()

    def set_white_all(self):
        for i in range(self.LED_COUNT):
            self.set_pixel_color(i, Color(255,255,255))
        self.show()

    def set_color_all(self, color):
        for i in range(self.LED_COUNT):
            self.set_pixel_color(i, color)
        self.show()

    def clear_all(self):
        for i in range(self.LED_COUNT):
            self.set_pixel_color(i, Color(0,0,0))
        self.show()
        
    ## Generate rainbow colors across 0-255 positions 
    def wheel(self, pos):
        if pos < 85:
            return Color(pos * 3, 255 - pos * 3, 0)
        elif pos < 170:
            pos -= 85
            return Color(255 - pos * 3, 0, pos * 3)
        else:
            pos -= 170
            return Color(0, pos * 3, 255 - pos * 3)
        
    ## Sets colors based on starting and end percentages of the strip (from 0 to 1)
    def set_color_range_percent(self, color, start_percent, end_percent):
        start_index = int(self.LED_COUNT * start_percent)
        end_index = int(self.LED_COUNT * end_percent)
        index_range = end_index - start_index

        if end_index < start_index:
            index_range = self.LED_COUNT - end_index + start_index

        for i in range(index_range):
            self.set_pixel_color((start_index + i)%self.LED_COUNT, color)

        self.show()

    ## Sets colors based on star and end index of the strip
    def set_color_range_exact(self, color, start_index, end_index):
        index_range = end_index - start_index
        
        if end_index < start_index:
            index_range = self.LED_COUNT - end_index + start_index

        for i in range(index_range):
             self.set_pixel_color((start_index + i)%self.LED_COUNT, color)

        self.show()

    # Vizualtion effects
    ## Glowing effect
    def glow(self, color, wait_ms=10):
        #Fade In.
        for i in range (0, 256):
            r = int(math.floor((i / 256.0) * color.r))
            g = int(math.floor((i / 256.0) * color.g))
            b = int(math.floor((i / 256.0) * color.b))
            self.set_color_all(Color(r, g, b))
            self.show()
            time.sleep(wait_ms / 1000.0)
        #Fade Out.
        for i in range (256, 0, -1):
            r = int(math.floor((i / 256.0) * color.r))
            g = int(math.floor((i / 256.0) * color.g))
            b = int(math.floor((i / 256.0) * color.b))
            self.set_color_all(Color(r, g, b))
            self.show()
            time.sleep(wait_ms / 1000.0)

    ## Wipe color across the display one pixel at a time
    def color_wipe(self, color, wait_ms=50):
        for i in range(self.LED_COUNT):
            self.set_pixel_color(i, color)
            self.show()
            time.sleep(wait_ms / 1000.0)
    
    ## Fade from one color into another in a certain amount of steps
    def color_fade(self, color_from, color_to, wait_ms=20, steps=100):
        step_R = (color_to.r - color_from.r) / steps
        step_G = (color_to.g - color_from.g) / steps
        step_B = (color_to.b - color_from.b) / steps

        r = color_from.r
        g = color_from.g
        b = color_from.b

        for x in range(steps):
            c = Color(int(r), int(g), int(b))
            for i in range(self.LED_COUNT):
                self.set_pixel_color(i, c)
            self.show()
            time.sleep(wait_ms / 1000.0)
            r += step_R
            g += step_G
            b += step_B

    ## Displays random pixels across the display (one color)
    def sparkle(self, color, wait_ms=50, cummulative=False):
        self.clear_all()
        for i in range (0, self.LED_COUNT):
            self.set_pixel_color(random.randrange(0, self.LED_COUNT), color)
            self.show()
            time.sleep(wait_ms / 1000.0)
            if not cummulative:
                self.clear_all()
        time.sleep(wait_ms / 1000.0)

    ## Displays random pixels across the display (multiple colors)
    def sparkle_multicolor(self, wait_ms=50, cummulative=False):
        self.clear_all()
        for i in range (0, self.LED_COUNT):
            self.set_pixel_color(random.randrange(0, self.LED_COUNT), Color(random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256)))
            self.show()
            time.sleep(wait_ms / 1000.0)
            if not cummulative:
                self.clear_all()
        time.sleep(wait_ms / 1000.0)

    ## Draw rainbow that fades across all pixels at once
    def rainbow(self, wait_ms=50, iterations=1):
        for j in range(256 * iterations):
            for i in range(self.LED_COUNT):
                self.set_pixel_color(i, self.wheel((i + j) & 255))
            self.show()
            time.sleep(wait_ms / 1000.0)

    ## Draw rainbow that uniformly distributes itself across all pixels
    def rainbow_cycle(self, wait_ms=50, iterations=5):
        for j in range(256 * iterations):
            for i in range(self.LED_COUNT):
                self.set_pixel_color(i, self.wheel(
                    (int(i * 256 / self.LED_COUNT) + j) & 255))
            self.show()
            time.sleep(wait_ms / 1000.0)

    ## Movie theater light style chaser animation
    def theater_chase(self, color, wait_ms=50, iterations=10):
        for j in range(iterations):
            for q in range(3):
                for i in range(0, self.LED_COUNT, 3):
                    self.set_pixel_color(i + q, color)
                self.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.LED_COUNT, 3):
                    self.set_pixel_color(i + q, 0)

    ## Movie theater light style chaser animation
    ## It will cycle through all the colors
    def theater_chase_rainbow(self, wait_ms=50):
        for j in range(256):
            for q in range(3):
                for i in range(0, self.LED_COUNT, 3):
                    self.set_pixel_color(i + q, self.wheel((i + j) % 255))
                self.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.LED_COUNT, 3):
                    self.set_pixel_color(i + q, 0)

    def running(self, wait_ms = 10, duration_ms = 18000, width = 1):
        self.clear_all()
        index = 0
        while duration_ms > 0:
            self.set_pixel_color((index - width) % self.LED_COUNT, Color(0,0,0))
            self.set_pixel_color(index, Color(255,0,0))
            self.show()
            index = (index + 1) % self.LED_COUNT
            duration_ms -= wait_ms
            time.sleep(wait_ms / 1000)
