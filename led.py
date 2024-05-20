import shift_register
import pinesp32
import time

# rgb leds: combining red, green and blue gives new colors (addition rules)
# turn led on by setting it to low


###### status leds ######
COLOR = list  # [bool]  # tuple[bool, bool, bool]

RED:    COLOR = (False, True,  True)
BLUE:   COLOR = (True,  True,  False)
GREEN:  COLOR = (True,  False, True)
WHITE:  COLOR = (False, False, False)
OFF:    COLOR = (True,  True,  True)
PURPLE: COLOR = (False, True,  False)
YELLOW: COLOR = (False, False, True)
CYAN:   COLOR = (True,  False, False)

# hardware lock variables to prevent from setting colors multiple times,
# wasting time: need some microbenchmarking here for multiple use cases
# to see if this is of any benefit # TODO
# decided to just write wrappers around the normal functions

_status_left = OFF
_status_right = OFF


def set_status_left(color: COLOR):
    """set color of left status LED"""
    shift_register.set(pinesp32.SR_LED_L_RED, color[0])
    shift_register.set(pinesp32.SR_LED_L_GREEN, color[1])
    shift_register.set(pinesp32.SR_LED_L_BLUE, color[2])
    shift_register.write()


def set_status_right(color: COLOR):
    """set color of right status LED"""
    shift_register.set(pinesp32.SR_LED_R_RED, color[0])
    shift_register.set(pinesp32.SR_LED_R_GREEN, color[1])
    shift_register.set(pinesp32.SR_LED_R_BLUE, color[2])
    shift_register.write()


def set_status_locked(direction: int, color: COLOR):
    """set color of status LED and check if color is already set"""
    if direction % 2 == 0:
        global _status_left
        if _status_left != color:
            set_status_left(color)
            _status_left = color
    if direction >= 1:
        global _status_right
        if _status_right != color:
            set_status_right(color)
            _status_right = color


###### lightsensorbar leds ######


def set_lightsensorbar_rgb(color: COLOR):
    """set color of status LED on lightsensorbar"""
    shift_register.set(pinesp32.SR_PT_RED, not color[0])
    shift_register.set(pinesp32.SR_PT_GREEN, not color[1])
    shift_register.set(pinesp32.SR_PT_BLUE, not color[2])
    shift_register.write()


def set_lightsensorbar_white(state: bool):
    """toggle white LEDs on lightsensorbar"""
    shift_register.set(pinesp32.SR_PT_WHITE, state)
    shift_register.write()


###### tests ######

def test_status():
    """cycle through all colors for the status LEDs"""
    colors = [RED, BLUE, GREEN, WHITE, OFF, PURPLE, YELLOW, CYAN]
    for _ in range(2):
        for color in colors:
            set_status_left(color)
            set_status_right(color)
            time.sleep_ms(500)
