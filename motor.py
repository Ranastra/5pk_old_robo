import math
import shift_register
import pinesp32
import machine
import time

print("motor got started")

MOT = int
MOT_A:  MOT = 1
MOT_B:  MOT = 2
MOT_AB: MOT = 3

_PWMA: machine.PWM = machine.PWM(machine.Pin(pinesp32.PWMA))
_PWMB: machine.PWM = machine.PWM(machine.Pin(pinesp32.PWMB))


def drive(mot: MOT, speed: int):
    """drive MOT with speed 0-100"""
    direction = speed < 0
    speed = int(min(math.fabs(speed), 100))
    shift_register.set(pinesp32.SR_STBY, True)
    if mot & MOT_A:  # IN1 and IN2 are switched or inverted?
        shift_register.set(pinesp32.SR_AIN1, direction)
        shift_register.set(pinesp32.SR_AIN2, not direction)
        _PWMA.duty_u16(speed * 655)  # 100*655 ~ 16bit
    if mot & MOT_B:
        shift_register.set(pinesp32.SR_BIN1, direction)
        shift_register.set(pinesp32.SR_BIN2, not direction)
        _PWMB.duty_u16(speed * 655)  # achtung schrott TODO
    shift_register.write()


def stop(mot: MOT):
    """stop given MOT"""
    if mot == MOT_AB:
        shift_register.set(pinesp32.SR_STBY, False)
    if mot & MOT_A:
        _PWMA.duty_u16(0)
    if mot & MOT_B:
        _PWMB.duty_u16(0)


def test():
    """drive forward and backward 5 times"""
    time.sleep(2)
    # for _ in range(5):
    while True:
        drive(MOT_AB, 80)
        time.sleep(4)
        drive(MOT_AB, -80)
        time.sleep(4)
    stop(MOT_AB)


def test_forward():
    """drive forward with max speed"""
    drive(MOT_AB, 100)
    while True:
        pass
