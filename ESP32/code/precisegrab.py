# give the space coordinate and tha robot arm will go to the point precisely
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

# Unified function for angle conversion for ID3~ID5
# we don't use inversekinematic to get the angle of servo ID3~ID5 but use self define rule to get grab position
def angle_convert(distance,start_num,middle_angle, factor, offset,sign,constant):
    
    angle = start_num + factor * (distance - offset)
    #for distance between 100mm~200mm
    #angleID5 = 90 + 0.3*(distance-100) #range 90~180
    #angleID4 = 90 - 0.4*(distance-100) #range 0~90
    #angleID3 = 90 - 0.2*(distance-100 )#range 0~90

    #for distance between 210mm~350mm
    #angleID5 = 120 + 0.2*(distance-200) #range 90~180 ,angleID5 = 120 at 200mm
    #angleID4 = 50  - 0.2*(distance-200) #range 0~90   ,angleID4 = 50  at 200mm
    #angleID3 = 90  - 0.2*(distance-100) #range 0~90
    
    #print(f"the angle of {servo_id} is:{angle}")
    print("the angle of servo is",angle)

    p = 500 +sign*(angle - middle_angle) * 25 / 6 + int(constant)
    #for distance between 100mm~200mm
    #pID5 = 500-(angleID5-middle_angle) * 25 / 6     #range 0~500   , middle_angle = 90
    #pID4 = 500+(angleID4-middle_angle) * 25 / 6     #range 500~1000, middle_angle = 0
    #pID3 = 500-(angleID3-middle_angle) * 25 / 6     #range 0~500   , middle_angle = 0 
    
    #for distance between 210mm~350mm
    #pID5 = 500-(angleID5-middle_angle) * 25 / 6 -10 #range 0~500   , middle_angle = 90
    #pID4 = 500+(angleID4-middle_angle) * 25 / 6     #range 500~1000, middle_angle = 0
    #pID3 = 500-(angleID3-middle_angle) * 25 / 6     #range 0~500   , middle_angle = 0

    #restrict the p value between 0~1000
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

# Control the arm to get to object position based on distance
def GoToObject(coordinate, _time):
    dist = calculate_distance(coordinate)
    # we use inversekenematic to get the angle of servo ID6 (main direction of the object)   
    angle = ArmIK.CalcAngle(X=coordinate[0], Y=coordinate[1], Z=coordinate[2])

    if 100 < dist <= 200:
        pID5 = angle_convert(dist,start_num=90, middle_angle=90, factor=0.3, offset=100 ,sign=-1,constant=0)
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
    # we assume the angle of servo ID2、ID1 to default (wrist and clip)
    bus_servo.run(2, 500, _time)
    bus_servo.run(1, 500, _time)
    return True

if __name__ == '__main__':
    while True:
      coordinate = []
      coordinate.append(int(input("請輸入x座標: ")))
      coordinate.append(int(input("請輸入y座標: ")))
      coordinate.append(int(input("請輸入z座標: ")))
      
      print ("initialzed position")
      run_action_group(bus_servo, action_groups_init)
      time.sleep_ms(100) 
      print ("go to the object")
      GoToObject(coordinate,2500) 
      time.sleep_ms(2500)





