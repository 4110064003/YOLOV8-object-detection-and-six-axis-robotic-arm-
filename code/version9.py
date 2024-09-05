from actions import action_groups
from BusServo import BusServo
from initial_position import action_groups_init
import ArmInversekinematics as ArmIK
import time
import math

class ArmController:
    def _init_(self,tx=26,rx=35,tx_en=25,rx_en=12):
        self.bus_servo = BusServo(tx-tx,rx=rx,tx_en=tx_en,rx_en=rx_en)
        self.A = [[-9.53128123, -0.00136586469],
                  [0.0417681628, 6.99054572]]
        self.b = [16.24220161, 84.9637588]
    def run_action_group(self):
        for action in action_group_init:
            servo_id = action['id']
            position = action['position']
            run_time = action['time']
            self.bus_servo.run(servo_id,position,run_time)
            max_time = max(action['time']for action in action_group_init)
            time.sleep(max_time / 1000.0)
    def convert_input_to_arm_coordinates(Self,input_x,input_y):
        arm_x = self.A[0][0] * input_x + self.A[0][1] * input_y + self.b[0]
        arm_y = self.A[1][0] * input_x + self.A[1][1] * input_y + self.b[1]
        
        arm_x = arm_x * 2
        arm_y = arm_y * 1.6
        
        print("Converted Coordinates: X={}, Y={}".format(arm_x, arm_y))
        return arm_x, arm_y
    
    def AngleConvert(self, angle, middle_angle, flip):
        #將角度轉換為伺服馬達的控制信號。
        p = 500 + (angle - middle_angle) * 25 / 6
        p = min(max(int(p), 0), 1000)
        return 1000 - p if flip else p





    def ArmControl_grab(self,object_coordinate,_time):
        converted_x ,converted_ = self.convert_input_to_arm_coordinates(object_coordinates[0], object_coordinates[1])
        adjusted_z=object_coordinates[2]+35
        while adjusted_z >= 30:
            angle = ArmIK.CalcAngle(X=converted_x, Y=converted_y, Z=adjusted_z)
            if angle == False:
              return False
            self.bus_servo.run(6, self.AngleConvert(angle[0], middle_angle=90, flip=False), _time)
            self.bus_servo.run(5, self.AngleConvert(angle[1] - 3, middle_angle=108, flip=True), _time)
            self.bus_servo.run(4, self.AngleConvert(angle[2] - 2, middle_angle=40, flip=False), _time)
            self.bus_servo.run(3, self.AngleConvert(angle[3] - 1, middle_angle=-120, flip=True), _time)
            self.bus_servo.run(2, 500, _time)
            self.bus_servo.run(1, 200, 1500)  # 設置夾爪打開，執行時間1500毫秒
            time.sleep(_time / 1000.0)
            
    def execute_arm_sequece(Self,object_label,destination_label,object_coordinates,destination_coordinates):
        self.run_action_group()
        time.sleep_ms(100)
        print("moving toward object{}".format(object_label))
        success_grab = self.ArmControl_grab(object_coordinates,2500)
        while object_coordinates[2] >= 30:
            angle = ArmIK.CalcAngle(X=converted_x, Y=converted_y, Z=adjusted_z)
            if angle == False:
              return False
        self.bus_servo.run(6, self.AngleConvert(angle[0], middle_angle=90, flip=False), _time)
        self.bus_servo.run(5, self.AngleConvert(angle[1] - 3, middle_angle=108, flip=True), _time)
        self.bus_servo.run(4, self.AngleConvert(angle[2] - 2, middle_angle=40, flip=False), _time)
        self.bus_servo.run(3, self.AngleConvert(angle[3] - 1, middle_angle=-120, flip=True), _time)
        self.bus_servo.run(2, 500, _time)
        self.bus_servo.run(1, 200, 1500)
        time.sleep(_time / 1000.0)
        self.bus_servo.run(1, 700, 500)  # 初始夾爪閉合，執行時間500毫秒
        print(1)