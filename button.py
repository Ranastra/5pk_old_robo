import pinesp32
import time
import machine

# middle = machine.Pin(pinesp32.T_M, machine.Pin.IN, machine.Pin.PULL_DOWN)
left = machine.Pin(pinesp32.T_L, machine.Pin.IN,
                   machine.Pin.PULL_UP)  # is inverted
right = machine.Pin(pinesp32.T_R, machine.Pin.IN)


def test():
    while True:
        time.sleep_ms(200)
        print("left", left.value())
        print("right", right.value())
