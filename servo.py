import pinesp32
import time
import machine

# min/max pulse witdh / pwm pulse width * duty cycle max
_MIN_DUTY_CYCLE = 0.5/20.0 * 2**16
_MAX_DUTY_CYCLE = 2.1/20.0 * 2**16

SERVO = machine.PWM

ONE: SERVO = machine.PWM(
    machine.Pin(pinesp32.SERVO1, mode=machine.Pin.OUT),
    freq=50
)
TWO: SERVO = machine.PWM(
    machine.Pin(pinesp32.SERVO2, mode=machine.Pin.OUT),
    freq=50
)
THREE: SERVO = machine.PWM(
    machine.Pin(pinesp32.SERVO3, mode=machine.Pin.OUT),
    freq=50
)
FOUR: SERVO = machine.PWM(
    machine.Pin(pinesp32.SERVO4, mode=machine.Pin.OUT),
    freq=50
)


def set_angle(servo: SERVO, angle: int, wait_time_ms: int = 500):
    """set angle of the servo -90 to +90 and wait for wait_time_ms"""
    angle += 90
    angle = max(0, min(angle, 180))
    duty_cycle = _MIN_DUTY_CYCLE + \
        (angle/180.0) * (_MAX_DUTY_CYCLE - _MIN_DUTY_CYCLE)
    servo.duty_u16(int(duty_cycle))
    time.sleep_ms(wait_time_ms)


def off(servo: SERVO):
    """turn off the servo"""
    servo.duty_u16(0)


def test_one(servo: SERVO):
    """set angle for servo -90 to +90 in steps of 30 degrees"""
    for angle in range(-90, 91, 30):
        set_angle(servo, angle)
        time.sleep_ms(1000)


def test_all():
    """all servos -90 to +90 in steps of 30 degrees"""
    while True:
        for angle in range(-90, 91, 30):
            set_angle(ONE, angle)
            set_angle(TWO, angle)
            set_angle(THREE, angle)
            set_angle(FOUR, angle)
            time.sleep_ms(1000)


def test180():
    """all servos from -90 to +90 degrees"""
    while True:
        for angle in [-90, 90]:
            print(angle)
            set_angle(ONE, angle)
            set_angle(TWO, angle)
            set_angle(THREE, angle)
            set_angle(FOUR, angle)
            time.sleep_ms(3000)

# mapping for max_pulse_width = 2.4ms linear?
# 0 -> 0
# 30 -> 40
# 60 -> 85
# 90 -> 130
# 120 -> 150
# 150 -> 180
# 160 -> 190
