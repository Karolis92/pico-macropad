from digitalio import DigitalInOut, Direction, Pull
import board
import storage
import usb_cdc


def main():
    firstRow = DigitalInOut(board.GP18)
    firstRow.direction = Direction.INPUT
    firstRow.pull = Pull.DOWN

    firstColumn = DigitalInOut(board.GP19)
    firstColumn.direction = Direction.OUTPUT
    firstColumn.value = True

    if not firstRow.value:
        storage.disable_usb_drive()
        usb_cdc.disable()

    firstRow.deinit()
    firstColumn.deinit()


if __name__ == "__main__":
    main()
