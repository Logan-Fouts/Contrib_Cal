import ntptime
import utime
import machine
import gc
from wifi_utils import connect_wifi
from github_tracker import GITHUB_TRACKER
from led_utils import LED_UTILS

def sync_time():
    try:
        ntptime.settime()
        # New York time (UTC-4 or UTC-5)
        UTC_OFFSET = -4 * 3600 if (utime.localtime()[1] > 3 and utime.localtime()[1] < 11) else -5 * 3600
        
        # Manually adjust the time
        current_time = utime.time() + UTC_OFFSET
        machine.RTC().datetime(utime.localtime(current_time))
        
        print("Time synced:", utime.localtime(current_time))
    except Exception as e:
        print("NTP sync failed:", e)

def main():
    gc.collect()
    num_days = 7
    leds = LED_UTILS(num_days)
    leds.startup_animation()
    leds.breathe()
    leds.turn_all_off()
    wlan = connect_wifi()
    #sync_time()
    
    gh_tracker = GITHUB_TRACKER(num_days)
    
    while True:
        event_counts = gh_tracker.fetch_github_events()
        leds.update_leds(event_counts)
        utime.sleep(3600)

if __name__ == "__main__":
    main()
