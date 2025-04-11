from machine import Pin
import neopixel
import ntptime
import time
import random

class LED_UTILS:
    def __init__(self, num_days=7, pin_num=28, animation=3, none_color=(255, 0, 0), event_color=(0, 255, 0)):
        self.colors = [
            ('red', (255, 0, 0)),
            ('green', (0, 255, 0)),
            ('blue', (0, 0, 255)),
            ('yellow', (255, 255, 0)),
            ('purple', (128, 0, 128)),
            ('cyan', (0, 255, 255)),
            ('orange', (255, 165, 0)),
            ('white', (255, 255, 255)),
            ('off', (0, 0, 0))
        ]
        
        self.num_leds = num_days
        self.animation = animation
        self.none_color = none_color
        self.event_color = event_color
        
        self.pin = Pin(pin_num, Pin.OUT, value=0)
        self.np = neopixel.NeoPixel(self.pin, self.num_leds)
        
        self.turn_all_off()
        self.startup_animation()
        self.turn_all_off()

    def startup_animation(self):
        if self.animation == 0:
            pass
        elif self.animation == 1:
            # Sequential pop
            for i in range(self.num_leds):
                _, color_rgb = self.colors[i % len(self.colors)]
                self.set_led(i, color_rgb, 30)
                time.sleep_ms(50)
                self.set_led(i, self.colors[len(self.colors) - 1][1], 0)
        elif self.animation == 2:
            # Color wave
            for _ in range(2):
                for _, color_rgb in self.colors:
                    for i in range(self.num_leds):
                        self.set_led(i, color_rgb, 30)
                        if i > 0:
                            self.set_led(i-1, color_rgb, 15)
                        time.sleep_ms(100)
                    self.turn_all_off()
        elif self.animation == 3:
            # Sparkle
            for _ in range(50):
                idx = random.randint(0, self.num_leds-1)
                _, color_rgb = random.choice(self.colors)
                self.set_led(idx, color_rgb, 30)
                time.sleep_ms(100)
                self.set_led(idx, self.colors[len(self.colors) - 1][1], 0)
        else:
            # Smooth fill to white
            for bri in range(0, 30, 1):
                self.fill(self.colors[7][1], bri)
                time.sleep_ms(25)
    

        self.turn_all_off()

    def set_led(self, led_index, color, brightness=50):
        r, g, b = color
        
        brightness = max(0, min(100, brightness))
        r = int(r * brightness / 100)
        g = int(g * brightness / 100)
        b = int(b * brightness / 100)
        
        self.np[led_index] = (g, r, b)
        self.np.write()
        
    def fill(self, color, brightness=50):
        for i in range(self.num_leds):
            self.set_led(i, color, brightness)
    
    def turn_all_off(self):
        self.np.fill((0, 0, 0))
        self.np.write()

    def update_leds(self, event_counts):
        """Visualize github history with brightness levels"""
        max_count = max(event_counts) if event_counts else 1
        
        for day in range(min(self.num_leds, len(event_counts))):
            count = event_counts[day]
            if count > 0:
                # Scale brightness
                brightness = 1 + int(99 * (count / max_count))
                self.set_led(day, self.colors[1][1], brightness)
            else:
                self.set_led(day, self.colors[0][1], 20)
            time.sleep_ms(50)

