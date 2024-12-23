#1~6+a,b
from BusServo import BusServo
from actions import action_groups
from default_position import action_groups_default
from action_generate import generate_action_group
import time 
import copy

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
      if place in ["4", "6"]:
          action_group = generate_action_group(place)
          run_multiple_groups(b, [action_group])
          print("move from position a->{place}")
      else:
          run_multiple_groups(b, action_groups_default)
          print("!please enter a valid position!")

      will = input("Do you want to continue? (yes/no): ").strip().lower()
      if will != 'yes':
          print("Exiting program.")
          break

