from digitalio import DigitalInOut, Direction, Pull
from rotaryio import IncrementalEncoder
from microcontroller import Pin


class EncoderBtnEvent:
    def __init__(self, pressed: int):
        self.pressed = pressed


class EncoderPostionEvent:
    def __init__(self, difference: int):
        self.difference = difference


class Encoder:
    def __init__(self, pin_a: Pin, pin_b: Pin, pin_btn: Pin, divisor: int):
        self._enc = IncrementalEncoder(pin_a, pin_b, divisor)

        self._btn = DigitalInOut(pin_btn)
        self._btn.direction = Direction.INPUT
        self._btn.pull = Pull.UP

        self.last_btn_val = self._btn.value
        self.last_position = self.position

    @property
    def position(self):
        return self._enc.position

    def getButtonEvent(self):
        if self._btn.value != self.last_btn_val:
            self.last_btn_val = self._btn.value
            return EncoderBtnEvent(not self.last_btn_val)
        return None

    def getPositionEvent(self):
        diff = self.position - self.last_position
        if diff != 0:
            self.last_position = self.position
            return EncoderPostionEvent(diff)
        return None
