from machine import Pin, ADC, Timer
from micropython import const
import time, uctypes, gc
from BusServo import BusServo, have_got_servo_pos
#from PWMServo import PWMServo
import Hiwonder_wifi_ble as HW_wb
from RobotControl import RobotControl
from Buzzer import Buzzer
from Key import Key
from Led import LED
from USBDevice import *
   
print("Please wait...")
ble = HW_wb.Hiwonder_wifi_ble(HW_wb.MODE_BLE_SLAVE, name = 'xArm-esp32')
# ble = HW_wb.Hiwonder_wifi_ble(HW_wb.MODE_BLE_MASTER, name = 'xArm-esp32')
# ble = HW_wb.Hiwonder_wifi_ble(HW_wb.MODE_BROADCAST_SLAVE)
# ble = HW_wb.Hiwonder_wifi_ble(HW_wb.MODE_BROADCAST_MASTER)
# ble.ble_broadcast_group(0xff)
ble.set_led_key_io(led=4,key=13)

bus_servo = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)
Robot = RobotControl(bus_servo = bus_servo)

buzzer = Buzzer()
key = Key()
led = LED()

adc = ADC(Pin(39))
adc.atten(ADC.ATTN_11DB)


def MouseHandle():
  xy_max = 16
  BUTTON_L = 0x01
  BUTTON_R = 0x02
  BUTTON_M = 0x04
  
  msg = USBDevice.get_mouse_msg()
  if msg == False:
    return 
  
  mouse_msg = uctypes.struct(uctypes.addressof(bytes(msg))
            ,{"button": uctypes.UINT8 | 5,'move_X': uctypes.INT8 | 6
            , 'move_Y': uctypes.INT8 | 7,'wheel': uctypes.INT8 | 8})

  if mouse_msg.button & BUTTON_M != 0:
    Robot.runActionGroup('0.rob')
  if mouse_msg.wheel != 0:
    bus_servo.run_add_or_dec(1, 30*mouse_msg.wheel)
  else:
    if mouse_msg.move_X > xy_max:mouse_msg.move_X = xy_max
    if mouse_msg.move_X < -xy_max:mouse_msg.move_X = -xy_max
    if mouse_msg.move_Y > xy_max:mouse_msg.move_Y = xy_max
    if mouse_msg.move_Y < -xy_max:mouse_msg.move_Y = -xy_max
    
    if abs(mouse_msg.move_X) > abs(mouse_msg.move_Y):
      if mouse_msg.button & BUTTON_L != 0:
        bus_servo.run_add_or_dec(2, mouse_msg.move_X)
      elif mouse_msg.button & BUTTON_R != 0:
        bus_servo.run_add_or_dec(2, mouse_msg.move_X)
      else:
        bus_servo.run_add_or_dec(6, -mouse_msg.move_X//2)
    elif abs(mouse_msg.move_X) < abs(mouse_msg.move_Y):
      if mouse_msg.button & BUTTON_L != 0:
        bus_servo.run_add_or_dec(4, -mouse_msg.move_Y)
      elif mouse_msg.button & BUTTON_R != 0:
        bus_servo.run_add_or_dec(3, mouse_msg.move_Y)
      else:
        bus_servo.run_add_or_dec(5, mouse_msg.move_Y//2)
      
def _GamepadHandle():

  MODE_SINGLE_SERVO = 1
  MODE_ARTION_GROUP = 2
  mode = MODE_ARTION_GROUP
  
  which_button_press = 0
  time_last = 0
  speed = 5

  def fun():
    nonlocal MODE_SINGLE_SERVO
    nonlocal MODE_ARTION_GROUP
    nonlocal mode
    nonlocal which_button_press
    nonlocal time_last

    msg =  USBDevice.get_gamepad_msg()

    if msg == PSB_START | PSB_SELECT | PSB_PRESS:
      if mode == MODE_ARTION_GROUP:
        mode = MODE_SINGLE_SERVO
        buzzer.on()
        time.sleep_ms(50)
        buzzer.off()
      else:
        mode = MODE_ARTION_GROUP
        buzzer.on()
        time.sleep_ms(50)
        buzzer.off()
        time.sleep_ms(50)
        buzzer.on()
        time.sleep_ms(50)
        buzzer.off()
        
    if msg == PSB_START | PSB_PRESS:
      if mode == MODE_ARTION_GROUP:
        # bus_servo.run_mult((500, 500, 500, 500, 500, 500), 1000)
        Robot.runActionGroup('00.rob')
      elif mode == MODE_SINGLE_SERVO:
        bus_servo.run_mult((500,500,500,500,500,500),1000)
        have_got_servo_pos.clear()

    elif msg == PSB_UP | PSB_PRESS:
      if mode == MODE_ARTION_GROUP:Robot.runActionGroup('01.rob')
      elif mode == MODE_SINGLE_SERVO:which_button_press = msg
    
    elif msg == PSB_DOWN | PSB_PRESS:
      if mode == MODE_ARTION_GROUP:Robot.runActionGroup('02.rob')
      elif mode == MODE_SINGLE_SERVO:which_button_press = msg    
        
    elif msg == PSB_LEFT | PSB_PRESS:
      if mode == MODE_ARTION_GROUP:Robot.runActionGroup('03.rob')
      elif mode == MODE_SINGLE_SERVO:which_button_press = msg
    
    elif msg == PSB_RIGHT | PSB_PRESS:
      if mode == MODE_ARTION_GROUP:Robot.runActionGroup('04.rob')
      elif mode == MODE_SINGLE_SERVO:which_button_press = msg  
    
    elif msg == PSB_L2 | PSB_PRESS:
      if mode == MODE_ARTION_GROUP:Robot.runActionGroup('11.rob')
      elif mode == MODE_SINGLE_SERVO:which_button_press = msg
    
    elif msg == PSB_R2 | PSB_PRESS:
      if mode == MODE_ARTION_GROUP:Robot.runActionGroup('12.rob')
      elif mode == MODE_SINGLE_SERVO:which_button_press = msg
    
    elif msg == PSB_TRIANGLE | PSB_PRESS:
      if mode == MODE_ARTION_GROUP:Robot.runActionGroup('05.rob')
      elif mode == MODE_SINGLE_SERVO:which_button_press = msg
    
    elif msg == PSB_CROSS | PSB_PRESS:
      if mode == MODE_ARTION_GROUP:Robot.runActionGroup('06.rob')
      elif mode == MODE_SINGLE_SERVO:which_button_press = msg
    
    elif msg == PSB_SQUARE | PSB_PRESS:
      if mode == MODE_ARTION_GROUP:Robot.runActionGroup('07.rob')
      elif mode == MODE_SINGLE_SERVO:which_button_press = msg
    
    elif msg == PSB_CIRCLE | PSB_PRESS:
      if mode == MODE_ARTION_GROUP:Robot.runActionGroup('08.rob')
      elif mode == MODE_SINGLE_SERVO:which_button_press = msg
    
    elif msg == PSB_L1 | PSB_PRESS:
      if mode == MODE_ARTION_GROUP:Robot.runActionGroup('09.rob')
      elif mode == MODE_SINGLE_SERVO:which_button_press = msg
    
    elif msg == PSB_R1 | PSB_PRESS:
      if mode == MODE_ARTION_GROUP:Robot.runActionGroup('10.rob')
      elif mode == MODE_SINGLE_SERVO:which_button_press = msg
      
      
    elif msg & PSB_PRESS_UP == PSB_PRESS_UP:
      if mode == MODE_ARTION_GROUP:pass
      elif mode == MODE_SINGLE_SERVO:which_button_press = 0
      

    if mode == MODE_SINGLE_SERVO:
      if time.ticks_ms() - time_last > 25:
        time_last = time.ticks_ms()

        if which_button_press == PSB_UP | PSB_PRESS:
          bus_servo.run_add_or_dec(5, -speed)
        elif which_button_press == PSB_DOWN | PSB_PRESS:
          bus_servo.run_add_or_dec(5, speed)
        elif which_button_press == PSB_LEFT | PSB_PRESS:
          bus_servo.run_add_or_dec(6, speed)
        elif which_button_press == PSB_RIGHT | PSB_PRESS:
          bus_servo.run_add_or_dec(6, -speed)
        elif which_button_press == PSB_L2 | PSB_PRESS:
          bus_servo.run_add_or_dec(1, speed)
        elif which_button_press == PSB_R2 | PSB_PRESS:
          bus_servo.run_add_or_dec(1, -speed)
        elif which_button_press == PSB_TRIANGLE | PSB_PRESS:
          bus_servo.run_add_or_dec(4, speed)
        elif which_button_press == PSB_CROSS | PSB_PRESS:
          bus_servo.run_add_or_dec(4, -speed)
        elif which_button_press == PSB_SQUARE | PSB_PRESS:
          bus_servo.run_add_or_dec(3, -speed)
        elif which_button_press == PSB_CIRCLE | PSB_PRESS:
          bus_servo.run_add_or_dec(3, speed)
        elif which_button_press == PSB_L1 | PSB_PRESS:
          bus_servo.run_add_or_dec(2, -speed)
        elif which_button_press == PSB_R1 | PSB_PRESS:
          bus_servo.run_add_or_dec(2, speed)
          
  return fun    
GamepadHandle = _GamepadHandle()


ble_data = bytearray()
def ble_handle():
  global ble_data
  ble_data += ble.ble_read()
  # print(ble_data)
  if ble.mode == HW_wb.MODE_BROADCAST_SLAVE:
    for i in range(6):
      id = i+1
      pos = ble_data[i*2+2] | (ble_data[i*2+3] << 8)
      t = ble_data[0] | (ble_data[1] << 8)
      if pos >= 0 and pos <= 1000:
        bus_servo.run(id, pos, t)
      time.sleep_us(120)
    ble_data = bytearray()
  elif ble.mode == HW_wb.MODE_BLE_SLAVE:
    ble_data_len = len(ble_data)
    if ble_data_len >= 4:
      i = 0
      while i < ble_data_len:
        if ble_data[i] == 0x55 and ble_data[i+1] == 0x55:
          if ble_data_len - i < ble_data[i+2] + 2:
            ble_data = ble_data[i:]
            return
          data = ble_data[i:i+ble_data[i+2]+2]
          i +=  ble_data[i+2]+1

          cmd = data[3]
          if cmd == 0x03:#舵机角度控制
            servos_sum = data[4]
            t = data[5] | (data[6] << 8)
            for n in range(0,servos_sum):
              id = data[7+3*n]
              pos = data[8+3*n] | (data[9+3*n] << 8)
              bus_servo.run(id, pos, t)
              time.sleep_us(120)
          elif cmd == 0x06:#动作组运行
            action_num = data[4]
            times = data[5] | (data[6] << 8)
            if times == 0:times = 100000
            Robot.runActionGroup(str(action_num)+'.rob', times)
          elif cmd == 0x07:#动作组停止
            Robot.stopActionGroup()
          elif cmd == 0x14:#舵机掉电
            servos = data[5:data[4]+5]
            for i in servos:
              bus_servo.unload(i)
          elif cmd == 0x15:#APP读取舵机位置
            return_data=bytearray()
            servos = data[5:data[4]+5]
            for i in servos:
              p = bus_servo.get_position(i)
              if p == False:p = bus_servo.get_position(i)
              if p != False:
                if p < 0:p = 0
                elif p > 1000:p = 1000
                return_data += i.to_bytes(1,'little') + p.to_bytes(2,'little')
            return_data = b'\x55\x55' + (len(return_data)+3).to_bytes(1,'little') + b'\x15'\
                + (len(return_data)//3).to_bytes(1,'little') + return_data
            ble.ble_write(return_data)

        i += 1
      ble_data = bytearray()
ble.ble_rx_irq(ble_handle)

def _SyncHandle():
  time_last = 0
  pos_last = [0]*7
  def moveServo(i, pos, t):
    buf = bytearray(10)
    buf[0] = 0x55
    buf[1] = 0x55
    buf[2] = 8
    buf[3] = 3
    buf[4] = 1
    buf[5] = t & 0xFF
    buf[6] = (t>>8) & 0xFF
    buf[7] = i
    buf[8] = pos & 0xFF
    buf[9] = (pos>>8) & 0xFF
    ble.ble_write(buf)
  def moveServoBleBroadcast(pos, t=20):
    buf = bytearray(14)
    buf[0] = t & 0xFF
    buf[1] = (t >> 8) & 0xFF
    for i in range(6):
      buf[i*2+2] = pos[i] & 0xFF
      buf[i*2+3] = (pos[i] >> 8) & 0xFF
    ble.ble_write(buf)
  def fun():
    nonlocal time_last
    if ble.mode == HW_wb.MODE_BLE_MASTER:
      if time.ticks_ms() - time_last > 100:
        time_last = time.ticks_ms()
        for i in range(1,7):
          if ble.ble_isconnected():
            pos = bus_servo.get_position(i)
            if pos != False and pos >= 0 and pos <= 1000:
              if abs(pos_last[i] - pos) >= 2:
                pos_last[i] = pos
                moveServo(i, pos, 20)
    elif ble.mode == HW_wb.MODE_BROADCAST_MASTER:
      if time.ticks_ms() - time_last > 100:
        time_last = time.ticks_ms()
        send = False
        pos=[0]*6
        for i in range(6):
          p = bus_servo.get_position(i+1)
          if p == False or p < 0 or p > 1000:p = 65535
          pos[i] = p
          if abs(pos_last[i] - pos[i]) >= 2:
            pos_last[i] = pos[i]
            send = True
        if send:
          moveServoBleBroadcast(pos, t=200)

  return fun
  
SyncHandle = _SyncHandle()


def main(t):
  #在定时器中断中完成的，不要出现死循环和过大的延时函数
  
  gc.collect()
  key.run_loop()
  USBDevice.run_loop()
  Robot.run_loop()

  MouseHandle()
  GamepadHandle()
  SyncHandle()

  if key.down_up():
    Robot.runActionGroup('100.rob')
  if key.down_long():
    Robot.runActionGroup('100.rob',100000)

  if adc.read() / 4095 * 3.6 * 4 < 6:
    pass
    #buzzer.on()
  else:buzzer.off()


print("Start")
tim = Timer(2)
tim.init(period=10, mode=Timer.PERIODIC, callback=main)






















