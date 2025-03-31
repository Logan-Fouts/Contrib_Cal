from machine import Pin
import neopixel
import time
import utime

# Initialize NeoPixel strip on GP28 with 5 LEDs
np = neopixel.NeoPixel(Pin(28), 5)

def set_led(led_index, color, brightness=50):
    """
    Set a single NeoPixel LED with color and brightness.
    
    Args:
        led_index (int): LED position (0 to 29).
        color (str): 'red', 'green', 'blue', 'yellow', etc.
        brightness (int): 0-255 (lower = safer for USB power).
    """

    colors = {
        'red': (255, 0, 0), 'green': (0, 255, 0), 'blue': (0, 0, 255),
        'yellow': (255, 200, 0), 'orange': (255, 100, 0), 'purple': (150, 0, 255),
        'indigo': (75, 0, 130), 'teal': (0, 180, 180), 'pink': (255, 50, 150),
        'warmwhite': (255, 180, 150), 'coolwhite': (200, 200, 255), 'amber': (255, 120, 0),
        'gold': (255, 215, 0), 'lavender': (180, 130, 255), 'mint': (100, 255, 180),
        'peach': (255, 160, 120), 'skyblue': (100, 200, 255), 'magenta': (255, 0, 150),
        'cyan': (0, 255, 255), 'lime': (150, 255, 0), 'turquoise': (0, 255, 200),
        'halloween': (255, 100, 0), 'xmas_red': (255, 10, 10), 'xmas_green': (10, 255, 10),
        'valentine': (255, 50, 100), 'sunrise': (255, 100, 50), 'forest': (0, 80, 0),
        'ocean': (0, 50, 150), 'dim_red': (50, 0, 0), 'dim_blue': (0, 0, 50),
        'dim_green': (0, 50, 0), 'off': (0, 0, 0), 'warm_dim': (80, 50, 30)
    }
    
    r, g, b = colors.get(color.lower(), (0, 0, 0))
    r = int(r * (brightness / 255))
    g = int(g * (brightness / 255))
    b = int(b * (brightness / 255))
    
    np[led_index] = (g, r, b)  # GRB order should be fixed later
    np.write()

def startup_animation():
    # Color wave pattern
    wave_colors = ['cyan', 'magenta', 'yellow', 'teal', 'purple']
    
    # Ripple out from center
    for color in wave_colors:
        # Expand outward
        for pos in range(3):
            set_led(2 - pos, color, 100)  # Move left
            set_led(2 + pos, color, 100)  # Move right
            utime.sleep(0.05)
            turn_all_off()
        
        # Collapse inward
        for pos in reversed(range(3)):
            set_led(2 - pos, color, 100)
            set_led(2 + pos, color, 100)
            utime.sleep(0.05)
            turn_all_off()
    
    # Final burst
    for i in range(5):
        for led in range(5):
            set_led(led, wave_colors[i % len(wave_colors)], 100)
        utime.sleep(0.1)
    turn_all_off()

def turn_all_off():
    np.fill((0, 0, 0))
    np.write()

def update_leds(event_counts):
    max_count = max(event_counts) if max(event_counts) > 0 else 1
    
    for day in range(5):
        count = event_counts[day]
        if count > 0:
            brightness = 15 + int(35 * (count / max_count))
            set_led(day, 'green', brightness)
        else:
            set_led(day, 'red', 25)
        utime.sleep(0.1)