from actions import action_groups
from BusServo import BusServo
from initial_position import action_groups_init
import ArmInversekinematics as ArmIK
import time, ustruct

bus_servo = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)

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

  print(p)
  if p < 0:
    p = 0
  elif p > 1000:
    p = 1000
  if flip: return 1000 - int(p)
  #print(p)
  return int(p)
 
def ArmControl(coordinate, _time):
  if(coordinate[0]==0):
    bus_servo.run(6, 500, middle_angle=90, flip=False), _time)
    bus_servo.run(5, 450, middle_angle=90, flip=True), _time)
    bus_servo.run(4, 800, middle_angle=0, flip=False), _time)
    bus_servo.run(3, 150, middle_angle=0, flip=True), _time)
    bus_servo.run(2, 500, _time)
    bus_servo.run(1, 700, 2000)
  print(angle)
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
