#程式整合
from actions import action_groups
from BusServo import BusServo
from initial_position import action_groups_init
import ArmInversekinematics as ArmIK
import time
import math

class ArmController:
    def __init__(self, tx=26, rx=35, tx_en=25, rx_en=12):
        self.bus_servo = BusServo(tx=tx, rx=rx, tx_en=tx_en, rx_en=rx_en)
        self.A = [[-9.53128123, -0.00136586469],
                  [0.0417681628, 6.99054572]]
        self.b = [16.24220161, 84.9637588]

    def convert_input_to_arm_coordinates(self, input_x, input_y):
        #將輸入的 x 和 y 座標轉換為機械臂的 x 和 y 座標
        arm_x = self.A[0][0] * input_x + self.A[0][1] * input_y + self.b[0]
        arm_y = self.A[1][0] * input_x + self.A[1][1] * input_y + self.b[1]
        
        arm_x = arm_x * 1.65
        arm_y = arm_y * 1.2
        
        print("Converted Coordinates: X={}, Y={}".format(arm_x, arm_y))
        return arm_x, arm_y

    def run_action_group(self):
        #執行一組動作
        for action in action_groups_init:
            servo_id = action['id']
            position = action['position']
            run_time = action['time']
            self.bus_servo.run(servo_id, position, run_time)
      
        max_time = max(action['time'] for action in action_groups_init)
        time.sleep(max_time / 1000.0)

    def AngleConvert(self, angle, middle_angle, flip):
        #將角度轉換為伺服馬達的控制信號。
        p = 500 + (angle - middle_angle) * 25 / 6
        p = min(max(int(p), 0), 1000)
        return 1000 - p if flip else p

    def calculate_distance(self, x, y):
        #計算從原點到 (x, y) 點的距離。
        return x**2 + y**2

    def adjust_z_based_on_distance(self, x, y, z):
        #根據距離調整 Z 座標。
        distance = self.calculate_distance(x, y)
        if distance >= 745:
            z -= 20
        elif distance >= 392:
            z -= 10
        elif distance >= 338:
            z -= 0
        elif distance >= 242:
            z += 10
        elif distance >= 200:
            z += 20
        elif distance >= 170:
            z += 30
        else:
            z += 40
        print("Adjusted Z:", z)
        return z

    def ArmControl_grab(self, object_coordinates, _time):
        #執行抓取動作。
        converted_x, converted_y = self.convert_input_to_arm_coordinates(object_coordinates[0], object_coordinates[1])
        adjusted_z = self.adjust_z_based_on_distance(object_coordinates[0], object_coordinates[1], object_coordinates[2])
        angle = ArmIK.CalcAngle(X=converted_x, Y=converted_y, Z=adjusted_z)

        if angle == False:
            return False

        self.bus_servo.run(6, self.AngleConvert(angle[0], middle_angle=90, flip=False), _time)
        self.bus_servo.run(5, self.AngleConvert(angle[1] - 3, middle_angle=108, flip=True), _time)
        self.bus_servo.run(4, self.AngleConvert(angle[2] - 2, middle_angle=40, flip=False), _time)
        self.bus_servo.run(3, self.AngleConvert(angle[3] - 1, middle_angle=-120, flip=True), _time)
        self.bus_servo.run(2, 500, _time)
        self.bus_servo.run(1, 200, 1000)  # 設置夾爪打開，執行時間1000毫秒
        time.sleep(_time / 1000.0)
        self.bus_servo.run(1, 600, 1000)  # 設置夾爪閉合，執行時間1000毫秒
        time.sleep(_time / 1500.0)
        self.bus_servo.run(5, self.AngleConvert(angle[1] - 3, middle_angle=115, flip=True), _time)
        return True

    def ArmControl_release(self, destination_coordinates, _time):
        #執行釋放動作。
        converted_x, converted_y = self.convert_input_to_arm_coordinates(destination_coordinates[0], destination_coordinates[1])
        adjusted_z = self.adjust_z_based_on_distance(destination_coordinates[0], destination_coordinates[1], destination_coordinates[2])
        angle = ArmIK.CalcAngle(X=converted_x, Y=converted_y, Z=adjusted_z)

        if angle == False:
            return False

        self.bus_servo.run(6, self.AngleConvert(angle[0], middle_angle=90, flip=False), _time)
        self.bus_servo.run(5, self.AngleConvert(angle[1] - 3, middle_angle=108, flip=True), _time)
        self.bus_servo.run(4, self.AngleConvert(angle[2] - 2, middle_angle=40, flip=False), _time)
        self.bus_servo.run(3, self.AngleConvert(angle[3] - 1, middle_angle=-120, flip=True), _time)
        self.bus_servo.run(2, 500, _time)
        self.bus_servo.run(1, 600, 1000)  # 設置夾爪打開，執行時間1000毫秒
        time.sleep(_time / 1000.0)
        self.bus_servo.run(1, 300, 1000)
        return True

    def execute_arm_sequence(self,object_label,destination_label, object_coordinates, destination_coordinates):
        #執行整個抓取和釋放的動作序列。
        self.run_action_group()
        time.sleep_ms(100)
        
        print("moving toward object {}".format(object_label))
        success_grab = self.ArmControl_grab(object_coordinates, 2500)
        
        if success_grab:
            time.sleep_ms(2500)
            time.sleep_ms(100)
            print("move object {} to destination {}".format(object_label, destination_label))
            self.ArmControl_release(destination_coordinates, 2500)
        
        time.sleep_ms(2000)
        self.run_action_group()
        time.sleep(2.5)  # 等待釋放動作完成



