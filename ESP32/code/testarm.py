from actions import action_groups
from BusServo import BusServo
from initial_position import action_groups_init
import ArmInversekinematics as ArmIK
import time, ustruct
import math

bus_servo = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)

def convert_input_x_to_arm_x(input_x,input_y):
    # 定義線性變換矩陣 A 和位移向量 b
    A = [[-9.53128123, -0.00136586469],
         [0.0417681628, 6.99054572]]
    b = [16.24220161, 84.9637588]
    
    # 計算對應的 (x2, y2)
    arm_x = A[0][0] * input_x + A[0][1] * input_y + b[0]
    arm_x = arm_x*1.65
    print(arm_x)
    return arm_x

def convert_input_y_to_arm_y(input_x,input_y):
    A = [[-9.53128123, -0.00136586469],
         [0.0417681628, 6.99054572]]
    b = [16.24220161, 84.9637588]
    
    # 計算對應的 (x2, y2)
    arm_y = A[1][0] * input_x + A[1][1] * input_y + b[1]
    arm_y = arm_y*1.2
    print(arm_y)
    return arm_y

def run_action_group(BusServo, action_groups_init):
    for action in action_groups_init:
        servo_id = action['id']
        position = action['position']
        run_time = action['time']

        BusServo.run(servo_id, position, run_time)
  
    max_time = max(action['time'] for action in action_groups_init)
    time.sleep(max_time / 1000.0)

def AngleConvert(angle, middle_angle, flip):
    # 0~240° ————> 0~1000
    p = 500 + (angle - middle_angle) * 25 / 6
    if p < 0:
        p = 0
    elif p > 1000:
        p = 1000
    if flip:

        return 1000 - int(p)

    #print(p)

    return int(p)



def calculate_distance(x, y):

    # 計算從原點到 (x, y) 點的水平距離

    return math.sqrt(x**2 + y**2)



def adjust_z_based_on_distance(x, y, z):

    distance = calculate_distance(x, y)
    # 根據距離調整 z 的值 (這些參數可以根據實際需要調整)
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
    elif distance >= 100:
        z += 30
    else:
        z += 40
    return z

def ArmControl_grab(object_coordinates, _time):
    converted_x = convert_input_x_to_arm_x(object_coordinates[0])
    converted_y = convert_input_y_to_arm_y(object_coordinates[1])
    adjusted_z = adjust_z_based_on_distance(converted_x,converted_y, object_coordinates[2])  # 調整 z 高度
    angle = ArmIK.CalcAngle(X= converted_x, Y= converted_y, Z= adjusted_z)

    if angle == False:
        return False
    bus_servo.run(6, AngleConvert(angle[0], middle_angle=90, flip=False), _time)
    bus_servo.run(5, AngleConvert(angle[1] - 3, middle_angle=108, flip=True), _time)
    bus_servo.run(4, AngleConvert(angle[2] - 2, middle_angle=40, flip=False), _time)
    bus_servo.run(3, AngleConvert(angle[3] - 1, middle_angle=-120, flip=True), _time)
    bus_servo.run(2, 500, _time)
    bus_servo.run(1, 200, 1000)  # 設置夾爪打開，執行時間1000毫秒
    time.sleep(_time / 1000.0)
    bus_servo.run(1, 600, 1000)  # 設置夾爪閉合，執行時間1000毫秒
    time.sleep(_time / 1500.0)
    bus_servo.run(5, AngleConvert(angle[1] - 3, middle_angle=115, flip=True), _time)
    #print(angle)
    return True

def ArmControl_release(destination_coordinates, _time):
    converted_x = convert_input_x_to_arm_x(destination_coordinates[0])
    converted_y = convert_input_y_to_arm_y(destination_coordinates[1])
    adjusted_z = adjust_z_based_on_distance(converted_x,converted_y,destination_coordinates[2])
    angle = ArmIK.CalcAngle(X= converted_x, Y= converted_y, Z= adjusted_z)
    if angle == False:
        return False

    bus_servo.run(6, AngleConvert(angle[0], middle_angle=90, flip=False), _time)
    bus_servo.run(5, AngleConvert(angle[1] - 3, middle_angle=108, flip=True), _time)
    bus_servo.run(4, AngleConvert(angle[2] - 2, middle_angle=40, flip=False), _time)
    bus_servo.run(3, AngleConvert(angle[3] - 1, middle_angle=-120, flip=True), _time)
    bus_servo.run(2, 500, _time)
    bus_servo.run(1, 600, 1000)  # 設置夾爪打開，執行時間1000毫秒
    time.sleep(_time / 1000.0)
    bus_servo.run(1, 300, 1000)
    #print(angle)
    return True

if __name__ == '__main__':
        
    while True:
      object_input = input("object_label (space) x_coor (space) y_coor (space) z_coor: ")
      destination_input = input("destination_label (space) x_coor (space) y_coor (space) z_coor: ")

      object_list = object_input.split()
      destination_list = destination_input.split()

      object_label = object_list[0]
      destination_label = destination_list[0]

      object_coordinates = list(map(int, object_list[1:]))
      destination_coordinates = list(map(int, destination_list[1:]))
      time.sleep_ms(1000)
      
      run_action_group(bus_servo, action_groups_init)
      time.sleep_ms(100)
      print("moving toward object {}".format(object_label))
      ArmControl_grab(object_coordinates, 2500)
      time.sleep_ms(2500)
      
      time.sleep_ms(100)
      print("move object {} to destination {}".format(object_label, destination_label))
      ArmControl_release(destination_coordinates, 2500)

      time.sleep_ms(2000)

      run_action_group(bus_servo, action_groups_init)

      time.sleep(2.5)  # 等待釋放動作完成





