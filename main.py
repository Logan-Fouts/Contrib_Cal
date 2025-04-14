import utime
from wifi_utils import WIFI_UTILS
from github_tracker import GITHUB_TRACKER
from led_utils import LED_UTILS
from config_manager import CONFIG_MANAGER

import machine

def detect_button_press(button, wifi, leds, poll_rate=0.1, run_time=60*60):
    for i in range(run_time *  int(1/poll_rate)):
        first = button.value()
        utime.sleep(poll_rate)
        second = button.value()
        if first and not second:
            print('Button pressed!')
            leds.startup_animation()
            #wifi.start_config_portal()
            break
        elif not first and second:
            print('Button released!')
            break

def main():
    pin_num = 28
    num_days, run_freq = 21, 60 * 30
    none_color, event_color = (255, 255, 255), (0, 255, 0)
    
    config_manager = CONFIG_MANAGER()
    config = config_manager.load_config()
    
    leds = LED_UTILS(num_days, config['STARTUP_ANIMATION'], none_color, event_color, pin_num)
    wifi = WIFI_UTILS(config_manager)
    gh_tracker = GITHUB_TRACKER(num_days)
    
    button = machine.Pin(27, machine.Pin.IN, machine.Pin.PULL_UP)
    
    while True:
        event_counts = gh_tracker.fetch_github_events()
        leds.update_leds(event_counts)
        detect_button_press(button, wifi, leds, poll_rate=0.1, run_time=run_freq)

if __name__ == "__main__":
    main()
