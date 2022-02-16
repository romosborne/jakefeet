import time
import board
from digitalio import DigitalInOut, Direction, Pull
import usb_hid
from adafruit_hid.keyboard import Keyboard
from adafruit_hid.mouse import Mouse
from adafruit_hid.keycode import Keycode

KEYBOARD = 1
MOUSE    = 2

LEFT_PEDAL   = board.GP18
MIDDLE_PEDAL = board.GP9
RIGHT_PEDAL  = board.GP13

kbd = Keyboard(usb_hid.devices)
mouse = Mouse(usb_hid.devices)

class Keymap:
    def __init__(self, pin, onPress = lambda : True, onRelease = lambda : True):
        self.state = 0
        self.pin = DigitalInOut(pin)
        self.onPress = onPress
        self.onRelease = onRelease
        
        self.pin.direction = Direction.INPUT
        self.pin.pull = Pull.UP

    def scan(self):
        # If key wasn't preesed but now is pressed
        if self.state == 0 and not self.pin.value:
            self.onPress()
            self.state = 1

        # If key was pressed and has just been released
        if self.state == 1 and self.pin.value:
            self.onRelease()
            self.state = 0

keys = [
    Keymap(
        LEFT_PEDAL,
        onPress = lambda : mouse.move(0, 0, 1)
    ),
    Keymap(
        MIDDLE_PEDAL,
        onPress   = lambda : mouse.press(Mouse.LEFT_BUTTON),
        onRelease = lambda : mouse.release(Mouse.LEFT_BUTTON)
        #onPress   = lambda : kbd.press(Keycode.B),
        #onRelease = lambda : kbd.release(Keycode.B)
    ),
    Keymap(
        RIGHT_PEDAL,
        onPress = lambda : mouse.move(0, 0, -3)
    )
]

# Turn on the LED
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = True

print("--- JakeyFootBoard ---")



# Loop
while True:
    for key in keys:
        key.scan()
    
    time.sleep(0.01)