from machine import Pin, UART
from micropython import const
import time, ustruct


DEVICE_GAMEPAD        = const(0)
DEVICE_MOUSE1         = const(1)
DEVICE_MOUSE2         = const(2)



PSB_TRIANGLE 	= const(0x0001)
PSB_CIRCLE		= const(0x0002)
PSB_CROSS		  = const(0x0004)
PSB_SQUARE		= const(0x0008)

PSB_L1			  = const(0x0010)
PSB_R1 			  = const(0x0020)
PSB_L2 			  = const(0x0040)
PSB_R2 			  = const(0x0080)

PSB_SELECT 		= const(0x0100)
PSB_START 		= const(0x0200)
PSB_L3 			  = const(0x0400)
PSB_R3 			  = const(0x0800)

PSB_UP 			  = const(0x1000)
PSB_RIGHT 		= const(0x2000)
PSB_DOWN 		  = const(0x4000)
PSB_LEFT 		  = const(0x8000)
    
    
PSB_PRESS          = const(0x00000)
PSB_PRESS_UP       = const(0x80000)



class USBDevice:
  uart = UART(1, 9600, tx=10, rx=34)
  USBDeviceMsgs = []
  MouseMsgs = []
  GamepadMsgs = []
  gamepad_data_last = 0
  
  @staticmethod   
  def get_msg():
    
    frameStarted = False
    frameCount = 0
    dataCount = 0
    dataLength = 2
    rx_buf = [0x55]
    time_now = time.ticks_ms()
    
    while USBDevice.uart.any():
      
      buf = ustruct.unpack('B', USBDevice.uart.read(1))[0]

      if not frameStarted:
        if buf == 0x55:
          frameCount += 1
          if frameCount == 2:
            frameCount = 0
            frameStarted = True
            dataCount = 1
        else:
          return False
        
      if frameStarted:
        rx_buf.append(buf)
        if dataCount == 2:
          dataLength = rx_buf[dataCount]
          if dataLength < 2 or dataLength > 10:
            return False
        dataCount += 1
        if dataCount == dataLength + 2:
          USBDevice.USBDeviceMsgs.append(rx_buf)
          break
      if time.ticks_ms() - time_now > 100:
        return False
      

    if len(USBDevice.USBDeviceMsgs) > 0:
      return USBDevice.USBDeviceMsgs.pop(0)
    return False
  
  @staticmethod 
  def msg_convert(msg):
    bit7_0 = msg[5]
    bit11_8 = (msg[6] & 0x0F)<<8
    bit15_12 = 0
    if msg[7] == 0 or msg[9] == 0:
      bit15_12 |= PSB_UP
    elif msg[7] == 4 or msg[9] == 0xFF:
      bit15_12 |= PSB_DOWN
    if msg[7] == 6 or msg[8] == 0:
      bit15_12 |= PSB_LEFT
    elif msg[7] == 2 or msg[8] == 0xFF:
      bit15_12 |= PSB_RIGHT
    
    if bit7_0 & 0x0F == 0:
      if msg[11] == 0:
        bit7_0 |= PSB_TRIANGLE
      elif msg[11] == 0xFF:
        bit7_0 |= PSB_CROSS
      if msg[10] == 0:
        bit7_0 |= PSB_SQUARE
      elif msg[10] == 0xFF:
        bit7_0 |= PSB_CIRCLE
        
    return bit15_12 | bit11_8 | bit7_0
    
  @staticmethod 
  def run_loop():
    msg = USBDevice.get_msg()
    if msg == False:return
    if msg[4] == DEVICE_MOUSE1 or msg[4] == DEVICE_MOUSE2:
      USBDevice.MouseMsgs.append(msg)
    elif msg[4] == DEVICE_GAMEPAD:
      data = USBDevice.msg_convert(msg)
      if data != 0:
        USBDevice.gamepad_data_last = data
        USBDevice.GamepadMsgs.append(data | PSB_PRESS)
      else:
        USBDevice.GamepadMsgs.append(USBDevice.gamepad_data_last | PSB_PRESS_UP)
        USBDevice.gamepad_data_last = 0
        
  @staticmethod 
  def get_mouse_msg():
    try:
      return USBDevice.MouseMsgs.pop()
    except:
      return False
    
  @staticmethod 
  def get_gamepad_msg():
    try:
      return USBDevice.GamepadMsgs.pop()
    except:
      return False

  







