# Contrib Cal - A Physical GitHub Contribution Tracker

![Contrib Cal in Action](/Images/Cal_Animation.gif)  
*Your GitHub streak, glowing IRL.*

A hackable desk calendar that visualizes your GitHub contributions using NeoPixels and a Raspberry Pi Pico W. Open-source hardware + software.

## 🤝 Sponsored by PCBWay

![PCBWay Logo](https://www.pcbway.com/project/img/images/frompcbway.png)

### Why PCBWay?
- **Quality**: Crystal-clear silkscreen and precise tolerances. Everything fits perfect
- **Fast**: From design to doorstep in days, took way less time than I had expected it to
- **Affordable**: Perfect for makers and small-batch projects
- **Global Shipping**: Reliable delivery worldwide, I was able to order in the US and get it delivered to Sweden since I would be there at that time

*Professional PCB manufacturing makes all the difference for clean builds*

### Want Your Own PCBs Made?
If you're building your own Contrib Cal, PCBWay offers:
- High-quality PCB fabrication
- 3D printing

**So you can build your own from scratch!**

**Get started**: Go to [PCBWay.com](https://www.pcbway.com/) and upload your Gerber files.


![PCB_LEDS](/Images/Real%20Pictures/assembled_pcb_front.jpg)

---


## Features
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

## What's Included
| Directory       | Contents                                  |
|-----------------|-------------------------------------------|
| `/src`          | Micropython firmware & configuration      |
| `/blender`      | Render 3d files   (Blender files)         |
| `/freecad`      | Enclosure designs (FreeCAD)               |
| `/kicad`        | Wiring diagrams                           |

## Build Guide
### You'll Need:
- Raspberry Pi Pico W ($6)
- 28x WS2812B NeoPixels (~$10)
- 3D-printed case
- Micro-USB cable
- Soldering tools and resources

![Contrib Cal](/Images/Render%20Front%20Face%20Screen.PNG)

### Assembly:
1. **Print the Case**: Use files from `/blender` or `/freecad`
2. **Solder the Matrix**
3. **Program with Thonny** (see above)
4. **Configure** `config.json`:
```python
{
  "WIFI_SSID": "*",
  "WIFI_PASSWORD": "*",
  "GITHUB_USERNAME": "*",
  "GITHUB_TOKEN": "*",
  "STARTUP_ANIMATION": 4
}
