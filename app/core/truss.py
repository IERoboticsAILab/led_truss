import time
import numpy as np
import random
import requests
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

    def set_colors(self, colors):
        """Set the entire strip from a list of Color(...) values and show once."""
        count = min(len(colors), self.LED_COUNT)
        for i in range(count):
            self.set_pixel_color(i, colors[i])
        # If provided list is shorter, leave remaining pixels as-is
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

    def heart_rate(self, url, duration = 300, poll_interval = 1, min_hr = 40, yellow_start = 75, red_start = 120, max_hr = 200, pattern = "trail"):
        """Render heart rate with fixed brightness using hue and motion only.

        - Brightness is constant across all HR values (fixed V in HSV).
        - HR maps to hue from green→yellow→red.
        - Motion encodes intensity (speed) and/or fill length; no brightness modulation.
        - EMA smoothing is applied to stabilize the HR value.
        """

        from playwright.sync_api import sync_playwright
        import threading
        import colorsys
        import math

        # Fixed brightness (0..1). Does not change with HR.
        FIXED_V = 0.8

        def _norm(x, lo, hi):
            return max(0.0, min(1.0, (x - lo) / float(hi - lo)))

        def hr_to_rgb_fixed(hr, lo=40, hi=200, sat=1.0, v=FIXED_V):
            t = _norm(hr, lo, hi)              # 0..1 across HR range
            h = (120.0 * (1.0 - t)) / 360.0    # 120°(green)→0°(red)
            r, g, b = colorsys.hsv_to_rgb(h, sat, v)
            return int(r * 255), int(g * 255), int(b * 255)

        def bpm_phase(hr, t=None):
            t = time.time() if t is None else t
            return (t * (hr / 60.0)) % 1.0

        # Patterns (no brightness modulation)
        def pat_solid(strip_self, hr, lo=40, hi=200):
            strip_self.set_color_all(Color(*hr_to_rgb_fixed(hr, lo, hi)))

        def pat_thermometer(strip_self, hr, n_leds, lo=40, hi=200):
            t = _norm(hr, lo, hi)
            lit = max(1, int(t * n_leds))
            out = []
            for i in range(n_leds):
                if i < lit:
                    frac = (i + 1) / float(n_leds)
                    c = hr_to_rgb_fixed(lo + frac * (hi - lo), lo, hi)  # hue gradient, fixed V
                    out.append(Color(*c))
                else:
                    out.append(Color(0, 0, 0))  # background off
            strip_self.set_colors(out)

        def pat_pulse_trail(strip_self, hr, n_leds, lo=40, hi=200, trail=0.35):
            base_r, base_g, base_b = hr_to_rgb_fixed(hr, lo, hi)
            now = time.time()
            pos = bpm_phase(hr, now) * (n_leds - 1)
            out = []
            for i in range(n_leds):
                d = abs(i - pos)
                gain = math.exp(-d * (6 * trail))  # spatial falloff only
                r = int(base_r * gain)
                g = int(base_g * gain)
                b = int(base_b * gain)
                out.append(Color(r, g, b))
            strip_self.set_colors(out)

        # Simple renderer state outside of an inner class
        renderer_state = {
            "lo": min_hr,
            "hi": max_hr,
            "ema_alpha": 0.35,
            "fps": 40,
            "pattern": pattern,
            "running": False,
            "hr_smooth": None,
        }

        def update_hr(hr_value):
            lo = renderer_state["lo"]
            hi = renderer_state["hi"]
            hr_value = max(lo, min(hi, hr_value))
            current = renderer_state["hr_smooth"]
            if current is None:
                renderer_state["hr_smooth"] = hr_value
            else:
                ema_alpha = renderer_state["ema_alpha"]
                renderer_state["hr_smooth"] = current + ema_alpha * (hr_value - current)

        def draw_frame():
            lo = renderer_state["lo"]
            hi = renderer_state["hi"]
            hr = renderer_state["hr_smooth"] if renderer_state["hr_smooth"] is not None else (lo + hi) / 2.0
            selected = renderer_state["pattern"]
            if selected == "solid":
                pat_solid(self, hr, lo, hi)
            elif selected == "thermo":
                pat_thermometer(self, hr, self.LED_COUNT, lo, hi)
            else:
                pat_pulse_trail(self, hr, self.LED_COUNT, lo, hi)

        def start_renderer(duration=None):
            renderer_state["running"] = True
            t_end = time.time() + duration if duration else None
            interval = 1.0 / float(renderer_state["fps"])    
            while renderer_state["running"] and (t_end is None or time.time() < t_end):
                draw_frame()
                time.sleep(interval)
            renderer_state["running"] = False

        # Create renderer with desired pattern; default to pulse trail
        render_thread = threading.Thread(target=start_renderer, kwargs={"duration": duration}, daemon=True)
        render_thread.start()

        # Poll HR and feed updates
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True, args=["--no-sandbox", "--disable-dev-shm-usage"])
            page = browser.new_page()
            page.goto(url, wait_until="domcontentloaded")
            page.wait_for_selector(".heartrate", timeout=20000)

            end_time = time.time() + duration
            while time.time() < end_time:
                text = page.inner_text(".heartrate")
                digits = ''.join(ch for ch in text if ch.isdigit())
                if digits:
                    try:
                        hr_val = int(digits)
                        update_hr(hr_val)
                    except ValueError:
                        pass
                time.sleep(poll_interval)

            browser.close()

        # Stop renderer
        renderer_state["running"] = False
        