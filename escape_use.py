import motor
import led
import utime
import gyro
import tof
import lightsensor
import button
import grappler
import color
import escape_room

# tof.ONE = upper
# tof.THREE = lower

BALL_ALIVE = 1
BALL_DEAD = 2

def sign(x: float):
    if x > 0:
        return 1
    elif x < 0:
        return -1
    else:
        return 0

def is_outside():
    lightsensor.measure_white()
    lightsensor.measure_reflective()
    # return False
    return lightsensor.silver()[0] or lightsensor.silver()[1] or not lightsensor.all_white()
    

def get_angle(angle: float, base_v: int, res=True):
    def inner() -> bool:
        gyro.update()
        return abs(gyro.angle[2]) > angle
    motor.stop(motor.MOT_AB)
    if res:
        gyro.reset()
    angle = angle - gyro.angle[2] # relative angle is better
    s = sign(angle)
    angle *= s
    motor.drive(motor.MOT_A, s * base_v)
    motor.drive(motor.MOT_B, -s * base_v)
    return inner


def get_timeout(t: int):
    def inner() -> bool:
        return utime.ticks_ms() > end
    end = utime.ticks_ms() + t
    return inner

def just_drive_angle(angle: float, t: int, res=True):
    # print("in just_drive_angle", angle)
    a = get_angle(angle, 70, res)
    timeout = get_timeout(t)
    while not a() and not timeout():
        pass
    motor.stop(motor.MOT_AB)

def just_drive_forward(t: int, rev = 1):
    motor.drive(motor.MOT_AB, rev * 70)
    timeout = get_timeout(t)
    while not timeout():
        pass
    motor.stop(motor.MOT_AB)

def try_scan() -> list[tuple[float, float, float]]:
    led.set_status_locked(2, led.RED)
    angle = get_angle(angle=-180.0, base_v=57)
    time_out = get_timeout(t=9000)
    data = []
    while not angle() and not time_out():
        tof.set(tof.ONE)
        upper = tof.read()
        tof.set(tof.THREE)
        lower = tof.read()
        data.append((upper, lower, gyro.angle[2]))
        print('test', (upper, lower, upper-lower))
    just_drive_angle(-gyro.angle[2], 4500)
    motor.stop(motor.MOT_AB)
    led.set_status_locked(2, led.GREEN)
    return data

def try_scan_and_break() -> tuple[bool, float]:
    led.set_status_locked(2, led.RED)
    angle = get_angle(angle=-180.0, base_v=57)
    time_out = get_timeout(t=9000)
    while not angle() and not time_out():
        tof.set(tof.ONE)
        upper = tof.read()
        tof.set(tof.THREE)
        lower = tof.read()
        # data.append((upper, lower, gyro.angle[2]))
        if check_diff_one((upper, lower, gyro.angle[2])):
            motor.stop(motor.MOT_AB)
            tof.set(tof.ONE)
            upper_now = tof.read()
            if check_diff_one((upper_now, lower, gyro.angle[2])):
                return (True, lower)
            else:
                angle = get_angle(angle=-180.0, base_v=57, res=False)
    just_drive_angle(-gyro.angle[2], 4500)
    motor.stop(motor.MOT_AB)
    led.set_status_locked(2, led.GREEN)
    return (False, 0.0)


def try_scan_stopping() -> list[tuple[float, float, float]]:
    led.set_status_locked(2, led.RED)
    gyro.reset()
    data =  []
    for i in range(0, 181, 5):
        i = float(i)
        just_drive_angle(i, 200, res=False)
        motor.stop(motor.MOT_AB)
        tof.set(tof.ONE)
        upper = tof.read()
        tof.set(tof.THREE)
        lower = tof.read()
        data.append((upper, lower, i))
    return data


def check_diff(data: list[tuple[float, float, float]]) -> tuple[float, float]:
    LIMIT_DIFF = 200.0
    OUT_OF_MAP_LIMIT = 1500.0
    max_diff = LIMIT_DIFF
    angle = 0.0
    distance = 0.0
    # print('test', data[:10]) 
    for i in range(len(data)):
        if data[i][0] - data[i][1] > max_diff and data[i][0] < OUT_OF_MAP_LIMIT:
            max_diff = data[i][0] - data[i][1]
            angle = data[i][2]
            distance = data[i][1]
    return angle, distance

def check_diff_one(data: tuple[float, float, float]):
    LIMIT_DIFF = 150.0
    OUT_OF_MAP_LIMIT = 1500.0
    return data[0] < OUT_OF_MAP_LIMIT and data[0] - data[1] > LIMIT_DIFF

def get_lowest(data: list[tuple[float, float, float]]) -> float:
    lowest = 4000.0
    lowest_angle = -1.0
    for i in range(len(data)):
        if data[i][0] < lowest:
            lowest = data[i][0]
            lowest_angle = data[i][2]
    # print("in get_lowest")
    # print("data: ", data)
    # print("lowest_angle", lowest_angle)
    return lowest_angle

def allign_with_wall():
    just_drive_angle(90, 1000)
    just_drive_forward(1500)
    just_drive_forward(1000, rev=-1)
    just_drive_angle(-90, 1000)


def drive_at_wall(t: int):
    led.set_status_locked(2, led.PURPLE)
    tof.set(tof.FOUR)
    if tof.read() < 400:
        allign_with_wall()
    # fahren
    tof.set(tof.ONE)
    motor.drive(motor.MOT_AB, 50)
    timeout = get_timeout(t)
    while not timeout():
        if is_outside():
            just_drive_forward(700, rev=-1)
            just_drive_angle(-90.0, 1000)
        if not button.right.value() or not button.left.value() or tof.read() < 200:
            just_drive_forward(300, rev=-1)
            just_drive_angle(-90.0, 1000)
    motor.stop(motor.MOT_AB)


def pick_ball(ball_angle: float, distance: float) -> int:
    just_drive_angle(ball_angle -10, 3000)
    motor.stop(motor.MOT_AB)
    led.set_status_locked(2, led.YELLOW)
    # utime.sleep_ms(1500)
    # grappler runter und aufmachen :)
    grappler.loose()
    grappler.down()
    motor.drive(motor.MOT_AB, 50)
    timeout = get_timeout(int(distance * 4 + 1000))
    while not timeout():
        if is_outside(): 
            break
    motor.stop(motor.MOT_AB)
    # grappler zu und hoch!!!
    grappler.grab()
    grappler.loose()
    tof.set(tof.THREE)
    # if tof.read() > 100:
    #     return False
    # else:11
    grappler.grab()
    grappler.up()
    utime.sleep_ms(300)
    # check with metal sens
    if button.read_metal():
        return BALL_ALIVE
    else:
        return BALL_DEAD
    # return BALL_ALIVE

def wall_opt(dist: float):
    tof.set(tof.FOUR)
    diff0 = tof.read()
    if diff0 - 50 < dist:
        just_drive_angle(90.0, 1000)
        just_drive_forward(300)
        just_drive_angle(-90.0, 1000)
    elif diff0 + 50 > dist:
        just_drive_angle(-90.0, 1000)
        just_drive_forward(300, rev=-1)
        just_drive_angle(90.0, 1000)
    diff1 = tof.read()
    just_drive_forward(300)
    diff2 = tof.read()
    just_drive_forward(300, rev=-1)
    just_drive_angle(diff2 - diff1, 1000)


def wall_bounce_allign():
    while button.left.value():
        just_drive_forward(400, rev=-1)
        just_drive_angle(-10, 700)
        just_drive_forward(600)

def drop_ball(ball_type: int):
    # an der wand ausrichten
    timeout = get_timeout(6000)
    motor.drive(motor.MOT_AB, 70)
    while not timeout() and button.left.value() and button.right.value():
        if is_outside():
            just_drive_forward(1000, rev=-1)
            just_drive_angle(-90.0, 1000)
            return drop_ball(ball_type)
    print('walll')
    motor.drive(motor.MOT_A, 90)
    motor.drive(motor.MOT_B, 50)
    utime.sleep_ms(1500)
    motor.drive(motor.MOT_A, 50)
    motor.drive(motor.MOT_B, 90)
    utime.sleep_ms(1500)
    print('allign')
    while True:
        motor.drive(motor.MOT_AB, 70)
        while not is_outside() and button.left.value() and button.right.value():
            pass
        motor.stop(motor.MOT_AB)
        if not is_outside():
            gyro.reset()
            just_drive_forward(300, rev=-1)
            motor.drive(motor.MOT_A, 90)
            motor.drive(motor.MOT_B, 50)
            utime.sleep_ms(2000)
            lightsensor.measure_front()
            if (color.get_front() == lightsensor.RED and ball_type == BALL_DEAD) or (color.get_front() == lightsensor.GREEN and ball_type == BALL_ALIVE):
                grappler.down()
                grappler.loose()
                return
            else:
                just_drive_forward(300, rev=-1)
        else:
            just_drive_forward(1000, rev=-1)
            just_drive_angle(90.0, 1000)
            # return drop_ball(ball_type)
        just_drive_forward(500, rev=-1)
        just_drive_angle(-90.0, 1000)


def drive_in_room():
    just_drive_forward(700)
    just_drive_angle(90, 1000)
    just_drive_forward(700)

def run():
    drive_in_room()
    counter = 0
    timeout = get_timeout(270_000)
    while not timeout():
        drive_at_wall(1200)
        flag, dist = try_scan_and_break()
        if flag:
            ball_type = pick_ball(0.0, dist)
            if ball_type:
                utime.sleep_ms(5000)
                drop_ball(ball_type)
                counter += 1
                if counter >= 3:
                    grappler.throw()
                    return

if __name__ == '__main__':
    drop_ball(BALL_ALIVE)
