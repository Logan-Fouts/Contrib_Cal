import network
import urequests
import utime
import ntptime
import gc
from secrets import WIFI_SSID, WIFI_PASSWORD, GITHUB_USERNAME, GITHUB_TOKEN
from led_utils import set_led

def connect_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.active(True)
    if not wlan.isconnected():
        print("Connecting to Wi-Fi...")
        wlan.connect(WIFI_SSID, WIFI_PASSWORD)
        while not wlan.isconnected():
            pass
    print("Connected! IP:", wlan.ifconfig()[0])
    
    # Sync time with NTP server
    try:
        ntptime.settime()
        print("Time synced:", utime.localtime())
    except Exception as e:
        print("NTP sync failed:", e)
    return wlan

def fetch_github_events(max_events=100):
    all_events = []
    page = 1
    per_page = 30
    
    while len(all_events) < max_events:
        url = f"https://api.github.com/users/{GITHUB_USERNAME}/events?page={page}&per_page={per_page}"
        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "User-Agent": "PicoW"
        }
        
        try:
            print(f"Fetching page {page}...")
            response = urequests.get(url, headers=headers)
            
            if response.status_code != 200:
                print(f"API Error {response.status_code}: {response.text[:200]}")
                break
                
            try:
                events = response.json()
                print(f"Got {len(events)} events in page {page}")
                all_events.extend(events)
                
                if len(events) < per_page:
                    break
                    
                page += 1
                utime.sleep(1)
                
            except ValueError as e:
                print(f"JSON Error: {e}")
                print("Response start:", response.text[:200])
                break
                
        except Exception as e:
            print(f"Request failed: {str(e)}")
            break
            
    print(f"Total events collected: {len(all_events)}")
    return all_events[:max_events]

def parse_github_date(date_str):
    try:
        return (
            int(date_str[0:4]),  # year
            int(date_str[5:7]),  # month
            int(date_str[8:10]), # day
            0, 0, 0, 0, 0
        )
    except:
        return (2020, 1, 1, 0, 0, 0, 0, 0)

def get_event_counts(events, days=5):
    event_counts = [0] * days
    now = utime.time()
    
    for event in events:
        try:
            # Proper JSON access (event is already a dict)
            created_at = event['created_at']
            year = int(created_at[0:4])
            month = int(created_at[5:7])
            day = int(created_at[8:10])
            
            event_time = utime.mktime((year, month, day, 0, 0, 0, 0, 0))
            days_ago = (now - event_time) // 86400
            
            if 0 <= days_ago < days:
                event_counts[days_ago] += 1
                
        except Exception as e:
            print(f"Error processing event: {type(event)} {str(e)}")
            if isinstance(event, dict):
                print("Event sample:", {k: event[k] for k in list(event.keys())[:3]})
            else:
                print("Event is:", str(event)[:100])
    
    print("Processed events counts:", event_counts)
    return event_counts

def update_leds(event_counts):
    max_count = max(event_counts) if max(event_counts) > 0 else 1
    print(f"Updating LEDs with counts: {event_counts} (max: {max_count})")
    
    for day in range(5):
        count = event_counts[day]
        if count > 0:
            print('Turning green. Day:', day, 'Count:', count)
            # Scale brightness: min=15, max=50 based on event count
            brightness = 15 + int(35 * (count / max_count))
            set_led(day, 'green', brightness)
            utime.sleep(0.1)
        else:
            print('Turning red. Day:', day, 'Count:', count)
            set_led(day, 'red', 25)
            utime.sleep(0.1)