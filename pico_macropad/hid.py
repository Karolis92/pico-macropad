import time
from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.keyboard import Keyboard
import usb_hid


class HidInterface():
    def send(self):
        pass

    def press(self):
        pass

    def release(self):
        pass


class Key(HidInterface):
    _device = Keyboard(usb_hid.devices)

    def __init__(self, *keys: str):
        self.keys = keys

    def send(self):
        self._device.send(*self.keys)

    def press(self):
        self._device.press(*self.keys)

    def release(self):
        self._device.release(*self.keys)


class ConsumerCtrl(Key):
    _device = ConsumerControl(usb_hid.devices)

    def __init__(self, key: str):
        super().__init__(key)

    def release(self):
        self._device.release()


class Lambda(HidInterface):
    def __init__(self, callable):
        self.callable = callable

    def press(self):
        pass

    def release(self):
        self.send()

    def send(self):
        self.callable()


class Multifunctional(HidInterface):
    long_press_duration = 0.5

    def __init__(self, short: HidInterface, long: HidInterface = None):
        self.tap = short
        self.long = long

    def press(self):
        self._pressed = time.monotonic()

    def release(self):
        released = time.monotonic()
        if (self.long and self.long_press_duration < released - self._pressed):
            self.long.send()
        else:
            self.tap.send()

    def send(self):
        raise Exception("Not implemented")
