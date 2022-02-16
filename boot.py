from digitalio import DigitalInOut, Direction, Pull
import storage
import board

print("Booting...")

middle_pedal = DigitalInOut(board.GP9)
middle_pedal.direction = Direction.INPUT
middle_pedal.pull = Pull.UP

if middle_pedal.value:
    print("Middle pedal not pressed - Booting normally")
    storage.disable_usb_drive()
else:
    print("Middle pedal pressed - programming mode!")