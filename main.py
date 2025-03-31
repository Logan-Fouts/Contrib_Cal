import ntptime
import utime
import machine
import gc
from wifi_utils import connect_wifi
from github_tracker import fetch_github_events, get_event_counts
from led_utils import update_leds, startup_animation

def sync_time():
    try:
        ntptime.settime()
        # New York time (UTC-4 or UTC-5)
        UTC_OFFSET = -4 * 3600 if (utime.localtime()[1] > 3 and utime.localtime()[1] < 11) else -5 * 3600
        utime.timezone(UTC_OFFSET)
        print("Time synced:", utime.localtime())
    except Exception as e:
        print("NTP sync failed:", e)

def main():
    gc.collect()
    startup_animation()
    wlan = connect_wifi()
    sync_time()
    
    while True:
        events = fetch_github_events()
        event_counts = get_event_counts(events)
        update_leds(event_counts)
        utime.sleep(3600)

if __name__ == "__main__":
    main()