#修改逆向運動學的算法(投影三角法)
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
    
    def angle_convert(self, distance, start_num, middle_angle, factor, offset, sign, constant):#servo1~5
        angle = start_num + factor * (distance - offset)
        print("the angle of servo is", angle)
        p = 500 + sign * (angle - middle_angle) * 25 / 6 + int(constant)
        p = max(0, min(1000, p))
        print("the p of servo is", p)
        return int(p)
        
    def AngleConvert(self, angle, middle_angle):#servo 6
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
        
        L1 = 101 #連桿1長度
        L2 = 95  #連桿2長度
        L3 = 165 #連桿3長度(含夾爪閉合後長度)
        baseHeight = 65 #基座的高度
        cubeHalfHeight = 15 #方塊一半的高度

        distance_project_part1  = 0.17 * dist
        print(" 0.17*d = ",distance_project_part1)
        distance_project_part2  = 0.83 * dist
        print(" 0.83*d = ",distance_project_part2)
        height1 = math.sqrt(L1 ** 2 - distance_project_part1  ** 2)#L1 * cos(180-theta1)
        print("a = ",height1)
        theta1_sup = (L1** 2 + distance_project_part1  ** 2 - height1 **2)/(2*L1*distance_project_part1 )#theta1補角-餘弦公式-三邊長求夾角
        print("180-theta1 = ",theta1_sup)
        theta1_sup_angle = math.degrees(math.acos(theta1_sup))
        print("180-theta1 = ",theta1_sup_angle)
        theta1 = 180  - theta1_sup_angle
        print("theta1 = ",theta1)

        #計算theta3
        height2 = height1 + baseHeight
        print("b = ",height2)
        height3 = height2 - cubeHalfHeight
        print("c = ",height3)
        hyp1 = math.sqrt(height3 ** 2 + distance_project_part2  ** 2)
        print("d = ",hyp1)
        theta3_sup = (L3** 2 + L2  ** 2 - hyp1 **2)/(2*L3*L2 )#theta3補角-餘弦公式-三邊長求夾角
        print("180-theta3 = ",theta3_sup)
        theta3_sup_angle = math.degrees(math.acos(theta3_sup))
        print("180-theta3 = ",theta3_sup_angle)
        theta3 = 180  - theta3_sup_angle
        print("theta3 = ",theta3)

        #計算theta2
        theta2_sup1 = (L1** 2 + height1 ** 2 - distance_project_part1 **2)/(2 * L1 * height1 )#theta2補角-餘弦公式-三邊長求夾角
        print("o1 = ",theta2_sup1)
        theta2_sup1_angle = math.degrees(math.acos(theta2_sup1))
        print("o1 = ",theta2_sup1_angle)
        theta2_sup2 = (hyp1** 2 + height3 ** 2 - distance_project_part2 **2)/(2 * hyp1 * height3 )#theta2補角-餘弦公式-三邊長求夾角
        print("o2 = ",theta2_sup2)
        theta2_sup2_angle = math.degrees(math.acos(theta2_sup2))
        print("o2 = ",theta2_sup2_angle)
        theta2_sup3 = (L2** 2 + hyp1 ** 2 - L3 **2)/(2 * L2 * hyp1 )#theta2補角-餘弦公式-三邊長求夾角
        print("o3 = ",theta2_sup3)
        theta2_sup3_angle = math.degrees(math.acos(theta2_sup3))
        print("o3 = ",theta2_sup3_angle)
        theta2 = 180  - theta2_sup1_angle - theta2_sup2_angle - theta2_sup3_angle
        print("theta2",theta2)

        self.bus_servo.run(6, self.AngleConvert(angle[0], middle_angle=90), _time)
        self.bus_servo.run(5, int(theta1), _time)
        self.bus_servo.run(4, int(theta2), _time)
        self.bus_servo.run(3, int(theta3), _time)
        self.bus_servo.run(2, 500, _time)
        self.bus_servo.run(1, int(pID1), _time)
        
        return True, theta1

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





