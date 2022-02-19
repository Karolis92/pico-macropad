import time
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.keyboard import Keyboard
import usb_hid


class Key:
    _device = Keyboard(usb_hid.devices)

    def __init__(self, *keys: str):
        self.keys = keys

    def send(self):
        self._device.send(*self.keys)

    def pressed(self):
        self._device.press(*self.keys)

    def released(self):
        self._device.release(*self.keys)


class ConsumerCtrl(Key):
    _device = ConsumerControl(usb_hid.devices)

    def __init__(self, key: str):
        super().__init__(key)

    def released(self):
        self._device.release()


class Multifunctional:
    long_press_duration = 0.5

    def __init__(self, short: Key, long: Key = None):
        self.tap = short
        self.long = long

    def pressed(self):
        self._pressed = time.monotonic()

    def released(self):
        released = time.monotonic()
        if (self.long and self.long_press_duration < released - self._pressed):
            self.long.send()
        else:
            self.tap.send()
