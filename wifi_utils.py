import network
import socket
import machine
import ntptime
import utime
from config_manager import CONFIG_MANAGER

class WIFI_UTILS:
    def __init__(self):
        self.AP_SSID = "Contrib Calendar"
        self.AP_PASSWORD = "setup123"
        self.config_manager = CONFIG_MANAGER()
        self.wlan = self.connect_wifi()

    def connect_wifi(self):
        config = self.config_manager.load_config()
        wlan = network.WLAN(network.STA_IF)
        wlan.active(True)
        wlan.connect(config['WIFI_SSID'], config['WIFI_PASSWORD'])
        
        if not wlan.isconnected():
            if "WIFI_SSID" in config and "WIFI_PASSWORD" in config:
                print(f"Connecting to {config['WIFI_SSID']}...")
                wlan.connect(config['WIFI_SSID'], config['WIFI_PASSWORD'])
                
                for _ in range(20):  # 10-second timeout
                    if wlan.isconnected():
                        break
                    utime.sleep(0.5)
            
            if not wlan.isconnected():
                print("Wi-Fi failed. Starting config portal...")
                start_config_portal()
        
        print("Connected! IP:", wlan.ifconfig()[0])
        
        self.test_dns()
        self.test_internet()
        self.sync_time()
        
        return wlan

    def start_config_portal(self):
        ap = network.WLAN(network.AP_IF)
        ap.active(True)
        ap.config(essid=self.AP_SSID, password=self.AP_PASSWORD)
        print(f"AP mode active. Connect to '{AP_SSID}' and visit http://192.168.4.1")

        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        s.bind(('', 80))
        s.listen(1)
        
        while True:
            conn = None
            try:
                conn, addr = s.accept()
                print('Connection from', addr)
                
                # Receive full request
                request = b''
                while True:
                    chunk = conn.recv(256)
                    if not chunk:
                        break
                    request += chunk
                    if b'\r\n\r\n' in request:  # End of headers
                        break
                
                request = request.decode('utf-8')
                
                if "POST /" in request:
                    # Extract content length
                    content_length = 0
                    for line in request.split('\r\n'):
                        if line.startswith('Content-Length:'):
                            content_length = int(line.split(':')[1].strip())
                            break
                    
                    # Read remaining body if needed
                    body_start = request.find('\r\n\r\n') + 4
                    body = request[body_start:]
                    while len(body) < content_length:
                        body += conn.recv(256).decode('utf-8')
                    
                    # Parse form data
                    config = {}
                    try:
                        for pair in body.split('&'):
                            if '=' in pair:
                                key, value = pair.split('=', 1)
                                config[key] = unquote(value).replace('+', ' ')
                        
                        # Validate required fields
                        required = ['WIFI_SSID', 'WIFI_PASSWORD', 'GITHUB_USERNAME', 'GITHUB_TOKEN']
                        if all(field in config for field in required):
                            save_config(config)
                            response = """HTTP/1.1 200 OK
    Content-Type: text/html
    Connection: close

    <html>
    <body>
    <h1>Settings Saved!</h1>
    <p>Device will reboot shortly...</p>
    </body>
    </html>"""
                            conn.send(response.replace('\n', '\r\n'))
                            conn.close()
                            utime.sleep(3)
                            machine.reset()
                        else:
                            raise ValueError("Missing required fields")
                            
                    except Exception as e:
                        error_response = """HTTP/1.1 400 Bad Request
    Content-Type: text/html
    Connection: close

    <html>
    <body>
    <h1>Error</h1>
    <p>Please fill all fields.</p>
    </body>
    </html>"""
                        conn.send(error_response.replace('\n', '\r\n'))
                
                else:
                    # Serve HTML form (simplified without CSS)
                    current_config = load_config()
                    html = """HTTP/1.1 200 OK
    Content-Type: text/html
    Connection: close

    <html>
    <body>
    <h1>Pico W Configuration</h1>
    <form method="POST">
    <h2>WiFi Settings</h2>
    SSID: <input type="text" name="WIFI_SSID" value="{WIFI_SSID}" required><br>
    Password: <input type="password" name="WIFI_PASSWORD" value="{WIFI_PASSWORD}" required><br>

    <h2>GitHub Settings</h2>
    Username: <input type="text" name="GITHUB_USERNAME" value="{GITHUB_USERNAME}" required><br>
    Token: <input type="password" name="GITHUB_TOKEN" value="{GITHUB_TOKEN}" required><br>
    <small>(Create token at github.com/settings/tokens)</small><br>

    <button type="submit">Save Settings</button>
    </form>
    </body>
    </html>""".format(
                        WIFI_SSID=current_config.get('WIFI_SSID', ''),
                        WIFI_PASSWORD=current_config.get('WIFI_PASSWORD', ''),
                        GITHUB_USERNAME=current_config.get('GITHUB_USERNAME', ''),
                        GITHUB_TOKEN=current_config.get('GITHUB_TOKEN', '')
                    )
                    conn.send(html.replace('\n', '\r\n'))
                    
            except Exception as e:
                print("Server error:", e)
            finally:
                if conn:
                    conn.close()
                    
    def sync_time(self):
        try:
            # TODO: Need to allow users to define there time zone
            # Calculate UTC offset for New York
            is_dst = utime.localtime()[1] > 3 and utime.localtime()[1] < 11  # DST from April to October
            UTC_OFFSET = -4 * 3600 if is_dst else -5 * 3600
            
            ntptime.host = "time.cloudflare.com"
            ntptime.settime()
            
            current_time = utime.localtime(utime.mktime(utime.localtime()) + UTC_OFFSET)
            print("New York time synced:", current_time)
        except Exception as e:
            print("NTP sync failed:", e)
     
    def test_dns(self):
        try:
            addr = socket.getaddrinfo("google.com", 80)[0][-1]
            print("✅ DNS works! IP:", addr[0])
        except Exception as e:
            print("❌ DNS failed:", e)
            
    def test_internet(self):
        try:
            s = socket.socket()
            s.connect(("142.250.190.46", 80))
            s.close()
            print("✅ Internet works!")
        except Exception as e:
            print("❌ No internet:", e)

