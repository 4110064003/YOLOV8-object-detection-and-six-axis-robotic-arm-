#1~6+a,b
from BusServo import BusServo
from actions import action_groups
from initial_position import action_groups_init
from default_position import action_groups_default
#from action_generate import generate_action_group
from position_ato1_ import action_groups_ato1
from position_ato1_ import action_groups_1toa
from position_ato2_ import action_groups_ato2
from position_ato2_ import action_groups_2toa
from position_ato3_ import action_groups_ato3
from position_ato3_ import action_groups_3toa
from position_ato4_ import action_groups_ato4
from position_ato4_ import action_groups_4toa
from position_ato5_ import action_groups_ato5
from position_ato5_ import action_groups_5toa
from position_ato6_ import action_groups_ato6
from position_ato6_ import action_groups_6toa
from position_atob_ import action_groups_atob
from position_atob_ import action_groups_btoa
import time
import ustruct 

def run_multiple_groups(BusServo, action_group):
    for group in action_group:
      for action in group:
        servo_id = action['id']
        position = action['position']
        run_time = action['time']

        BusServo.run(servo_id, position, run_time)
        
      max_time = max(action['time'] for action in group)
      time.sleep(max_time / 1000.0)  

def ArmControl(coordinate,_time):
    #X = coordinate[0], Y = coordinate[1], Z = coordinate[2]
    #X, Y, Z = coordinate[0], coordinate[1], coordinate[2]
    coordinate[0]=-coordinate[0]
    #coordinate[2]=-coordinate[2]
    if coordinate[0]>20:
        print ("please enter lower value of x")
    elif coordinate[0]>=5:
        if coordinate[1]>27:
            print("please enter lower value of y")
        elif coordinate[1]>=15:
            print("move from position a->3")
            run_multiple_groups(b, action_groups_ato3)
            print("move from position 3->a")
            run_multiple_groups(b, action_groups_3toa)
        elif coordinate[1]>=1:
            print("move from position a->6")
            run_multiple_groups(b, action_groups_ato6)
            print("move from position 6->a")
            run_multiple_groups(b, action_groups_6toa)
        elif coordinate[1]>=-15:
            print("move from position a->b")
            run_multiple_groups(b, action_groups_atob)
            print("move from position b->a")
            run_multiple_groups(b, action_groups_btoa)
        else:
            print("please enter higher value of y")
    elif coordinate[0]>=-8:
        if coordinate[1]>27:
            print("please enter lower value of y")
        elif coordinate[1]>=15:
            print("move from position a->2")
            run_multiple_groups(b, action_groups_ato2)
            print("move from position 2->a")
            run_multiple_groups(b, action_groups_2toa)
        elif coordinate[1]>=1:
            print("move from position a->5")
            run_multiple_groups(b, action_groups_ato5)
            print("move from position 5->a")
            run_multiple_groups(b, action_groups_5toa)
        else:
            print("please enter higher value of y")
    elif coordinate[0]>-23:
        if coordinate[1]>27:
            print("please enter lower value of y")
        elif coordinate[1]>=15:
            print("move from position a->1")
            run_multiple_groups(b, action_groups_ato1)
            print("move from position 1->a")
            run_multiple_groups(b, action_groups_1toa)
        elif coordinate[1]>=1:
            print("move from position a->4")
            run_multiple_groups(b, action_groups_ato4)
            print("move from position 4->a")
            run_multiple_groups(b, action_groups_4toa)
        else:

            print("please enter higher value of y")
    else:
        print ("please enter higher value of x")
    return True          
                 
 
if __name__ == '__main__':
  b = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)
  
  while True:
    coor=[]
    coor.append(int(input("請輸入x座標:")))
    coor.append(int(input("請輸入y座標:")))
    #coor.append(int(input("請輸入z座標:")))
    #run_action_group(bus_servo,action_group_init)
    time.sleep_ms(1000)

    ArmControl(coor,2500)
    time.sleep_ms(2500)











