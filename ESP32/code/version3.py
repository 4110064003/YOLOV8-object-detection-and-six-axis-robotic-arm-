#將操作範圍以九宮的方式劃分為編號1~6的區塊以及a、b 區塊，根據輸入指令操控手臂運行動作組，夾取方塊制止定點擺放
# 1 2 3
# 4 5 6
# a R b
from BusServo import BusServo
from actions import action_groups
from default_position import action_groups_default
#from action_generate import generate_action_group
from position_ato1_ import action_groups_ato1
from position_ato2_ import action_groups_ato2
from position_ato3_ import action_groups_ato3
from position_ato4_ import action_groups_ato4
from position_ato5_ import action_groups_ato5
from position_ato6_ import action_groups_ato6
import time 

def run_multiple_groups(BusServo, action_group):
    for group in action_group:
      for action in group:
        servo_id = action['id']
        position = action['position']
        run_time = action['time']

        BusServo.run(servo_id, position, run_time)
        
      max_time = max(action['time'] for action in group)
      time.sleep(max_time / 1000.0)  
        
 
if __name__ == '__main__':
  b = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)
  
  while True:
    place = str(input("請輸入想移動到的位置: "))
    if place == "a1":
      run_multiple_groups(b, action_groups_ato1)
      print("move from position a->1")
    elif place =="a2":
      run_multiple_groups(b, action_groups_ato2)
      print("move from position a->2")
    elif place =="a3":
      run_multiple_groups(b, action_groups_ato3)
      print("move from position a->3")
    elif place =="a4":
      run_multiple_groups(b, action_groups_ato4)
      print("move from position a->4")
    elif place =="a5":
      run_multiple_groups(b, action_groups_ato5)
      print("move from position a->5")
    elif place =="a6":
      run_multiple_groups(b, action_groups_ato6)
      print("move from position a->6")
    else:
      run_multiple_groups(b, action_groups_default)
      print("!please enter a valid position!")

    will = input("Do you want to continue? (yes/no): ").strip().lower()
      
    if will != 'yes':
      print("Exiting program.")
      break   
  # if __name__ == '__main__':
    # b = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)
    # 
    # while True:
        # place = str(input("請輸入想移動到的位置: "))
        # if place in ["4", "6"]:
            # action_group = generate_action_group(place)
            # run_multiple_groups(b, [action_group])
            # print(f"move from position a->{place}")
        # else:
            # run_multiple_groups(b, action_groups_default)
            # print("!please enter a valid position!")
# 
        # will = input("Do you want to continue? (yes/no): ").strip().lower()
        # if will != 'yes':
            # print("Exiting program.")
            # break
























