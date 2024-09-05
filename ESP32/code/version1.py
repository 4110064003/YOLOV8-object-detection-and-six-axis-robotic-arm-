from actions import action_groups
from BusServo import BusServo

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
  
  run_multiple_groups(b, action_groups)
    
  














