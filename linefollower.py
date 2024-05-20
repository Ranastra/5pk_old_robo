import motor
import utime
import lightsensor
import color
import led
import gyro
import button
import sensor

# this module will host helper functions for the linefollower
# combining sensors, motor and decision making

###### directions ######
DIRECTION = int
FORWARD:  DIRECTION = 0
LEFT:     DIRECTION = 1
RIGHT:    DIRECTION = -1
BACKWARD: DIRECTION = 3

# map direction constants to names
direction_map = {FORWARD: "forward", LEFT: "left",
                 RIGHT: "right", BACKWARD: "backward"}

V0: int = 50

# flags
CHECK_FOR_HOVER: bool = True


def decide_crossroad(values: list[list[lightsensor.COLOR]]) -> DIRECTION:
    """ decide direction at crossroad """  # TODO
    (left, right, first, second) = (0, 1, 0, 1)
    if values[left][first] == lightsensor.GREEN and values[right][first] == lightsensor.GREEN:
        if values[left][second] == lightsensor.BLACK and values[right][second] == lightsensor.BLACK:
            return BACKWARD
        else:
            return FORWARD
    elif values[left][first] == lightsensor.GREEN:
        if values[left][second] == lightsensor.WHITE:
            return FORWARD
        else:
            return LEFT
    else:
        if values[right][second] == lightsensor.WHITE:
            return FORWARD
        else:
            return RIGHT


def watch_hover():
    """check if the robot is hovered in the air"""
    if CHECK_FOR_HOVER and lightsensor.is_hovered():
        motor.stop(motor.MOT_AB)
        while lightsensor.is_hovered():
            lightsensor.measure_white()


def until_green_end(direction: DIRECTION) -> list[int]:
    """
    dont change driving until the other side sees green,
    than returns the current colors
    """
    while True:
        lightsensor.measure_green_red()
        values = color.get()
        if (
                (direction == LEFT and values[0] != lightsensor.GREEN) or
                (direction == RIGHT and values[1] != lightsensor.GREEN)
        ):
            # print(values)
            # utime.sleep_ms(50)
            # values = color.get()
            return values


def drive_off_green(direction: DIRECTION) -> list[list[lightsensor.COLOR]]:
    """
    gets called after one sensor sees green, drive until green ends on this side
    measure, on the other side, and store which color comes after green
    return the colors as [left[first, second], right[first, second]]
    """
    motor.drive(motor.MOT_AB, V0)
    values = [
        [lightsensor.WHITE, lightsensor.WHITE],
        [lightsensor.WHITE, lightsensor.WHITE]
    ]
    (left, right) = (0, 1)
    if direction == LEFT:
        values[left][0] = lightsensor.GREEN
    else:
        values[right][0] = lightsensor.GREEN
    motor.drive(motor.MOT_AB, V0)
    while True:
        lightsensor.measure_green_red()
        (color_left, color_right) = color.get()
        if direction == LEFT:
            if color_right == lightsensor.GREEN:
                values[right][0] = color_right
            if color_left != lightsensor.GREEN:
                utime.sleep_ms(100)
                (color_left, color_right) = color.get()
                values[left][1] = color_left
                values[right][1] = until_green_end(RIGHT)[right]
                break
        else:
            if color_left == lightsensor.GREEN:
                values[left][0] = color_left
            if color_right != lightsensor.GREEN:
                utime.sleep_ms(100)
                (color_left, color_right) = color.get()
                values[right][1] = color_right
                values[left][1] = until_green_end(LEFT)[left]
                break
    motor.stop(motor.MOT_AB)
    return values


def drive_angle(angle: float):
    """drive angle with gyro"""
    V0 = 100
    gyro.reset()
    if angle > 0:
        motor.drive(motor.MOT_A, V0)
        motor.drive(motor.MOT_B, -V0)
        while gyro.angle[2] < angle:
            gyro.update()
    else:
        motor.drive(motor.MOT_B, V0)
        motor.drive(motor.MOT_A, -V0)
        while gyro.angle[2] > angle:
            gyro.update()
    motor.stop(motor.MOT_AB)


def turn_direction(direction: DIRECTION):
    """turn direction at crossroad with some corrections"""
    # TODO verschiedene Geschwindikeiten oder stottern
    V0 = 70
    # try correcting with gyro # TODO
    # drive_angle(-gyro.angle[2])  # this will prob break everything
    # drive a bit forward
    if direction != BACKWARD:
        motor.drive(motor.MOT_AB, V0)
        utime.sleep_ms(50)
    gyro.reset()
    if direction == LEFT:
        drive_angle(-70.0)
    elif direction == RIGHT:
        drive_angle(70.0)
    elif direction == BACKWARD:
        drive_angle(180.0)
    motor.drive(motor.MOT_AB, V0)
    utime.sleep_ms(100)
    motor.stop(motor.MOT_AB)


def run():
    linefollower()


def linefollower():
    """linefollower"""

    faktor = 3
    V0 = 50 # Basisgeschwindigkeit
    V0_BASIC = 25 # Reduzierte Geschwindigkeit für einfachen Linienfolger

    basic_time_end = utime.ticks_ms()
    basic_flag = False
    v = V0
    
    while True:
        # Werte messen
        lightsensor.measure_white()
        diff = lightsensor.get_linefollower_diff_calib()
        diff_outer = lightsensor.get_linefollower_diff_outside()

        # bei großer Abweichung der äußeren Sensorwerte
        # nur noch mit den äußeren Sensoren ausgleichen
        if abs(diff_outer) > 70:
            if diff_outer < 0:
                vr = v - diff_outer
                vl = v + diff_outer * faktor
            else:
                vl = v + diff_outer
                vr = v - diff_outer * faktor

        # ansonsten mit den inneren Sensoren ausgleichen
        else:
            vr = v - diff * faktor
            vl = v + diff * faktor

        motor.drive(motor.MOT_A, vl)
        motor.drive(motor.MOT_B, vr)

        # andere Sensoren auswerten
        if not basic_flag:

            for _ in range(5):
                # grün und rot Werte messen
                lightsensor.measure_green_red()
                # die Zähler aktualisieren
                color_l, color_r = color.get()

            # Silber Werte messen
            lightsensor.measure_reflective()

            # Grün
            if color_l == lightsensor.GREEN or color_r == lightsensor.GREEN:
                # Grün erkannt, weiterfahren und messen
                if color_l == lightsensor.GREEN:
                    vals = drive_off_green(LEFT) 
                else:
                    vals = drive_off_green(RIGHT)

                # Farben auswerten
                direction = decide_crossroad(vals) 
                utime.sleep_ms(1000)

                # Abbiegen
                turn_direction(direction)
                # langsam weiterfahren
                basic_time_end, basic_flag = utime.ticks_ms() + 700, True
                v = V0_BASIC

            # rot
            elif color_l == lightsensor.RED or color_r == lightsensor.RED:
                # 10 sec warten
                motor.stop(motor.MOT_AB)
                utime.sleep_ms(10_000)
                # Zähler zurücksetzen und langsamer weiterfahren
                color.reset()
                basic_time_end, basic_flag = utime.ticks_ms() + 700, True
                v = V0_BASIC

            # silber: Eingang escape room 
            elif lightsensor.on_silver():
                motor.stop(motor.MOT_AB)
                led.set_status_locked(2, led.WHITE)
                utime.sleep_ms(1000)
                # zurück zu main
                return

            # Kollision
            elif not button.left.value() or not button.right.value():
                # Hinderniss umfahren
                drive_around_object(LEFT)   
                # langsamer weiterfahren
                basic_time_end, basic_flag = utime.ticks_ms() + 600, True
                v = V0_BASIC
        else:
            # auf Ende des einfachen Linefollowers testen
            basic_flag = utime.ticks_ms() < basic_time_end
            if not basic_flag:
                v = V0


def drive_around_object(direction: DIRECTION):
    """drive around an object after collision"""
    V0 = 85
    motor.drive(motor.MOT_AB, -60)
    led.set_status_locked(2, led.CYAN)
    utime.sleep_ms(200)
    vdiff = 65
    drive_angle(-70.0*direction)
    motor.drive(motor.MOT_AB, V0)
    utime.sleep_ms(100)
    motor.drive(motor.MOT_A, V0 + vdiff*direction)
    motor.drive(motor.MOT_B, V0 - vdiff*direction)
    lightsensor.measure_white()
    start = utime.ticks_ms()
    while True:
        if not lightsensor.all_white() and utime.ticks_ms() - start > 500:
            break
        lightsensor.measure_white()
    motor.drive(motor.MOT_AB, V0)
    utime.sleep_ms(250)
    drive_angle(-70.0*direction)


def test_crossroad():
    """test for green detection at crossroads, prints the colors"""
    motor.drive(motor.MOT_AB, V0)
    while True:
        lightsensor.measure_white()
        lightsensor.measure_green_red()
        diff = lightsensor.get_linefollower_diff_calib()
        motor.drive(motor.MOT_A, V0 + diff)
        motor.drive(motor.MOT_B, V0 - diff)
        colors = color.get()
        if colors[0] == lightsensor.GREEN:
            print("left")
            print([[[lightsensor.color_map[val] for val in direc]
                  for direc in drive_off_green(LEFT)]])
            break
        elif colors[1] == lightsensor.GREEN:
            print("right")
            # print(drive_off_green(RIGHT))
            print([[[lightsensor.color_map[val] for val in direc]
                  for direc in drive_off_green(RIGHT)]])
            break


def test_turn_direction():
    """unit test for turn_direction"""
    gyro.calib()
    for _ in range(2):
        print("left")
        turn_direction(LEFT)
        utime.sleep(1)
        print("right")
        turn_direction(RIGHT)
        utime.sleep(1)
        print("forward")
        turn_direction(FORWARD)
        utime.sleep(1)
        print("backward")
        turn_direction(BACKWARD)
        utime.sleep(1)


def test_watch_hover():
    while True:
        print("watching")
        lightsensor.measure_white()
        for sens in sensor.white:
            print(sens.map_raw_value(), end=" ")
        print()
        watch_hover()
        print("end")
        utime.sleep_ms(300)


def test_turn_angle():
    """unit test for turn_direction"""
    gyro.calib()
    while True:
        print("left")
        drive_angle(-90.0)
        utime.sleep(1)
        print("right")
        drive_angle(90.0)
        utime.sleep(1)


def test_drive_forward_gyro():
    """drive forward with gyro"""
    gyro.calib()
    gyro.reset()
    while True:
        gyro.update()
        print(gyro.angle[0])


if __name__ == "__main__":
    run()
