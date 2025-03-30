import gc
from wifi_utils import connect_wifi, fetch_github_events, update_leds, get_event_counts
from led_utils import turn_all_off, startup_animation


def main():
    startup_animation()
    wlan = connect_wifi()
    
    # Fetch all event types (up to 100)
    events = fetch_github_events(max_events=100)
    print(f"Total events fetched: {len(events)}")
    
    # Count events per day
    event_counts = get_event_counts(events)
    print("Final event counts:", event_counts)
    
    # Update LEDs with brightness scaling
    update_leds(event_counts)
    
    # Clean up
    del events
    gc.collect()

if __name__ == "__main__":
    main()