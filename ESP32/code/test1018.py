#距離法推算角度初步設計
from actions import action_groups
from BusServo import BusServo
from initial_position import action_groups_init
import ArmInversekinematics as ArmIK
import time, ustruct
import math

bus_servo = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)

#function for run servo 
def run_action_group(BusServo, action_groups_init):
    for action in action_groups_init:
        servo_id = action['id']
        position = action['position']
        run_time = action['time']

        BusServo.run(servo_id, position, run_time)
  
    max_time = max(action['time'] for action in action_groups_init)
    time.sleep(max_time / 1000.0)

#for distance between 100mm~200mm             
def AngleConvertID5_close(distance, middle_angle):
  angleID5 = 90 + 0.3(distance-100)#range 90~180
  print (angleID5)
  pID5 = 500-(angleID5-middle_angle) * 25 / 6 #range 0~500 , middle_angle=90
  print (pID5)
  return int(pID5)
  
def AngleConvertID4_close(distance, middle_angle):
  angleID4 = 90 - 0.4(distance-100)#range 0~90
  print (angleID4)
  pID4 = 500+(angleID4-middle_angle) * 25 / 6 #range 500~1000, middle_angle=0
  print (pID4)
  return int(pID4)

def AngleConvertID3_close(distance, middle_angle):
  angleID3 = 90 - 0.2(distance-100)#range 0~90
  print (angleID3)
  pID3 = 500-(angleID3-middle_angle) * 25 / 6 #range 0~500, middle_angle=0
  print (pID3)
  return int(pID3)
  
#for distance between 210mm~350mm     
def AngleConvertID5_far(distance, middle_angle):
  angleID5 = 120 + 0.2(distance-200)#range 90~180 ,angleID5=120 at 200mm
  print (angleID5)
  pID5 = 500-(angleID5-middle_angle) * 25 / 6 -10#range 0~500 , middle_angle=90
  print (pID5)
  return int(pID5)
  
def AngleConvertID4_far(distance, middle_angle):
  angleID4 = 50 - 0.2(distance-200)#range 0~90 ,,angleID4=50 at 200mm
  print (angleID4)
  pID4 = 500+(angleID4-middle_angle) * 25 / 6 #range 500~1000, middle_angle=0
  print (pID4)
  return int(pID4)

def AngleConvertID3_far(distance, middle_angle):
  angleID3 = 90 - 0.2(distance-100)#range 0~90
  print (angleID3)
  pID3 = 500-(angleID3-middle_angle) * 25 / 6 #range 0~500, middle_angle=0
  print (pID3)
  return int(pID3)

def AngleConvert(angle, middle_angle, flip):
  # 0~240° ————> 0~1000
  p = 500 + (angle - middle_angle) * 25 / 6
  if p < 0:
    p = 0
  elif p > 1000:
    p = 1000
  if flip: return 1000 - int(p)
  print(p)
  return int(p)

def distance(coordinate):
    # calculate distance between the object and the basement of the robot arm
    # return distance in mm
    X = coordinate[0]
    Y = coordinate[1]
    distance = math.sqrt(X**2 + Y**2)
    print(distance)
    return round(distance)

def ArmControl(distance, _time):
    angle = ArmIK.CalcAngle(X = coordinate[0], Y = coordinate[1], Z = coordinate[2])
    if distance>100:
        pID5 = AngleConvertID5_far(distance, 90)
        pID4 = AngleConvertID4_far(distance, 0)
        pID3 = AngleConvertID3_far(distance, 0)

    elif distance>200:
        pID5 = AngleConvertID5_close(distance, 90)
        pID4 = AngleConvertID4_close(distance, 0)
        pID3 = AngleConvertID3_close(distance, 0)
    else :
        return False
    bus_servo.run(6, AngleConvert(angle[0] , middle_angle=90, flip=False), _time)
    bus_servo.run(5, pID5, _time)
    bus_servo.run(4, pID4, _time)
    bus_servo.run(3, pID3, _time)
    bus_servo.run(2, 500, _time)
    bus_servo.run(1, 500, _time)
    return True

if __name__ == '__main__':
  while True:
    coor=[]
    coor.append(int(input("請輸入x座標: ")))
    coor.append(int(input("請輸入y座標: ")))
    coor.append(int(input("請輸入z座標: ")))
    run_action_group(bus_servo, action_groups_init)
    time.sleep_ms(100) 
    
    ArmControl(coor,2500) 
    time.sleep_ms(2500)