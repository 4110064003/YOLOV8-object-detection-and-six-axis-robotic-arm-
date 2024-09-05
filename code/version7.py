from BusServo import BusServo
import time
#運行動作組
def run_multiple_groups(BusServo, action_group):
    for group in action_group:
      for action in group:
        servo_id = action['id']
        position = action['position']
        run_time = action['time']

        BusServo.run(servo_id, position, run_time)
        
      max_time = max(int(action['time']) for action in group)  # Convert to int if necessary
      time.sleep(max_time / 1000.0)
#將方塊夾取至目的地後再夾回出發點      
def move_object_to_destination(b, action_group_to, action_group_from, object_label, destination_label):
    print("move object {} to destination {}".format(object_label, destination_label))
    run_multiple_groups(b, action_group_to)
    print("move object back to origin position")
    run_multiple_groups(b, action_group_from)
#根據模組名稱動態加載指定的動作組   
def load_action_groups(module_name,group_name):
    module = __import__(module_name)
    return getattr(module, group_name)
#設計映射表，根據坐標範圍來選擇正確的動作組
def process_action_map(b, action_map, destination_coordinate, object_label, destination_label):
    for (x_min, x_max), y_conditions in action_map.items():
        if x_min < destination_coordinate[0] <= x_max:
            if y_conditions is None:
              print("Invalid x coordinate. Please enter lower destination x coordinate.")
              return False

            for (y_min, y_max), ((to_module, to_group), (from_module, from_group)) in y_conditions:
                if y_min < destination_coordinate[1] <= y_max:
                  move_to_group = load_action_groups(to_module,to_group)
                  move_back_group = load_action_groups(from_module,from_group)
                  move_object_to_destination(b, move_to_group, move_back_group, object_label, destination_label)
                  return True

            print("Invalid y coordinate. Please enter a valid y coordinate.")
            return False

    print("Invalid x coordinate. Please enter a valid x coordinate.")
    return False
    

#對應座標所執行的動作組判斷
def ArmControl(destination_coordinate, object_coordinates, object_label, destination_label, _time):
    destination_coordinate[0] = -destination_coordinate[0]
    object_coordinates[0] = -object_coordinates[0]
    
    #映射表 action_map 字典,鍵為(x_min,x_max),值為y_conditions列表
    if object_coordinates[0]<-8:
      action_map_a = {
        (20, 100): None,#float('int')表示Python中無窮大的特殊浮點數(20, +∞)
        (5, 20): [
            ((15, 27), (("position_ato3_", "action_groups_ato3"), ("position_ato3_", "action_groups_3toa"))),
            ((1, 15), (("position_ato6_", "action_groups_ato6"), ("position_ato6_", "action_groups_6toa"))),
            ((-15, 1), (("position_atob_", "action_groups_atob"), ("position_atob_", "action_groups_btoa"))),
        ],
        (-8, 5): [
            ((15, 27), (("position_ato2_", "action_groups_ato2"), ("position_ato2_", "action_groups_2toa"))),
            ((1, 15), (("position_ato5_", "action_groups_ato5"), ("position_ato5_", "action_groups_5toa"))),
        ],
        (-23, -8): [
            ((15, 27), (("position_ato1_", "action_groups_ato1"), ("position_ato1_", "action_groups_1toa"))),
            ((1, 15), (("position_ato4_", "action_groups_ato4"), ("position_ato4_", "action_groups_4toa"))),
        ],
      }
      return process_action_map(b, action_map_a, destination_coordinate, object_label, destination_label)
    
    elif object_coordinates[0]>5:
      action_map_b = {
        (20, 100): None,
        (5, 20): [
            ((15, 27), (("position_bto3_", "action_groups_bto3"), ("position_bto3_", "action_groups_3tob"))),
            ((1, 15), (("position_bto6_", "action_groups_bto6"), ("position_bto6_", "action_groups_6tob"))),
        ],
        (-8, 5): [
            ((15, 27), (("position_bto2_", "action_groups_bto2"), ("position_bto2_", "action_groups_2tob"))),
            #((1, 15), (action_groups_bto5, action_groups_5tob)),
        ],
        (-23, -8): [
            ((15, 27), (("position_bto1_", "action_groups_bto1"), ("position_bto1_", "action_groups_1tob"))),
            ((1, 15), (("position_bto4_", "action_groups_bto4"), ("position_bto4_", "action_groups_4tob"))),
            ((-15, 1), (("position_btoa_", "action_groups_b2a"), ("position_btoa_", "action_groups_a2b"))),
        ],
      }
      return process_action_map(b, action_map_b, destination_coordinate, object_label, destination_label)
    
    else:
      action_map_2 = {
        (20, 100): None,
        (5, 20): [
            ((15, 27), (("position_2to3_", "action_groups_2to3"), ("position_2to3_", "action_groups_3to2"))),
            ((1, 15), (("position_2to6_", "action_groups_2to6"), ("position_2to6_", "action_groups_6to2"))),
            ((-15, 1), (("position_2tob_", "action_groups_b22"), ("position_2tob_", "action_groups_22b"))),
        ],
        (-23, -8): [
            ((15, 27), (("position_2to1_", "action_groups_2to1"), ("position_2to1_", "action_groups_1to2"))),
            ((1, 15), (("position_2to4_", "action_groups_2to4"), ("position_2to4_", "action_groups_4to2"))),
            ((-15, 1), (("position_2toa_", "action_groups_22a"), ("position_2toa_", "action_groups_a22"))),
        ],
      }
      return process_action_map(b, action_map_2, destination_coordinate, object_label, destination_label)

#主程式
if __name__ == '__main__':
    b = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)

    while True:
      object_input = input("object_label (space) x_coor (space) y_coor: ")
      destination_input = input("destination_label (space) x_coor (space) y_coor: ")

      object_list = object_input.split()
      destination_list = destination_input.split()

      object_label = object_list[0]
      destination_label = destination_list[0]

      object_coordinates = list(map(int, object_list[1:]))
      destination_coordinates = list(map(int, destination_list[1:]))
      time.sleep_ms(1000)
      
      ArmControl(destination_coordinates, object_coordinates, object_label, destination_label, 2500)
      time.sleep_ms(1000)
