import board
import keypad
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keycode import Keycode

from pico_macropad.encoder import Encoder
from pico_macropad.hid import CcKey, KbKeys, KbKeys as Key


def main():
    # create keys to send commands to the computer
    keys: list[Key] = [
        # row 1
        CcKey(ConsumerControlCode.SCAN_PREVIOUS_TRACK),
        CcKey(ConsumerControlCode.SCAN_NEXT_TRACK),
        CcKey(ConsumerControlCode.PLAY_PAUSE),
        None,  # no key here
        # row 2
        KbKeys(Keycode.F17),
        KbKeys(Keycode.CONTROL, Keycode.ALT, Keycode.A),
        KbKeys(Keycode.F19),
        KbKeys(Keycode.F20),
        # row 3
        KbKeys(Keycode.F21),
        KbKeys(Keycode.F22),
        KbKeys(Keycode.F23),
        KbKeys(Keycode.F24),
    ]
    encoder_cw_key = CcKey(ConsumerControlCode.VOLUME_INCREMENT)
    encoder_ccw_key = CcKey(ConsumerControlCode.VOLUME_DECREMENT)
    encoder_btn_key = CcKey(ConsumerControlCode.MUTE)

    # create KeyMatrix to read key presses
    matrix = keypad.KeyMatrix(
        row_pins=(board.GP18, board.GP17, board.GP16), column_pins=(
            board.GP19, board.GP20, board.GP21, board.GP22)
    )

    # create Encoder to read values
    encoder = Encoder(board.GP10, board.GP11, board.GP12, 2)

    while True:
        event = matrix.events.get()
        if event:
            key = keys[event.key_number]
            if event.pressed:
                key.press()
            else:
                key.release()

        event = encoder.getButtonEvent()
        if event:
            if event.pressed:
                encoder_btn_key.press()
            else:
                encoder_btn_key.release()

        event = encoder.getPositionEvent()
        if event:
            key = encoder_cw_key if event.difference > 0 else encoder_ccw_key
            for x in range(abs(event.difference)):
                key.send()


if __name__ == "__main__":
    main()
