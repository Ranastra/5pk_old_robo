import reset
import calib
import rotary_encoder
import time
import linefollower
import led
import escape_room
import gyro
import test
import motor

print("main.py like maintenance")


def start():
    """setup"""
    # reset hardware
    reset.reset_hardware()
    # load stored calib
    calib.load_from_file()
    # calibration of gyro
    gyro.calib()
    while not rotary_encoder.watch_button_press():
        led.set_status_locked(2, led.PURPLE)
        val = rotary_encoder.watch_rotary()
        if val == 1:
            # calibrate lightsensors
            led.set_status_locked(2, led.RED)
            time.sleep_ms(500)
            calib.start()
            calib.write_to_file()
        if val == -1:
            # run tests
            led.set_status_locked(2, led.BLUE)
            time.sleep_ms(500)
            test.run()
    led.set_status_locked(2, led.GREEN)
    time.sleep_ms(500)


def run():
    led.set_status_locked(2, led.PURPLE)
    time.sleep_ms(500)
    linefollower.run()
    led.set_status_locked(2, led.BLUE)
    time.sleep_ms(500)
    escape_room.run()
    led.set_status_locked(2, led.PURPLE)
    time.sleep_ms(500)
    linefollower.run()


def stop():
    """cleanup"""
    reset.run()


while True:
    try:
        start()
        run()
        stop()
    except:
        motor.stop(motor.MOT_AB)
        led.set_status_locked(2, led.GREEN)
        time.sleep_ms(500)
