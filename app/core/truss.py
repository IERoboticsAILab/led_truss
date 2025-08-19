import time
import numpy as np
import random
import requests
from rpi_ws281x import *

class truss:
    def __init__(self, strip1_count=900, strip2_count=900, strip1_pin=18, strip2_pin=13, freq=800000, dma=10, brightness=125):
        # 
        self.STRIP1_COUNT = strip1_count  # Number of LEDs in strip 1
        self.STRIP2_COUNT = strip2_count  # Number of LEDs in strip 2
        self.LED_COUNT = strip1_count + strip2_count  # Total LED count
        self.STRIP1_PIN = strip1_pin     # GPIO pin for strip 1
        self.STRIP2_PIN = strip2_pin     # GPIO pin for strip 2
        self.LED_FREQ_HZ    = freq       # LED signal frequency in hertz (usually 800khz)
        self.LED_DMA        = dma        # DMA channel to use for generating a signal (try 10)
        self.LED_BRIGHTNESS = brightness # Set to 0 for darkest and 255 for brightest
        self.LED_INVERT     = False      # True to invert the signal (when using NPN transistor level shift)
        self.LED_CHANNEL    = None       # set to '1' for GPIOs 13, 19, 41, 45 or 53

        self.strip1 = Adafruit_NeoPixel(self.STRIP1_COUNT, 
                                   self.STRIP1_PIN, 
                                   self.LED_FREQ_HZ, 
                                   self.LED_DMA, 
                                   self.LED_INVERT, 
                                   self.LED_BRIGHTNESS, 
                                   0)

        self.strip2 = Adafruit_NeoPixel(self.STRIP2_COUNT, 
                                   self.STRIP2_PIN, 
                                   self.LED_FREQ_HZ, 
                                   self.LED_DMA, 
                                   self.LED_INVERT, 
                                   self.LED_BRIGHTNESS, 
                                   1)


        self.strip1.begin()
        self.strip2.begin()

    # Auxiliary Functions
    def set_pixel_color(self, pixel_index, color):
        if pixel_index < self.STRIP1_COUNT:
            pixel_index_new = int(self.STRIP1_COUNT - 1 - pixel_index)
            self.strip1.setPixelColor(pixel_index_new, color)
        else: 
            pixel_index_new = int(pixel_index - self.STRIP1_COUNT)
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

    def set_brightness(self, brightness):
        self.strip1.setBrightness(brightness)
        self.strip2.setBrightness(brightness)

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
    def glow(self, color, frames=300, wait_ms=10):
        cos_lookup = (np.cos(np.linspace(np.pi, np.pi*3, frames)) + 1) * 0.5
        color_lookup = np.tile(np.array((color.r, color.g, color.b), dtype=np.uint8), [frames, self.LED_COUNT])
        cos_color_table = np.multiply(color_lookup, cos_lookup[:, np.newaxis],).astype(int)
        
        for f in range(frames):
            for i in range(self.LED_COUNT):
                c = Color(cos_color_table[f][i*3], cos_color_table[f][(i*3)+1], cos_color_table[f][(i*3)+2])
                self.set_pixel_color(i, c)
            self.show()
            time.sleep(wait_ms / 1000.0)

    ## Sends moving cosine waves (with amplitude 1) throughtout the LEDs
    def wave(self, color, frames=300, cycles=1, speed=0.1, wait_ms=10):
        for i in range(frames):
            cos_lookup = (np.cos(np.linspace(np.pi-(i*speed), (np.pi*(cycles*3))-(i*speed), self.LED_COUNT)) + 1) * 0.5
            color_lookup = np.tile(np.array((color.r, color.g, color.b), dtype=np.uint8), [self.LED_COUNT, 1])
            cos_color_table = np.multiply(color_lookup, cos_lookup[:, np.newaxis],).astype(int)
        
            for i in range(self.LED_COUNT):
                c = Color(cos_color_table[i][0], cos_color_table[i][1], cos_color_table[i][2])
                self.set_pixel_color(i, c)
            
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


    def bitcoin(self, duration = 60, time_threshold_in_secs = 30):
        """Monitor Bitcoin price and show changes on the LED truss.
        
        Args:
            duration (int): Total duration to monitor in seconds
            time_threshold_in_secs (int): How long to show each price change
            
        Returns:
            dict: Status of the operation
        """
        key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCEUR"
        previous_price = 0
        total_end_time = time.time() + duration

        while time.time() < total_end_time:
            # Get current Bitcoin price
            data = requests.get(key, timeout=5).json()
            current_price = float(data['price'])

            # Show price change visualization
            timeout = time.time() + time_threshold_in_secs

            if current_price > previous_price:
                while time.time() < timeout:
                    self.glow(Color(0, 255, 0))  # Green for price increase
            elif current_price < previous_price:
                while time.time() < timeout:
                    self.glow(Color(255, 0, 0))  # Red for price decrease
            else:
                while time.time() < timeout:
                    self.glow(Color(255, 255, 255))  # White for no change
            
            previous_price = current_price

    def heart_rate(self, url, duration = 300, poll_interval_ms = 5000, min_hr = 40, yellow_start = 75, red_start = 120, max_hr = 200):
        """Fetch heart rate from a URL and visualize status from green to red.

        The strip is filled with a solid color mapped from heart rate:
        - Green within [min_hr, yellow_start)
        - Gradient from green→yellow within [min_hr, yellow_start)
        - Gradient from yellow→red within [yellow_start, red_start)
        - Red at or above red_start
        Values are clamped within [min_hr, max_hr].
        """

        def clamp(value, low, high):
            return max(low, min(high, value))

        def lerp(a, b, t):
            return int(a + (b - a) * t)

        def color_from_hr(hr_value):
            hr = clamp(hr_value, min_hr, max_hr)
            if hr <= yellow_start:
                # green (0,255,0) to yellow (255,255,0)
                if yellow_start == min_hr:
                    t = 1.0
                else:
                    t = (hr - min_hr) / float(yellow_start - min_hr)
                r = lerp(0, 255, t)
                g = 255
                b = 0
                return Color(r, g, b)
            elif hr < red_start:
                # yellow (255,255,0) to red (255,0,0)
                if red_start == yellow_start:
                    t = 1.0
                else:
                    t = (hr - yellow_start) / float(red_start - yellow_start)
                r = 255
                g = lerp(255, 0, t)
                b = 0
                return Color(r, g, b)
            else:
                return Color(255, 0, 0)

        end_time = time.time() + duration
        while time.time() < end_time:
            try:
                resp = requests.get(url, timeout=5)
                resp.raise_for_status()
                hr_val = None
                # Try JSON first
                try:
                    data = resp.json()
                    # common keys
                    for key in ("hr", "heart_rate", "heartRate", "bpm", "value"):
                        if isinstance(data, dict) and key in data:
                            hr_val = float(data[key])
                            break
                    if hr_val is None and isinstance(data, (int, float)):
                        hr_val = float(data)
                except ValueError:
                    # Fallback to plain text
                    txt = resp.text.strip()
                    # Extract first float-like number
                    num = ''
                    for ch in txt:
                        if ch.isdigit() or ch in ['.', ',']:
                            num += ('.' if ch == ',' else ch)
                        elif num:
                            break
                    if num:
                        hr_val = float(num)

                if hr_val is None:
                    # Could not parse; show blue as error
                    self.set_color_all(Color(0, 0, 255))
                else:
                    c = color_from_hr(hr_val)
                    self.set_color_all(c)
            except Exception:
                # network or parse error -> magenta
                self.set_color_all(Color(255, 0, 255))

            time.sleep(poll_interval_ms / 1000.0)
        