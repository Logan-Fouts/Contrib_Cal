import ntptime
import utime
import time
import machine
import gc
from wifi_utils import connect_wifi
from github_tracker import GITHUB_TRACKER
from led_utils import LED_UTILS

import socket
def test_dns():
    try:
        addr = socket.getaddrinfo("google.com", 80)[0][-1]
        print("✅ DNS works! IP:", addr[0])
    except Exception as e:
        print("❌ DNS failed:", e)
        
def test_internet():
    try:
        s = socket.socket()
        s.connect(("142.250.190.46", 80))
        s.close()
        print("✅ Internet works!")
    except Exception as e:
        print("❌ No internet:", e)


def sync_time():
    try:
        # Calculate UTC offset for New York (UTC-4 or UTC-5)
        is_dst = utime.localtime()[1] > 3 and utime.localtime()[1] < 11  # DST from April to October
        UTC_OFFSET = -4 * 3600 if is_dst else -5 * 3600
        
        ntptime.host = "time.cloudflare.com"
        ntptime.settime()
        
        current_time = utime.localtime(utime.mktime(utime.localtime()) + UTC_OFFSET)
        print("New York time synced:", current_time)
    except Exception as e:
        print("NTP sync failed:", e)

def main():
    gc.collect()
    num_days = 7
    leds = LED_UTILS(num_days)
    #leds.startup_animation()
    leds.turn_all_off()
    wlan = connect_wifi()
    test_dns()
    test_internet()
    sync_time()
    
    gh_tracker = GITHUB_TRACKER(num_days)
    
    while True:
        event_counts = gh_tracker.fetch_github_events()
        leds.update_leds(event_counts)
        time.sleep(1000)

if __name__ == "__main__":
    main()
