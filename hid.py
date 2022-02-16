from adafruit_hid.consumer_control import ConsumerControl
from adafruit_hid.keyboard import Keyboard
import usb_hid


class Key:
    _device: Keyboard | ConsumerControl

    def __init__(self, *keys: str):
        self._keys = keys

    def press(self):
        self._device.press(*self._keys)

    def send(self):
        self._device.send(*self._keys)

    def release(self):
        self._device.release(*self._keys)


class KbKeys(Key):
    _device = Keyboard(usb_hid.devices)


class CcKey(Key):
    _device = ConsumerControl(usb_hid.devices)

    def __init__(self, keys: str):
        super().__init__(keys)

    def release(self):
        self._device.release()
