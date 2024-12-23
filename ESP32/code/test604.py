from actions import action_groups
from BusServo import BusServo
from initial_position import action_groups_init
import ArmInversekinematics as ArmIK
import time
import math
import random

bus_servo = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)

# Generate random coordinate within specified constraints
def generate_random_coordinate():
    while True:
        x = random.randint(-299, 299)
        y = random.randint(101, 299)
        z = random.randint(101, 299)
        distance = math.sqrt(x ** 2 + y ** 2)
        if 100 < distance < 350:
            return [x, y, z]
            
# Function to run servo actions
def run_action_group(bus_servo, action_groups_init):
    for action in action_groups_init:
        servo_id = action['id']
        position = action['position']
        run_time = action['time']
        bus_servo.run(servo_id, position, run_time)
    max_time = max(action['time'] for action in action_groups_init)
    time.sleep(max_time / 1000.0)

# Unified function for angle conversion for ID3~ID5
def angle_convert(distance,start_num,middle_angle, factor, offset,sign,constant):
    angle = start_num + factor * (distance - offset)
    #print(f"the angle of {servo_id} is:{angle}")
    print("the angle of servo is",angle)
    p = 500 +sign*(angle - middle_angle) * 25 / 6 + int(constant)
    p = max(0, min(1000, p))
    #print(f"the p of {servo_id} is:{p}")
    print("the p of servo is",p)
    return int(p)
    
# Unified function for angle conversion for ID6   
def AngleConvert(angle, middle_angle):
    # 0~240° ————> 0~1000
    p = 500 + (angle - middle_angle) * 25 / 6
    if p < 0:
      p = 0
    elif p > 1000:
      p = 1000
    print("the p of id6 is:", p)
    return int(p)

# Calculate distance between the object and the base of the robot arm
def calculate_distance(coordinate):
    x, y = coordinate[0], coordinate[1]
    distance = math.sqrt(x ** 2 + y ** 2)
    print("the distance between to object and robot is: ", distance)
    return round(distance)

# Control the arm based on distance
def GoToObject(pID1,coordinate, _time):
    dist = calculate_distance(coordinate)
    angle = ArmIK.CalcAngle(X=coordinate[0], Y=coordinate[1], Z=coordinate[2])

    if 100 < dist <= 200:
        pID5 = angle_convert(dist,start_num=90, middle_angle=90, factor=0.3, offset=100 ,sign=-1,constant=50)
        pID4 = angle_convert(dist,start_num=90, middle_angle=0, factor=-0.4, offset=100 ,sign=1 ,constant=0)
        pID3 = angle_convert(dist,start_num=90, middle_angle=0, factor=-0.2, offset=100 ,sign=-1,constant=0)
    elif 200 < dist <= 350:
        pID5 = angle_convert(dist,start_num=120, middle_angle=90, factor=0.2, offset=200 ,sign=-1,constant=-10)
        pID4 = angle_convert(dist,start_num=50 , middle_angle=0, factor=-0.2, offset=200 ,sign=1,constant=0)
        pID3 = angle_convert(dist,start_num=90 , middle_angle=0, factor=-0.2, offset=100 ,sign=-1,constant=0)
    else:
        print("Distance out of range")
        return False
        
    bus_servo.run(6, AngleConvert(angle[0], middle_angle=90), _time)
    bus_servo.run(5, int(pID5), _time)
    bus_servo.run(4, int(pID4), _time)
    bus_servo.run(3, int(pID3), _time)
    bus_servo.run(2, 500, _time)
    bus_servo.run(1, int(pID1), _time)
    return True,pID5
    
def Grab(pID5_value,_time):
    bus_servo.run(1, 200, _time)
    time.sleep_ms(800)
    bus_servo.run(5,int(pID5_value)-50, _time)
    bus_servo.run(1, 600, _time)
    
def Release(pID5_value,_time):
    bus_servo.run(5,int(pID5_value)-50, _time)
    time.sleep_ms(1500)
    bus_servo.run(1, 200, _time)
    time.sleep_ms(800)
    print(4)
    #bus_servo.run(5,int(pID5_value)+50, _time)
    #bus_servo.run(1, 600, _time)
    
  

if __name__ == '__main__':
    while True:
      coordinate1 = generate_random_coordinate()
      print("Generated object coordinate:" , coordinate1)
      # coordinate1.append(int(input("請輸入物件x座標: ")))
      # coordinate1.append(int(input("請輸入物件y座標: ")))
      # coordinate1.append(int(input("請輸入物件z座標: ")))
      
      print ("initialzed position")
      run_action_group(bus_servo, action_groups_init)
      time.sleep_ms(100) 
      print ("go to the object",coordinate1[0], coordinate1[1], coordinate1[2])
      
      success, pID5_value = GoToObject(500, coordinate1, 2500)
      time.sleep_ms(2500)
      Grab(pID5_value,800) 
      time.sleep_ms(2500)
      
      coordinate2 = generate_random_coordinate()
      print("Generated destination coordinate" , coordinate2)
      # coordinate2.append(int(input("請輸入目的x座標: ")))
      # coordinate2.append(int(input("請輸入目的y座標: ")))
      # coordinate2.append(int(input("請輸入目的z座標: ")))
      
      print ("go to the destination",coordinate2[0], coordinate2[1], coordinate2[2])
      success, pID5_value = GoToObject(600, coordinate2, 2500)
      time.sleep_ms(2500)
      Release(pID5_value,2000) 
      time.sleep_ms(2500)
      run_action_group(bus_servo, action_groups_init)
      time.sleep_ms(100)





