import utime
from wifi_utils import WIFI_UTILS
from github_tracker import GITHUB_TRACKER
from led_utils import LED_UTILS

def main():
    num_days = 14
    run_freq = 60 * 60 # One hour
    
    leds = LED_UTILS(num_days, animation=3)
    wifi = WIFI_UTILS()
    gh_tracker = GITHUB_TRACKER(num_days)
    
    while True:
        event_counts = gh_tracker.fetch_github_events()
        leds.update_leds(event_counts)
        utime.sleep(run_freq)

if __name__ == "__main__":
    main()