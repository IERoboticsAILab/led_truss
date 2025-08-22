import time
import numpy as np
import random
import requests
import threading
from rpi_ws281x import *

class truss:
    def __init__(self, strip1_count=896, strip2_count=894, strip1_pin=18, strip2_pin=13, freq=800000, dma=10, brightness=125):
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

        # Effect orchestration
        self._lock = threading.Lock()
        self._cancel_event = threading.Event()
        self._effect_thread = None

    def _run_effect(self, target, args):
        try:
            target(*args)
        finally:
            with self._lock:
                self._effect_thread = None

    def stop_effect(self, timeout=2.0):
        with self._lock:
            thread = self._effect_thread
            if thread is None:
                return
            self._cancel_event.set()
        thread.join(timeout=timeout)
        with self._lock:
            if self._effect_thread is thread:
                self._effect_thread = None
            self._cancel_event.clear()

    def start_effect(self, effect_name, *args, clear_first=True):
        self.stop_effect()
        if clear_first:
            self.clear_all()
        effect_fn = getattr(self, effect_name)
        with self._lock:
            self._cancel_event.clear()
            self._effect_thread = threading.Thread(target=self._run_effect, args=(effect_fn, args), daemon=True)
            self._effect_thread.start()

    # Auxiliary Functions
    def set_pixel_color(self, pixel_index, color):
        if pixel_index < self.STRIP1_COUNT:
            self.strip1.setPixelColor(pixel_index, color)

        else: 
            pixel_index_new = int(self.STRIP2_COUNT - (pixel_index - self.STRIP1_COUNT)) -1
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
    ## Glowing effect (runs continuously until stopped)
    def glow(self, color, wait_ms=10):
        phase = 0.0
        while True:
            if self._cancel_event.is_set():
                return
            brightness_scale = (1.0 - np.cos(phase)) * 0.5
            r = int(color.r * brightness_scale)
            g = int(color.g * brightness_scale)
            b = int(color.b * brightness_scale)
            c = Color(r, g, b)
            for i in range(self.LED_COUNT):
                self.set_pixel_color(i, c)
            self.show()
            phase += 0.1
            time.sleep(wait_ms / 1000.0)

    ## Sends moving cosine waves (with amplitude 1) throughtout the LEDs (continuous)
    def wave(self, color, cycles=1, speed=0.1, wait_ms=10):
        i = 0
        while True:
            if self._cancel_event.is_set():
                return
            cos_lookup = (np.cos(np.linspace(np.pi-(i*speed), (np.pi*(cycles*3))-(i*speed), self.LED_COUNT)) + 1) * 0.5
            color_lookup = np.tile(np.array((color.r, color.g, color.b), dtype=np.uint8), [self.LED_COUNT, 1])
            cos_color_table = np.multiply(color_lookup, cos_lookup[:, np.newaxis],).astype(int)

            for j in range(self.LED_COUNT):
                c = Color(cos_color_table[j][0], cos_color_table[j][1], cos_color_table[j][2])
                self.set_pixel_color(j, c)

            self.show()
            i += 1
            time.sleep(wait_ms / 1000.0)

    ## Wipe color across the display one pixel at a time
    def color_wipe(self, color, wait_ms=50):
        for i in range(self.LED_COUNT):
            if self._cancel_event.is_set():
                return
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
            if self._cancel_event.is_set():
                return
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
            if self._cancel_event.is_set():
                return
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
            if self._cancel_event.is_set():
                return
            self.set_pixel_color(random.randrange(0, self.LED_COUNT), Color(random.randrange(0, 256), random.randrange(0, 256), random.randrange(0, 256)))
            self.show()
            time.sleep(wait_ms / 1000.0)
            if not cummulative:
                self.clear_all()
        time.sleep(wait_ms / 1000.0)

    ## Draw rainbow that fades across all pixels at once (continuous)
    def rainbow(self, wait_ms=50):
        j = 0
        while True:
            if self._cancel_event.is_set():
                return
            for i in range(self.LED_COUNT):
                self.set_pixel_color(i, self.wheel((i + j) & 255))
            self.show()
            j = (j + 1) % 256
            time.sleep(wait_ms / 1000.0)

    ## Draw rainbow that uniformly distributes itself across all pixels (continuous)
    def rainbow_cycle(self, wait_ms=50):
        j = 0
        while True:
            if self._cancel_event.is_set():
                return
            for i in range(self.LED_COUNT):
                self.set_pixel_color(i, self.wheel((int(i * 256 / self.LED_COUNT) + j) & 255))
            self.show()
            j = (j + 1) % 256
            time.sleep(wait_ms / 1000.0)

    ## Movie theater light style chaser animation (continuous)
    def theater_chase(self, color, wait_ms=50):
        while True:
            if self._cancel_event.is_set():
                return
            for q in range(3):
                if self._cancel_event.is_set():
                    return
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
            if self._cancel_event.is_set():
                return
            for q in range(3):
                for i in range(0, self.LED_COUNT, 3):
                    self.set_pixel_color(i + q, self.wheel((i + j) % 255))
                self.show()
                time.sleep(wait_ms / 1000.0)
                for i in range(0, self.LED_COUNT, 3):
                    self.set_pixel_color(i + q, 0)

    def running(self, wait_ms = 10, width = 1):
        self.clear_all()
        index = 0
        while True:
            if self._cancel_event.is_set():
                return
            self.set_pixel_color((index - width) % self.LED_COUNT, Color(0,0,0))
            self.set_pixel_color(index, Color(255,0,0))
            self.show()
            index = (index + 1) % self.LED_COUNT
            time.sleep(wait_ms / 1000)


    def bitcoin(self, time_threshold_in_secs = 30):
        """Monitor Bitcoin price and show changes on the LED truss.
        
        Args:
            duration (int): Total duration to monitor in seconds
            time_threshold_in_secs (int): How long to show each price change
            
        Returns:
            dict: Status of the operation
        """
        key = "https://api.binance.com/api/v3/ticker/price?symbol=BTCEUR"
        previous_price = 0

        while True:
            if self._cancel_event.is_set():
                return
            # Get current Bitcoin price
            data = requests.get(key, timeout=5).json()
            current_price = float(data['price'])

            # Show price change visualization
            timeout = time.time() + time_threshold_in_secs

            if current_price > previous_price:
                while time.time() < timeout:
                    if self._cancel_event.is_set():
                        return
                    self.glow(Color(0, 255, 0))  # Green for price increase
            elif current_price < previous_price:
                while time.time() < timeout:
                    if self._cancel_event.is_set():
                        return
                    self.glow(Color(255, 0, 0))  # Red for price decrease
            else:
                while time.time() < timeout:
                    if self._cancel_event.is_set():
                        return
                    self.glow(Color(255, 255, 255))  # White for no change
            
            previous_price = current_price

    def heart_rate(self, url, poll_hz = 1.0, min_hr = 40, yellow_start = 75, red_start = 120, max_hr = 200, pulse = True):
        """Read heart rate from an app.heart.io-like widget and map value to color.

        Simple implementation: open the page, read `.heartrate` every tick, set color.
        """

        from playwright.sync_api import sync_playwright

        def clamp(value, low, high):
            return max(low, min(high, value))

        def lerp(a, b, t):
            return int(a + (b - a) * t)

        def color_from_hr(hr_value):
            # Gradient: green -> yellow -> red, returns (r, g, b)
            hr = clamp(hr_value, min_hr, max_hr)
            if hr <= yellow_start:
                # green (0,255,0) to yellow (255,255,0)
                t = 1.0 if yellow_start == min_hr else (hr - min_hr) / float(max(1, yellow_start - min_hr))
                return (lerp(0, 255, t), 255, 0)
            if hr < red_start:
                # yellow (255,255,0) to red (255,0,0)
                t = 1.0 if red_start == yellow_start else (hr - yellow_start) / float(max(1, red_start - yellow_start))
                return (255, lerp(255, 0, t), 0)
            return (255, 0, 0)

        def compute_bpm_period_seconds(hr_value):
            safe_hr = max(1, hr_value)
            return 60.0 / float(safe_hr)

        # Support multiple URLs separated by commas; compute average heart rate
        urls = [u.strip() for u in str(url).split(',') if u.strip()]
        if not urls:
            urls = [str(url)]

        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            try:
                pages = []
                for u in urls:
                    pg = browser.new_page()
                    pg.goto(u, wait_until="domcontentloaded")
                    pg.wait_for_selector(".heartrate", timeout=20000)
                    pages.append(pg)

                latest_hr = None
                next_poll_time = 0.0
                poll_period = 1.0 / float(max(0.1, poll_hz))
                while True:
                    if self._cancel_event.is_set():
                        return
                    now = time.time()
                    # Polling in Hz
                    if now >= next_poll_time:
                        values = []
                        for pg in pages:
                            try:
                                text = pg.inner_text(".heartrate")
                                digits = ''.join(ch for ch in text if ch.isdigit())
                                if digits:
                                    values.append(int(digits))
                            except Exception:
                                # Ignore read errors for individual pages in this cycle
                                pass
                        if values:
                            latest_hr = int(round(sum(values) / float(len(values))))
                        else:
                            # If no numeric HR is visible (e.g., "-"), treat as 0 to show solid green
                            latest_hr = 0
                        next_poll_time = now + poll_period

                    # Determine color from latest HR (fallback to green if unknown)
                    base_rgb = (0, 255, 0) if latest_hr is None else color_from_hr(latest_hr)

                    # Glow at HR frequency if enabled: brightness follows cosine with period derived from BPM
                    if pulse and latest_hr is not None and latest_hr > 0:
                        period = compute_bpm_period_seconds(latest_hr)
                        # map current time to [0..1] phase
                        phase = (now % period) / period
                        # cosine brightness [0..1]
                        brightness_scale = (1.0 - np.cos(phase * 2 * np.pi)) * 0.5
                    else:
                        brightness_scale = 1.0

                    # Apply scaled brightness to the display color
                    r = int(base_rgb[0] * brightness_scale)
                    g = int(base_rgb[1] * brightness_scale)
                    b = int(base_rgb[2] * brightness_scale)
                    scaled_color = Color(r, g, b)
                    self.set_color_all(scaled_color)

                    # Small frame delay for smooth animation
                    time.sleep(0.02)
            finally:
                browser.close()
        