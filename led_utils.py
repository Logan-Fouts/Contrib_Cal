from machine import Pin
import neopixel
import time
import random

class LED_UTILS:
    
    def __init__(self, num_days=7, pin_num=28):
        self.num_leds = num_days
        self.pin = Pin(pin_num, Pin.OUT, value=0)
        time.sleep_ms(100) 
        self.np = neopixel.NeoPixel(self.pin, self.num_leds)
        self.turn_all_off()

    def startup_animation(self):
        """Advanced startup animation with multiple effects"""
        colors = [
            ('red', (255, 0, 0)),
            ('green', (0, 255, 0)),
            ('blue', (0, 0, 255)),
            ('yellow', (255, 255, 0)),
            ('purple', (128, 0, 128)),
            ('cyan', (0, 255, 255)),
            ('orange', (255, 165, 0))
        ]
        
        # 1. Sequential pop effect
        for i in range(self.num_leds):
            color_name, color_rgb = colors[i % len(colors)]
            self.set_led(i, color_name, 30)
            time.sleep_ms(50)
            self.set_led(i, 'off', 0)
        
        # 2. Color wave
        for _ in range(2):
            for color_name, color_rgb in colors:
                for i in range(self.num_leds):
                    self.set_led(i, color_name, 30)
                    if i > 0:
                        self.set_led(i-1, color_name, 15)  # Dim previous
                    time.sleep_ms(100)
                self.turn_all_off()
        
        # 3. Sparkle finale
        for _ in range(50):
            idx = random.randint(0, self.num_leds-1)
            color_name, color_rgb = random.choice(colors)
            self.set_led(idx, color_name, 30)
            time.sleep_ms(100)
            self.set_led(idx, 'off', 0)
        
        # 4. Smooth fill to white
        for bri in range(0, 30, 1):
            self.fill('white', bri)
            time.sleep_ms(100)
        

        self.turn_all_off()

    def set_led(self, led_index, color, brightness=50):
        """Properly handles color order (GRB for NeoPixels/APA106)"""
        if isinstance(color, str):
            colors = {
                'red': (255, 0, 0),
                'green': (0, 255, 0),
                'blue': (0, 0, 255),
                'yellow': (255, 255, 0),
                'purple': (128, 0, 128),
                'white': (255, 255, 255),
                'off': (0, 0, 0),
                'cyan': (0, 255, 255),
                'orange': (255, 165, 0)
            }
            r, g, b = colors.get(color.lower(), (0, 0, 0))
        else:
            r, g, b = color
        
        brightness = max(0, min(100, brightness))
        r = int(r * brightness / 100)
        g = int(g * brightness / 100)
        b = int(b * brightness / 100)
        
        self.np[led_index] = (g, r, b)
        self.np.write()

    def fill(self, color, brightness=50):
        """Fill all LEDs with color"""
        for i in range(self.num_leds):
            self.set_led(i, color, brightness)
    
    def turn_all_off(self):
        """Turn off all LEDs reliably"""
        self.np.fill((0, 0, 0))
        self.np.write()

    def update_leds(self, event_counts):
        """Visualize event counts with brightness levels"""
        max_count = max(event_counts) if event_counts else 1
        
        for day in range(min(self.num_leds, len(event_counts))):
            count = event_counts[day]
            if count > 0:
                # Scale brightness between 20-70%
                brightness = 20 + int(60 * (count / max_count))
                self.set_led(day, 'green', brightness)
            else:
                self.set_led(day, 'red', 20)
            time.sleep_ms(50)
            
    def breathe(self):
        while True:
            for bri in range(0, 30, 1):
                self.fill('green', bri)
                time.sleep_ms(50)
            for bri in range(30, 0, -1):
                self.fill('green', bri)
                time.sleep_ms(50)

