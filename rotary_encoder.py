import pinesp32
import time
import machine


# Constants
_TIME_DISABLE_BUTTON_MS = 300

# Rotary Encoder Pins
_ENC_A = machine.Pin(pinesp32.ENC_A, machine.Pin.IN)
_ENC_B = machine.Pin(pinesp32.ENC_B, machine.Pin.IN)
_ENC_SW = machine.Pin(pinesp32.ENC_SW, machine.Pin.IN)

# state variables
state = 0
_last_state_a = _ENC_A.value()
_time_stamp_button = time.ticks_ms()
_button_pressed = False


def watch_button_press() -> bool:
    """return if button was pressed"""
    global _button_pressed, _time_stamp_button
    if _ENC_SW.value():
        if _button_pressed:
            if _time_stamp_button < time.ticks_ms():
                _button_pressed = False
            return False
        else:
            _button_pressed = True
            _time_stamp_button = time.ticks_ms() + _TIME_DISABLE_BUTTON_MS
            return True
    return False


def watch_rotary() -> int:
    """return direction of rotation"""
    global _last_state_a, state
    if _ENC_A.value():
        if not _last_state_a:
            _last_state_a = True
            if _ENC_B.value():
                state += 1
                return 1
            else:
                state -= 1
                return -1
        _last_state_a = True
    else:
        _last_state_a = False
    return 0


def test():
    while True:
        if watch_button_press():
            print("button pressed")
        if watch_rotary():
            print("rotary", state)
