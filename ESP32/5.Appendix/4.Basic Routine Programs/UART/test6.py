from BusServo import BusServo
from actions import action_groups
from initial_position import action_groups_init
from default_position import action_groups_default
from position_ato1_ import action_groups_ato1, action_groups_1toa
from position_ato2_ import action_groups_ato2, action_groups_2toa
from position_ato3_ import action_groups_ato3, action_groups_3toa
from position_ato4_ import action_groups_ato4, action_groups_4toa
from position_ato5_ import action_groups_ato5, action_groups_5toa
from position_ato6_ import action_groups_ato6, action_groups_6toa
from position_atob_ import action_groups_atob, action_groups_btoa
from position_bto1_ import action_groups_bto1, action_groups_1tob
from position_bto2_ import action_groups_bto2, action_groups_2tob
from position_bto3_ import action_groups_bto3, action_groups_3tob
from position_bto4_ import action_groups_bto4, action_groups_4tob
from position_bto6_ import action_groups_bto6, action_groups_6tob
from position_btoa_ import action_groups_btoa, action_groups_atob

def move_object_to_destination(b, action_group_to, action_group_from, object_label, destination_label):
    print(f"move object {object_label} to destination {destination_label}")
    run_multiple_groups(b, action_group_to)
    print(f"move destination {destination_label} to object {object_label}")
    run_multiple_groups(b, action_group_from)

def process_action_map(b, action_map, destination_coordinate, object_label, destination_label):
    for (x_min, x_max), y_conditions in action_map.items():
        if x_min < destination_coordinate[0] <= x_max:
            if y_conditions is None:
                print("Invalid x coordinate. Please enter lower destination x coordinate.")
                return False

            for (y_min, y_max), (move_to_group, move_back_group) in y_conditions:
                if y_min < destination_coordinate[1] <= y_max:
                    move_object_to_destination(b, move_to_group, move_back_group, object_label, destination_label)
                    return True

            print("Invalid y coordinate. Please enter a valid y coordinate.")
            return False

    print("Invalid x coordinate. Please enter a valid x coordinate.")
    return False

def ArmControl(destination_coordinate, object_coordinates, object_label, destination_label, _time):
    destination_coordinate[0] = -destination_coordinate[0]
    object_coordinates[0] = -object_coordinates[0]
    
    #映射表 action_map 字典,鍵為(x_min,x_max),值為y_conditions列表
    if object_coordinates[0]<0:
        action_map_a = {
            (20, float('inf')): None,
            (5, 20): [
                ((15, 27), (action_groups_ato3, action_groups_3toa)),
                ((1, 15), (action_groups_ato6, action_groups_6toa)),
                ((-15, 1), (action_groups_atob, action_groups_btoa)),
            ],
            (-8, 5): [
                ((15, 27), (action_groups_ato2, action_groups_2toa)),
                ((1, 15), (action_groups_ato5, action_groups_5toa)),
            ],
            (-23, -8): [
                ((15, 27), (action_groups_ato1, action_groups_1toa)),
                ((1, 15), (action_groups_ato4, action_groups_4toa)),
            ],
        }
        return process_action_map(b, action_map_a, destination_coordinate, object_label, destination_label)
        
    else :
        action_map_b = {
            (20, float('inf')): None,
            (5, 20): [
                ((15, 27), (action_groups_bto3, action_groups_3tob)),
                ((1, 15), (action_groups_bto6, action_groups_6tob)),
            ],
            (-8, 5): [
                ((15, 27), (action_groups_bto2, action_groups_2tob)),
                #((1, 15), (action_groups_bto5, action_groups_5tob)),
            ],
            (-23, -8): [
                ((15, 27), (action_groups_bto1, action_groups_1tob)),
                ((1, 15), (action_groups_bto4, action_groups_4tob)),
                ((-15, 1), (action_groups_btoa, action_groups_atob)),
            ],
        }
        return process_action_map(b, action_map_b, destination_coordinate, object_label, destination_label)

if __name__ == '__main__':
    b = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)

    while True:
        object_input = input("object_label (space) x_coor (space) y_coor: ")
        destination_input = input("destination_label (space) x_coor (space) y_coor: ")

        object_list = object_input.split()
        destination_list = destination_input.split()

        object_label = object_list[0]
        destination_label = destination_list[0]

        object_coordinates = list(map(float, object_list[1:]))
        destination_coordinates = list(map(float, destination_list[1:]))

        time.sleep_ms(1000)
        ArmControl(destination_coordinates, object_coordinates, object_label, destination_label, 2500)
        time.sleep_ms(1000)


