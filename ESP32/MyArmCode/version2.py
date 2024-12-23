from BusServo import BusServo
from actions import action_groups
from default_position import action_groups_default
from position1to1 import action_groups_1to1
from position1to2 import action_groups_1to2
from position2to1 import action_groups_2to1
from position2to2 import action_groups_2to2

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
    place = int(input("請輸入想移動到的位置: "))
    if place == 11:
      run_multiple_groups(b, action_groups_1to1)
      print("move from position 1->1")
    elif place == 12:
      run_multiple_groups(b, action_groups_1to2)
      print("move from position 1->2")
    elif place == 21:
      run_multiple_groups(b, action_groups_2to1)
      print("move from position 2->1")
    elif place == 22:
      run_multiple_groups(b, action_groups_2to2)
      print("move from position 2->2")
    else:
      run_multiple_groups(b, action_groups_default)
      print("!please enter a valid position!")

    will = input("Do you want to continue? (yes/no): ").strip().lower()
      
    if will != 'yes':
      print("Exiting program.")
      break   
  
















