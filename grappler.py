import servo

_servo_turn = servo.THREE
_servo_grab = servo.FOUR


def up():
    servo.set_angle(_servo_turn, -90)


def down():
    servo.set_angle(_servo_turn, 90)


def grab():
    servo.set_angle(_servo_grab, -90)


def loose():
    servo.set_angle(_servo_grab, 60)
