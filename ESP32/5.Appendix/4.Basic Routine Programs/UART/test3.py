#1~6+a,b
from BusServo import BusServo
from actions import action_groups
from default_position import action_groups_default
from position_ato1_ import action_groups_ato1
from position_ato2_ import action_groups_ato2
from position_ato3_ import action_groups_ato3


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
      print("move from position 1->1")
    elif place =="a2":
      run_multiple_groups(b, action_groups_ato2)
      print("move from position 1->2")
    elif place =="a3":
      run_multiple_groups(b, action_groups_ato3)
      print("move from position 2->1")
    else:
      run_multiple_groups(b, action_groups_default)
      print("!please enter a valid position!")

    will = input("Do you want to continue? (yes/no): ").strip().lower()
      
    if will != 'yes':
      print("Exiting program.")
      break   
  
















