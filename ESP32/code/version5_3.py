#將操作範圍以九宮的方式劃分為編號1~6的區塊以及a、b 區塊，
#夾取方塊至指定點擺放之後，沿原路徑夾回初始位置放置
#輸入值加入物件名稱，分別為相機檢測到數字目標板(類別名稱)(中心點的相機座標值)、方塊(類別名稱)(中心點的相機座標值)，
#將擺放在指定區域(區域a或區域b)的不同顏色方塊(紅色或藍色或綠色)移動至目標數字板所在區域。

#括弧中的數字為x、y方向邊界值、R為手臂放置位置
#(27)----------------------
# |   1   |   2   |   3   |
#(15)----------------------
# |   4   |   5   |   6   |
#(1)-----------------------
# |   a   |   R   |   b   |
#(-23)  (-8)     (5)    (20)

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

from position_bto1_ import action_groups_bto1
from position_bto1_ import action_groups_1tob
from position_bto2_ import action_groups_bto2
from position_bto2_ import action_groups_2tob
from position_bto3_ import action_groups_bto3
from position_bto3_ import action_groups_3tob
from position_bto4_ import action_groups_bto4
from position_bto4_ import action_groups_4tob
#from position_bto5_ import action_groups_bto5
#from position_bto5_ import action_groups_5tob
from position_bto6_ import action_groups_bto6
from position_bto6_ import action_groups_6tob
from position_btoa_ import action_groups_btoa
from position_btoa_ import action_groups_atob

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

def ArmControl(destination_coordinate,object_coordinates,object_label,destination_label,_time):
    destination_coordinate[0]=-destination_coordinate[0]
    object_coordinates[0]=-object_coordinates[0]
    if object_coordinates[0]>0:
      if destination_coordinate[0]>20:
          print ("please enter lower destination xcoor")
      elif destination_coordinate[0]>=5:
          if destination_coordinate[1]>27:
              print("please enter lower destination ycoor")
          elif destination_coordinate[1]>=15:
              print("move  object{object_label} to destination{destination_label}")
              run_multiple_groups(b, action_groups_ato3)
              print("move  destination{destination_label} to object{object_label}")
              run_multiple_groups(b, action_groups_3toa)
          elif destination_coordinate[1]>=1:
              print("move  object{object_label} to destination{destination_label}")
              run_multiple_groups(b, action_groups_ato6)
              print("move  destination{destination_label} to object{object_label}")
              run_multiple_groups(b, action_groups_6toa)
          elif destination_coordinate[1]>=-15:
              print("move  object{object_label} to destination{destination_label}")
              run_multiple_groups(b, action_groups_atob)
              print("move  destination{destination_label} to object{object_label}")
              run_multiple_groups(b, action_groups_btoa)
          else:
              print("please enter higher destination ycoor")
      elif destination_coordinate[0]>=-8:
          if destination_coordinate[1]>27:
              print("please enter lower value of y")
          elif destination_coordinate[1]>=15:
              print("move  object{object_label} to destination{destination_label}")
              run_multiple_groups(b, action_groups_ato2)
              print("move  destination{destination_label} to object{object_label}")
              run_multiple_groups(b, action_groups_2toa)
          elif destination_coordinate[1]>=1:
              print("move  object{object_label} to destination{destination_label}")
              run_multiple_groups(b, action_groups_ato5)
              print("move  destination{destination_label} to object{object_label}")
              run_multiple_groups(b, action_groups_5toa)
          else:
              print("please enter higher destination ycoor")
      elif destination_coordinate[0]>-23:
          if destination_coordinate[1]>27:
              print("please enter lower destination ycoor")
          elif destination_coordinate[1]>=15:
              print("move  object{object_label} to destination{destination_label}")
              run_multiple_groups(b, action_groups_ato1)
              print("move  destination{destination_label} to object{object_label}")
              run_multiple_groups(b, action_groups_1toa)
          elif destination_coordinate[1]>=1:
              print("move  object{object_label} to destination{destination_label}")
              run_multiple_groups(b, action_groups_ato4)
              print("move  destination{destination_label} to object{object_label}")
              run_multiple_groups(b, action_groups_4toa)
          else:
              print("please enter higher destination ycoor")
      else:
          print ("please enter higher destination xcoor")
      return True
      
    else:
      if destination_coordinate[0]>20:
          print ("please enter lower destination xcoor")
      elif destination_coordinate[0]>=5:
          if destination_coordinate[1]>27:
              print("please enter lower destination ycoor")
          elif destination_coordinate[1]>=15:
              print("move  object{object_label} to destination{destination_label}")
              run_multiple_groups(b, action_groups_bto3)
              print("move  destination{destination_label} to object{object_label}")
              run_multiple_groups(b, action_groups_3tob)
          elif destination_coordinate[1]>=1:
              print("move  object{object_label} to destination{destination_label}")
              run_multiple_groups(b, action_groups_bto6)
              print("move  destination{destination_label} to object{object_label}")
              run_multiple_groups(b, action_groups_6tob)
          else:
              print("please enter higher destination ycoor")
      elif destination_coordinate[0]>=-8:
          if destination_coordinate[1]>27:
              print("please enter lower destination ycoor")
          elif destination_coordinate[1]>=15:
              print("move  object{object_label} to destination{destination_label}")
              run_multiple_groups(b, action_groups_bto2)
              print("move  destination{destination_label} to object{object_label}")
              run_multiple_groups(b, action_groups_2tob)
          else:
              print("please enter higher destination ycoor")
      elif destination_coordinate[0]>-23:
          if destination_coordinate[1]>27:
              print("please enter lower destination ycoor")
          elif destination_coordinate[1]>=15:
              print("move  object{object_label} to destination{destination_label}")
              run_multiple_groups(b, action_groups_bto1)
              print("move  destination{destination_label} to object{object_label}")
              run_multiple_groups(b, action_groups_1tob)
          elif destination_coordinate[1]>=1:
              print("move  object{object_label} to destination{destination_label}")
              run_multiple_groups(b, action_groups_bto4)
              print("move  destination{destination_label} to object{object_label}")
              run_multiple_groups(b, action_groups_4tob)
          elif destination_coordinate[1]>=-15:
              print("move  object{object_label} to destination{destination_label}")
              run_multiple_groups(b, action_groups_btoa)
              print("move  destination{destination_label} to object{object_label}")
              run_multiple_groups(b, action_groups_btoa)
          else:
              print("please enter higher destination ycoor")
      else:
          print ("please enter higher destination xcoor")
      return True    
                 
if __name__ == '__main__':
  b = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)
   
  while True:

    object = input(" object_label (space) x_coor (space) y_coor (space) ")#請根據最上方提供的邊界值輸入x座標
    destination = input(" destination_label (space) x_coor (space) y_coor (space) ")#請根據最上方提供的邊界值輸入y座標

    object_list = object.split()
    destination_list = destination.split()

    object_label = object_list[0]
    destination_label = destination_list[0]

    object_coordinates = list(map(float,object_list[1:]))
    destination_coordinates = list(map(float,destination_list[1:]))

    time.sleep_ms(1000)
    ArmControl(destination_coordinates,object_coordinates,object_label,destination_label,2500)
    time.sleep_ms(2500)

   














