from actions import action_groups
from BusServo import BusServo
from initial_position import action_groups_init
import ArmInversekinematics as ArmIK
import time
import math
import random

class ArmController:
	def __init__(self, tx=26, rx=35, tx_en=25, rx_en=12):
		self.bus_servo = BusServo(tx=tx, rx=rx, tx_en=tx_en, rx_en=rx_en)

	def convert_input_to_arm_coordinates(self, input_x, input_y):
		arm_y = input_y+200
		arm_x = input_x+200
		
		print("Converted Coordinate:X={},Y={}".format(arm_x,arm_y))
		return arm_x,arm_y
	
	# Function to run servo actions
	def run_action_group(bus_servo, action_groups_init):
		for action in action_groups_init:
			servo_id = action['id']
			position = action['position']
			run_time = action['time']
			bus_servo.run(servo_id, position, run_time)
		max_time = max(action['time'] for action in action_groups_init)
		time.sleep(max_time / 1000.0)
	
	# Unified function for angle conversion for ID3~ID5
	def angle_convert(distance,start_num,middle_angle, factor, offset,sign,constant):
		angle = start_num + factor * (distance - offset)
		print("the angle of servo is", angle)
		p = 500 + sign * (angle - middle_angle) * 25 / 6 + int(constant)
		p = max(0, min(1000, p))
		print("the p of servo is", p)
		return int(p)
		
	# Unified function for angle conversion for ID6   
	def AngleConvert(angle, middle_angle):
		p = 500 + (angle - middle_angle) * 25 / 6
		p = max(0, min(1000, p))
		print("the p of id6 is:", p)
		return int(p)
		
	# Calculate distance between the object and the base of the robot arm
	def calculate_distance(coordinate):
		x, y = coordinate[0], coordinate[1]
		distance = math.sqrt(x ** 2 + y ** 2)
		print("the distance between object and robot is: ", distance)
		return round(distance)
	
	# Control the arm based on distance
	def GoToObject(pID1, coordinate, _time):
		dist = calculate_distance(coordinate)
		angle = ArmIK.CalcAngle(X=coordinate[0], Y=coordinate[1], Z=coordinate[2])
		if angle == False:
			print("Distance out of range")
			return False, 0
		
		# define different distance range parameters combination
		# writen in dictionary
		parameters = [
			(100, 155, {"pID5": (90, 90, 0.3, 100, -1, 0), "pID4": (90, 0, -0.4, 100, 1, 0), "pID3": (90, 0, -0.16, 100, -1, 0)}),
			(155, 170, {"pID5": (120, 90, 0.2, 200, -1, 0), "pID4": (50, 0, -0.2, 200, 1, 0), "pID3": (90, 0, -0.04, 100, -1, 0)}),
			(170, 190, {"pID5": (120, 90, 0.2, 200, -1, 0), "pID4": (50, 0, -0.2, 200, 1, 0), "pID3": (90, 0, -0.1, 100, -1, 0)}),
			(190, 230, {"pID5": (120, 90, 0.2, 200, -1, 5), "pID4": (50, 0, -0.2, 200, 1, 0), "pID3": (90, 0, -0.13, 100, -1, 0)}),
			(230, 260, {"pID5": (120, 90, 0.2, 200, -1, -5), "pID4": (50, 0, -0.2, 200, 1, 0), "pID3": (90, 0, -0.17, 100, -1, 0)}),
			(260, 290, {"pID5": (120, 90, 0.2, 200, -1, -5), "pID4": (50, 0, -0.2, 200, 1, 0), "pID3": (90, 0, -0.19, 100, -1, 0)}),
			(290, 310, {"pID5": (120, 90, 0.2, 200, -1, -13), "pID4": (50, 0, -0.2, 200, 1, 0), "pID3": (90, 0, -0.21, 100, -1, 0)}),
			(310, 330, {"pID5": (120, 90, 0.2, 200, -1, -30), "pID4": (50, 0, -0.2, 200, 1, 0), "pID3": (90, 0, -0.26, 100, -1, 0)})
		]
		
		# choosing the param_set base on distance between object and base of robotArm
		selected_params = None
		for min_dist, max_dist, param_set in parameters:
			if min_dist < dist <= max_dist:
				selected_params = param_set
				break
		
		if selected_params is None:
			print("Distance out of range")
			return False, 0
		
		pID5 = angle_convert(dist, *selected_params["pID5"])
		pID4 = angle_convert(dist, *selected_params["pID4"])
		pID3 = angle_convert(dist, *selected_params["pID3"])

		# control the server 
		bus_servo.run(6, AngleConvert(angle[0], middle_angle=90), _time)
		bus_servo.run(5, int(pID5), _time)
		bus_servo.run(4, int(pID4), _time)
		bus_servo.run(3, int(pID3), _time)
		bus_servo.run(2, 500, _time)
		bus_servo.run(1, int(pID1), _time)
		
		return True, pID5

	def Grab(pID5_value, _time):
		#bus_servo.run(1, 200, _time)
		time.sleep_ms(1000)
		bus_servo.run(1, 600, _time)
		time.sleep_ms(1500)
		bus_servo.run(5, int(pID5_value)+50, _time)

	def Release(pID5_value, _time):
		#bus_servo.run(5, int(pID5_value)+20, _time)
		time.sleep_ms(1000)
		# bus_servo.run(5, int(pID5_value), _time)
		# time.sleep_ms(1500)
		#bus_servo.run(5, int(pID5_value), _time)
		bus_servo.run(1, 200, _time)
		time.sleep_ms(1500)
		print("Initializing position")
		run_action_group(bus_servo, action_groups_init)
		time.sleep_ms(100)
		
	def execute_arm_sequence(self,object_label,destination_label, object_coordinates, destination_coordinates):
		
		print("Initializing position")
        run_action_group(bus_servo, action_groups_init)
        time.sleep_ms(100)
		
		print("moving toward object {}".format(object_label))
		success, pID5_value = GoToObject(200, object_coordinates, 2500)
		time.sleep_ms(2500)
        Grab(pID5_value, 800)
        time.sleep_ms(2500)
		
		print("move object {} to destination {}".format(object_label, destination_label))
		angle = ArmIK.CalcAngle(X=coordinate2[0], Y=coordinate2[1], Z=coordinate2[2])
        bus_servo.run(6, AngleConvert(angle[0], middle_angle=90), 1000)
        time.sleep_ms(3500)
        success, pID5_value = GoToObject(600, coordinate2, 2500)
        time.sleep_ms(2500)
        Release(pID5_value, 800)
        time.sleep_ms(2500)
