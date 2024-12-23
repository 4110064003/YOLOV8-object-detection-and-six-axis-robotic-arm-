from actions import action_groups
from BusServo import BusServo
from initial_position import action_groups_init
import ArmInversekinematics as ArmIK
import time
import math

bus_servo = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)

# Function to run servo actions
def run_action_group(bus_servo, action_groups_init):
    for action in action_groups_init:
        servo_id = action['id']
        position = action['position']
        run_time = action['time']
        bus_servo.run(servo_id, position, run_time)
    max_time = max(action['time'] for action in action_groups_init)
    time.sleep(max_time / 1000.0)

# Unified function for angle conversion
def angle_convert(distance, middle_angle, factor, offset, flip=False):
    angle = middle_angle + factor * (distance - offset)
    p = 500 + (angle - middle_angle) * 25 / 6
    p = max(0, min(1000, p))
    if flip:
        return 1000 - int(p)
    return int(p)

# Calculate distance between the object and the base of the robot arm
def calculate_distance(coordinate):
    x, y = coordinate[0], coordinate[1]
    distance = math.sqrt(x ** 2 + y ** 2)
    return round(distance)

# Control the arm based on distance
def arm_control(coordinate, _time):
    dist = calculate_distance(coordinate)
    angle = ArmIK.CalcAngle(X=coordinate[0], Y=coordinate[1], Z=coordinate[2])

    if 100 < dist <= 200:
        pID5 = angle_convert(dist, middle_angle=90, factor=0.3, offset=100)
        pID4 = angle_convert(dist, middle_angle=0, factor=-0.4, offset=100)
        pID3 = angle_convert(dist, middle_angle=0, factor=-0.2, offset=100)
    elif 200 < dist <= 350:
        pID5 = angle_convert(dist, middle_angle=90, factor=0.2, offset=200)
        pID4 = angle_convert(dist, middle_angle=0, factor=-0.2, offset=200)
        pID3 = angle_convert(dist, middle_angle=0, factor=-0.2, offset=100)
    else:
        print("Distance out of range")
        return False

    bus_servo.run(6, angle_convert(angle[0], middle_angle=90, factor=1, offset=0), _time)
    bus_servo.run(5, pID5, _time)
    bus_servo.run(4, pID4, _time)
    bus_servo.run(3, pID3, _time)
    bus_servo.run(2, 500, _time)
    bus_servo.run(1, 500, _time)
    return True

if __name__ == '__main__':
    while True:
        coordinate = []
        coordinate.append(int(input("請輸入x座標: ")))
        coordinate.append(int(input("請輸入y座標: ")))
        coordinate.append(int(input("請輸入z座標: ")))
        run_action_group(bus_servo, action_groups_init)
        time.sleep(0.1)
        arm_control(coordinate, 2.5)
        time.sleep(2.5)

