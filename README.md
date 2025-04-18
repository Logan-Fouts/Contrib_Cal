# Contrib Cal - A Physical GitHub Contribution Tracker

![Contrib Cal in Action](/Images/Cal_Animation.gif)  
*Your GitHub streak, glowing IRL.*

A hackable desk calendar that visualizes your GitHub contributions using NeoPixels and a Raspberry Pi Pico W. Open-source hardware + software.

## 🌟 Features
- **Real GitHub Sync**: Updates via GitHub API
- **Guilt Mode**: Glows red when you miss commits
- **100% Hackable**: Customize animations in MicroPython
- **Beginner-Friendly**: Program with **Thonny IDE** (no toolchains needed)
- **DIY Build**: 3D-printable case & hand-solderable LED matrix

## 🛠️ Quick Start with Thonny
### Programming the Pico W:
1. **Install [Thonny](https://thonny.org/)** (Python IDE for beginners)
2. Connect your Pico W via USB
3. In Thonny:
   - Select interpreter: **MicroPython (Raspberry Pi Pico)**
   - Open `/src/main.py` and click **Run**
4. **Save to Pico** (Ctrl+S → "Raspberry Pi Pico"):
   - Save `main.py` and `config.json` to the Pico's storage

![Thonny Setup](/Images/thonny-screenshot.png)

## 📦 What's Included
| Directory       | Contents                                  |
|-----------------|-------------------------------------------|
| `/src`          | Micropython firmware & configuration      |
| `/blender`      | 3D-printable case (Blender files)         |
| `/freecad`      | Alternative enclosure designs (FreeCAD)   |
| `/schematics`   | Wiring diagrams & PCB templates           |

## 🔧 Build Guide
### You'll Need:
- Raspberry Pi Pico W ($6)
- 28x WS2812B NeoPixels (~$10)
- 3D-printed case
- Micro-USB cable
![Contrib Cal](/Images/Render%20Front%20Face%20Screen.PNG)
![Contrib Cal Face with Screen](/Images/Render.PNG)

### Assembly:
1. **Print the Case**: Use files from `/blender` or `/freecad`
2. **Solder the Matrix**
3. **Program with Thonny** (see above)
4. **Configure** `config.json`:
```python
{
  "github_user": "YOUR_USERNAME",
  "wifi_creds": ["SSID", "PASSWORD"],  # Optional for live sync
  "colors": {
    "event_color": "#00ff00",  # Green for active days
    "none_color": "#ff0000"    # Red for no commits
  }
}
