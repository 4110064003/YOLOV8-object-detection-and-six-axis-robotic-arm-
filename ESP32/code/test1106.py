#距離法推算角度(微調後)
from actions import action_groups
from BusServo import BusServo
from initial_position import action_groups_init
import ArmInversekinematics as ArmIK
import time
import math
import random

class ArmController:
    def __init__(self, tx=26, rx=35, tx_en=25, rx_en=12):
        self.bus_servo = BusServo(tx=tx, rx=rx, tx_en=tx_en, rx_en=rx_en)

    def convert_input_to_arm_coordinates(self, input_x, input_y):
        arm_y = input_y + 220
        arm_x = input_x + 10 
        
        print("Converted Coordinate:X={},Y={}".format(arm_x, arm_y))
        return arm_x, arm_y
    
    def run_action_group(self, bus_servo, action_groups_init):
        for action in action_groups_init:
            servo_id = action['id']
            position = action['position']
            run_time = action['time']
            bus_servo.run(servo_id, position, run_time)
        max_time = max(action['time'] for action in action_groups_init)
        time.sleep(max_time / 1000.0)
    
    def angle_convert(self, distance, start_num, middle_angle, factor, offset, sign, constant):
        angle = start_num + factor * (distance - offset)
        print("the angle of servo is", angle)
        p = 500 + sign * (angle - middle_angle) * 25 / 6 + int(constant)
        p = max(0, min(1000, p))
        print("the p of servo is", p)
        return int(p)
        
    def AngleConvert(self, angle, middle_angle):
        p = 500 + (angle - middle_angle) * 25 / 6
        p = max(0, min(1000, p))
        print("the p of id6 is:", p)
        return int(p)
        
    def calculate_distance(self, coordinate):
        arm_x,arm_y=self.convert_input_to_arm_coordinates(coordinate[0],coordinate[1])
        x, y = arm_x,arm_y
        distance = math.sqrt(x ** 2 + y ** 2)
        print("the distance between object and robot is:", distance)
        return round(distance)
    
    def GoToObject(self, pID1, coordinate, _time):
        dist = self.calculate_distance(coordinate)
        arm_x,arm_y=self.convert_input_to_arm_coordinates(coordinate[0],coordinate[1])
        angle = ArmIK.CalcAngle(X=arm_x, Y=arm_y, Z=coordinate[2])
        if angle == False:
            print("Distance out of range")
            return False, 0
        
        parameters = [
            (100, 155, {"pID5": (90, 90, 0.3, 100, -1, 5), "pID4": (90, 0, -0.4, 100, 1, 0), "pID3": (90, 0, -0.16, 100, -1, 0)}),
            (155, 170, {"pID5": (120, 90, 0.2, 200, -1, 0), "pID4": (50, 0, -0.2, 200, 1, 0), "pID3": (90, 0, -0.04, 100, -1, 0)}),
            (170, 190, {"pID5": (120, 90, 0.2, 200, -1, 0), "pID4": (50, 0, -0.2, 200, 1, 0), "pID3": (90, 0, -0.1, 100, -1, 0)}),
            (190, 230, {"pID5": (120, 90, 0.2, 200, -1, 5), "pID4": (50, 0, -0.2, 200, 1, 0), "pID3": (90, 0, -0.13, 100, -1, 0)}),
            (230, 260, {"pID5": (120, 90, 0.2, 200, -1, -5), "pID4": (50, 0, -0.2, 200, 1, 0), "pID3": (90, 0, -0.17, 100, -1, 0)}),
            (260, 290, {"pID5": (120, 90, 0.2, 200, -1, -5), "pID4": (50, 0, -0.2, 200, 1, 0), "pID3": (90, 0, -0.19, 100, -1, 0)}),
            (290, 310, {"pID5": (120, 90, 0.2, 200, -1, -13), "pID4": (50, 0, -0.2, 200, 1, 0), "pID3": (90, 0, -0.21, 100, -1, 0)}),
            (310, 330, {"pID5": (120, 90, 0.2, 200, -1, -30), "pID4": (50, 0, -0.2, 200, 1, 0), "pID3": (90, 0, -0.26, 100, -1, 0)})
        ]
        
        selected_params = None
        for min_dist, max_dist, param_set in parameters:
            if min_dist < dist <= max_dist:
                selected_params = param_set
                break
        
        if selected_params is None:
            print("Distance out of range")
            return False, 0
        
        pID5 = self.angle_convert(dist, *selected_params["pID5"])
        pID4 = self.angle_convert(dist, *selected_params["pID4"])
        pID3 = self.angle_convert(dist, *selected_params["pID3"])

        self.bus_servo.run(6, self.AngleConvert(angle[0], middle_angle=90), _time)
        self.bus_servo.run(5, int(pID5), _time)
        self.bus_servo.run(4, int(pID4), _time)
        self.bus_servo.run(3, int(pID3), _time)
        self.bus_servo.run(2, 500, _time)
        self.bus_servo.run(1, int(pID1), _time)
        
        return True, pID5

    def Grab(self, pID5_value, _time):
        time.sleep_ms(3000)
        self.bus_servo.run(1, 600, _time)
        print("Grabbing: Servo 1 closed at 600 position")  # 增加此輸出
        time.sleep_ms(3000)
        self.bus_servo.run(5, int(pID5_value) + 50, _time)
        print("Adjusting pID5 position after grabbing")  # 增加此輸出
        time.sleep_ms(3000)

    def Release(self, pID5_value, _time):
        time.sleep_ms(3000)
        self.bus_servo.run(1, 200, _time)
        print("Releasing: Servo 1 opened at 200 position")  # 增加此輸出
        time.sleep_ms(3000)
        print("Initializing position")
        self.run_action_group(self.bus_servo, action_groups_init)
        print("Action group initialization completed")  # 增加此輸出
        time.sleep_ms(3000)
        
    def execute_arm_sequence(self, object_label, destination_label, object_coordinates, destination_coordinates):
        self.bus_servo.run(1,200,1000)
        print("Initializing position")
        time.sleep_ms(3000)
        self.run_action_group(self.bus_servo, action_groups_init)
        time.sleep_ms(3000)
        
        print("Moving toward object {}".format(object_label))
        time.sleep_ms(3000)
        self.bus_servo.run(3,400,1000)
        success, pID5_value = self.GoToObject(200, object_coordinates, 2500)
        time.sleep_ms(2500)
        self.Grab(pID5_value, 500)
        time.sleep_ms(3000)

        
        print("Move object {} to destination {}".format(object_label, destination_label))
        arm_x,arm_y=self.convert_input_to_arm_coordinates(destination_coordinates[0],destination_coordinates[1])
        angle = ArmIK.CalcAngle(X=arm_x, Y=arm_y, Z=destination_coordinates[2])
        
        self.bus_servo.run(6, self.AngleConvert(angle[0], middle_angle=90), 1000)
        time.sleep_ms(3500)
        success, pID5_value = self.GoToObject(600, destination_coordinates, 2500)
        time.sleep_ms(3000)
        self.Release(pID5_value, 500)
        time.sleep_ms(3000)
        
        # 確保夾爪回到開啟狀態
        self.bus_servo.run(1, 200, 1000)
        print("Ensuring gripper is open for next sequence")  # 增加此輸出
        time.sleep_ms(3000)
        
        # 完全重設伺服器以準備下一次循環
        print("Resetting arm and gripper for next iteration")

        self.run_action_group(self.bus_servo, action_groups_init)

        time.sleep_ms(5000)  # 延長延遲，確保伺服器有足夠時間完成重設





