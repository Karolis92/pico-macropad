import board
import keypad
from adafruit_hid.consumer_control_code import ConsumerControlCode
from adafruit_hid.keycode import Keycode
from pico_macropad.encoder import Encoder
from pico_macropad.hid import HidInterface, Key, Lambda, ConsumerCtrl, Multifunctional
import supervisor


def main():
    # Multifunctional.long_press_duration = 1 # change long press duration
    # create keys to send commands to the computer
    keys: list[HidInterface] = [
        # row 1
        ConsumerCtrl(ConsumerControlCode.SCAN_PREVIOUS_TRACK),
        ConsumerCtrl(ConsumerControlCode.SCAN_NEXT_TRACK),
        Multifunctional(short=ConsumerCtrl(ConsumerControlCode.PLAY_PAUSE),
                        long=Key(Keycode.CONTROL, Keycode.ALT, Keycode.S)),
        None,
        # row 2
        Multifunctional(short=Key(Keycode.CONTROL, Keycode.ALT, Keycode.F1),
                        long=Key(Keycode.CONTROL, Keycode.ALT, Keycode.F2)),
        Key(Keycode.CONTROL, Keycode.ALT, Keycode.A),
        Multifunctional(short=Key(Keycode.WINDOWS, Keycode.SHIFT, Keycode.A),  # PowerToys - mute microphone
                        long=Key(Keycode.WINDOWS, Keycode.SHIFT, Keycode.O)),  # PowerToys - turn off cam
        Key(Keycode.WINDOWS, Keycode.E),
        # row 3
        Key(Keycode.CONTROL, Keycode.ALT, Keycode.V),
        Key(Keycode.CONTROL, Keycode.ALT, Keycode.T),
        Multifunctional(short=Key(Keycode.F12),
                        long=Lambda(lambda: supervisor.reload())),
        Multifunctional(short=Key(Keycode.WINDOWS, Keycode.D),
                        long=Key(Keycode.WINDOWS, Keycode.CONTROL, Keycode.T)),  # PowerToys - pin window
    ]
    encoder_cw_key = ConsumerCtrl(ConsumerControlCode.VOLUME_INCREMENT)
    encoder_ccw_key = ConsumerCtrl(ConsumerControlCode.VOLUME_DECREMENT)
    encoder_btn_key = ConsumerCtrl(ConsumerControlCode.MUTE)

    # create KeyMatrix to read key presses
    matrix = keypad.KeyMatrix(
        row_pins=(board.GP18, board.GP17, board.GP16),
        column_pins=(board.GP19, board.GP20, board.GP21, board.GP22)
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
