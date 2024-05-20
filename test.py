import lightsensor
import led
import color
import motor
import linefollower
import gyro
import servo
import button
import time
import grappler
import reset
import i2c
import tof
import calib
import escape_room


def measure_rate():
    start = time.ticks_ms()
    for _ in range(1000):
        lightsensor.measure_green_red()
        lightsensor.measure_white()
        color.get()
    end = time.ticks_ms()
    print(end - start)


def run():
    reset.reset_hardware()
    calib.load_from_file()
    calib.show()
    # lightsensor ##############################
    # lightsensor.test_reflective()
    # lightsensor.test_outer_diff()
    # lightsensor.test_linefollower_diffs_all()
    # lightsensor.test_all()
    # lightsensor.test_white()
    # lightsensor.test_red_green()
    # lightsensor.test_red_green_calib()
    # lightsensor.test_all_calib()
    # lightsensor.test_green_red_diff()
    # lightsensor.test_linefollower_diff()

    # color ####################################
    # color.test()

    # led ######################################
    # led.test_status()
    # led.set_status_left(led.OFF)
    # led.set_status_right(led.OFF)

    # linefollower #############################
    # linefollower.linefollower()
    # linefollower.test_turn_direction()
    # linefollower.test_crossroad()
    # linefollower.test_turn_angle()
    # linefollower.drive_around_object(linefollower.LEFT)
    # linefollower.test_watch_hover()
    # linefollower.test_drive_forward_gyro()

    # gyro #####################################
    # gyro.test()

    # motor ####################################
    # motor.test()
    # motor.test_forward()

    # servo ####################################
    # servo.test(servo.FOUR)
    # servo.test_all()
    # servo.test180()

    # button ###################################
    # button.test()

    # speed ####################################
    # measure_rate()

    # grappler
    # grappler.down()

    # i2c ######################################
    # i2c.test()

    # tof ######################################
    # tof.test(tof.FOUR)

    # escape ###################################
    # escape_room.wall_follower()
    escape_room.find_line(2)
    pass


# TODO gyro calibrierung an use case anpassen
# motoren drehen mit


if __name__ == "__main__":
    run()
