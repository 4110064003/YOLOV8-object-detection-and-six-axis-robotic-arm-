#置中
base_action_group_1= [
    {'id': 1, 'position': 300, 'time': 1000},  
    {'id': 2, 'position': 500, 'time': 1000},  
    {'id': 3, 'position': 300, 'time': 1000},  
    {'id': 4, 'position': 900, 'time': 1000},  
    {'id': 5, 'position': 700, 'time': 1000},  
    {'id': 6, 'position': 500, 'time': 1000}   
]
#a上張
base_action_group_2= [
    {'id': 1, 'position': 300, 'time': 1000},
    {'id': 2, 'position': 500, 'time': 1000},
    {'id': 3, 'position': 150, 'time': 1000},
    {'id': 4, 'position': 800, 'time': 1000},
    {'id': 5, 'position': 450, 'time': 1000},
    {'id': 6, 'position': 800, 'time': 1000}
]
#a上抓
base_action_group_3= [
    {'id': 1, 'position': 600, 'time': 1000},
    {'id': 2, 'position': 500, 'time': 1000},
    {'id': 3, 'position': 150, 'time': 1000},
    {'id': 4, 'position': 800, 'time': 1000},
    {'id': 5, 'position': 450, 'time': 1000},
    {'id': 6, 'position': 800, 'time': 1000}
]
initialization_actions = [base_action_group_1, base_action_group_2,base_action_group_3,base_action_group_1]

import copy

def generate_action_group(position):
  if position in ["4", "6"]:
    
    action_group_grab = copy.deepcopy(base_action_group_1)#使用深複製避免修改一個列表時影響到另一個列表
    action_group_grab[0]['position'] = 600
    action_group_grab[2]['position'] = 200
    action_group_grab[3]['position'] = 750
    action_group_grab[4]['position'] = 400
    
    action_group_put = copy.deepcopy(action_group_grab)#使用深複製避免修改一個列表時影響到另一個列表
    action_group_put[0]['position'] = 300
    
    if position =="4":
      action_group_grab[5]['position'] = 680  
      return [initialization_actions,action_group_grab,action_group_put,base_action_group_1]
      
    else:  
      action_group_grab[5]['position'] = 300 
      return [initialization_actions,action_group_grab,action_group_put,base_action_group_1]  


# Example usage:
#action_group_ato4 = generate_action_group("4")
#action_group_ato6 = generate_action_group("6")

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


