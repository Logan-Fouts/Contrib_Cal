import utime
from wifi_utils import WIFI_UTILS
from github_tracker import GITHUB_TRACKER
from led_utils import LED_UTILS
from config_manager import CONFIG_MANAGER

def main():
    pin_num = 28
    num_days, run_freq = 14, 60 * 60
    none_color, event_color = (255, 0, 0), (0, 255, 0)
    
    config_manager = CONFIG_MANAGER()
    config = config_manager.load_config()
    
    leds = LED_UTILS(num_days, config['STARTUP_ANIMATION'], none_color, event_color, pin_num)
    wifi = WIFI_UTILS(config_manager)
    gh_tracker = GITHUB_TRACKER(num_days)
    
    while True:
        event_counts = gh_tracker.fetch_github_events()
        leds.update_leds(event_counts)
        utime.sleep(run_freq)

if __name__ == "__main__":
    main()
