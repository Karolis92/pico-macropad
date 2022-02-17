# Raspberry Pi Pico Macropad

This repository contains CircuitPython code for macropad
## Usage

In your CIRCUITPY drive:
* Add these dependencies to the `lib` folder:
  * `adafruit_hid` from [CircuitPython bundle](https://circuitpython.org/libraries).
* Copy `pico_macropad` to the root of the drive.
* Create `main.py` and write your code there. Example can be found in this repo.  
* Optionally create `boot.py`. Example that disables usb drive and serial communication if first button in first row is not pressed on boot can be found in this repo. Be careful as that can potentially lock you out from accessing your microcontroller if pins are not configured correctly.

## Photos

![macropad](/img/macropad.JPG)
![macropad internals](/img/internals.JPG)

