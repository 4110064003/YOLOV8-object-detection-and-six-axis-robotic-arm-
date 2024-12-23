from machine import Pin,UART
from micropython import const
import time, ustruct
from actions import action_groups


SERVO_MOVE_TIME_WRITE       = const(1)
SERVO_MOVE_TIME_READ        = const(2)
SERVO_POS_READ              = const(28)
SERVO_MOVE_STOP             = const(12)
SERVO_ID_WRITE              = const(13)
SERVO_ID_READ               = const(14)

SERVO_ANGLE_OFFSET_ADJUST   = const(17)
SERVO_ANGLE_OFFSET_WRITE    = const(18)
SERVO_ANGLE_OFFSET_READ     = const(19)

SERVO_VIN_READ              = const(27)
SERVO_OR_MOTOR_MODE_WRITE   = const(29)
SERVO_LOAD_OR_UNLOAD_WRITE  = const(31)

have_got_servo_pos = {}

def get_low8_byte(data):
  return (data & 0xFF)

def get_high8_byte(data):
  return ((data>>8) & 0xFF)
  
def byte_to_hw(a, b):
  return (a | (b << 8))
  
  
class BusServo:
  def __init__(self, tx, rx, tx_en = None, rx_en = None):
    self.rx_buf = [0x55]
    self.isAutoEnableRT = False
    if tx_en == None:
      self.isAutoEnableRT = True
      
    if self.isAutoEnableRT == False:
      self.tx_en = Pin(tx_en, Pin.OUT)
      self.rx_en = Pin(rx_en, Pin.OUT)
      self.rx_enable()
    
    self.uart = UART(2, 115200, tx=tx, rx=rx)

  def rx_enable(self):
    if self.isAutoEnableRT == False:
      self.rx_en.value(1)
      self.tx_en.value(0)
  
  def tx_enable(self):
    if self.isAutoEnableRT == False:
      self.rx_en.value(0)
      self.tx_en.value(1)
    
  def check_sum(self, data):
    sum = 0
    for i in range(2,data[3] + 2):
      sum += data[i]
    sum = ~sum
    return (sum & 0xFF)
    
  def send_data(self, data):
    self.tx_enable()
    for d in data:
      self.uart.write(ustruct.pack('B',d))
    # time.sleep_us(10)
    if self.isAutoEnableRT == False:
      self.rx_en.value(1)
      self.tx_en.value(0)
    # self.rx_enable()
  def run(self, id, p, servo_run_time = 1000):
    tx_buf = [0x55,0x55]
    tx_buf.append(id)
    tx_buf.append(7)
    tx_buf.append(SERVO_MOVE_TIME_WRITE)
    tx_buf.append(get_low8_byte(p))
    tx_buf.append(get_high8_byte(p))
    tx_buf.append(get_low8_byte(servo_run_time))
    tx_buf.append(get_high8_byte(servo_run_time))
    tx_buf.append(self.check_sum(tx_buf))
    self.send_data(tx_buf)
  
  # def run_mult(self, pp, servo_run_time):
    # for p in enumerate(pp):
      # self.run(p[0] + 1, p[1], servo_run_time)
      #time.sleep(run_time / 1000.0)  # 等待动作完成
      
  def run_action_group(self, action_group):
    for action in action_group:
        servo_id = action['id']
        position = action['position']
        run_time = action['time']
        self.run(servo_id, position, run_time)
    # 等待最大的运行时间，以确保所有伺服马达完成动作
    max_time = max(action['time'] for action in action_group)
    time.sleep(max_time / 1000.0)

  def run_multiple_groups(self, action_groups):
    for group in action_groups:
        self.run_action_group(group)  
        
  def run_add_or_dec(self, id, speed):
    try:
      pos = have_got_servo_pos[id]
    except:
      pos = self.get_position(id)
      if pos == False:
        return False

    pos += speed
    if pos < 0:pos = 0
    if pos > 1000:pos = 1000
    have_got_servo_pos[id] = pos
    self.run(id, pos, 20)
    return True
    
  def stop(self, id):
    tx_buf = [0x55,0x55]
    tx_buf.append(id)
    tx_buf.append(3)
    tx_buf.append(SERVO_MOVE_STOP)
    tx_buf.append(self.check_sum(tx_buf))
    self.send_data(tx_buf)

  def set_ID(self, old_id,new_id):
    tx_buf = [0x55,0x55]
    tx_buf.append(old_id)
    tx_buf.append(4)
    tx_buf.append(SERVO_ID_WRITE)
    tx_buf.append(new_id)
    tx_buf.append(self.check_sum(tx_buf))
    self.send_data(tx_buf)

  def get_ID(self, id):
    self.uart.read()
    tx_buf = [0x55, 0x55]
    tx_buf.append(id)
    tx_buf.append(3)
    tx_buf.append(SERVO_ID_READ)
    tx_buf.append(self.check_sum(tx_buf))
    self.send_data(tx_buf)

    time_now = time.ticks_ms()
    while self.uart.any() == 0:
      if time.ticks_ms() - time_now > 50:
        return False
    if self.servo_receive_handle():
      return self.rx_buf[5]
    return False

  def set_mode(self, id, mode, speed = 0):
    tx_buf = [0x55,0x55]
    tx_buf.append(id)
    tx_buf.append(7)
    tx_buf.append(SERVO_OR_MOTOR_MODE_WRITE)
    tx_buf.append(mode)
    tx_buf.append(0)
    tx_buf.append(get_low8_byte(speed))
    tx_buf.append(get_high8_byte(speed))
    tx_buf.append(self.check_sum(tx_buf))
    self.send_data(tx_buf)
    
  def load(self, id):
    tx_buf = [0x55,0x55]
    tx_buf.append(id)
    tx_buf.append(4)
    tx_buf.append(SERVO_LOAD_OR_UNLOAD_WRITE)
    tx_buf.append(1)
    tx_buf.append(self.check_sum(tx_buf))
    self.send_data(tx_buf)
    
  def unload(self, id):
    tx_buf = [0x55,0x55]
    tx_buf.append(id)
    tx_buf.append(4)
    tx_buf.append(SERVO_LOAD_OR_UNLOAD_WRITE)
    tx_buf.append(0)
    tx_buf.append(self.check_sum(tx_buf))
    self.send_data(tx_buf)
    
    
  def servo_receive_handle(self):
    frameStarted = False
    frameCount = 0
    dataCount = 0
    dataLength = 2
    self.rx_buf = [0x55]
    time_now = time.ticks_ms()
    while self.uart.any():
      buf = ustruct.unpack('B', self.uart.read(1))[0]
      time.sleep_us(100)
      if not frameStarted:
        if buf == 0x55:
          frameCount += 1
          if frameCount == 2:
            frameCount = 0
            frameStarted = True
            dataCount = 1
        else:
          frameStarted = False
          dataCount = 0
          frameCount = 0
        
      if frameStarted:
        self.rx_buf.append(buf)
        
        if dataCount == 3:
          dataLength = self.rx_buf[dataCount]
          if dataLength < 3 or dataLength > 7:
            dataLength = 2
            frameStarted = False
        dataCount += 1
        if dataCount == dataLength + 3:
          c = self.check_sum(self.rx_buf)
          if c == self.rx_buf[dataCount - 1]:
            return True
          return False
      if time.ticks_ms() - time_now > 1000:
        return False
    
  def get_position(self, id):
    self.uart.read()
    tx_buf = [0x55,0x55]
    tx_buf.append(id)
    tx_buf.append(3)
    tx_buf.append(SERVO_POS_READ)
    tx_buf.append(self.check_sum(tx_buf))
    
    self.send_data(tx_buf)
    
    time_now = time.ticks_ms()
    while self.uart.any() == 0:
      if time.ticks_ms() - time_now > 50:
        return False
    if self.servo_receive_handle():
      return ustruct.unpack('h', ustruct.pack('H', byte_to_hw(self.rx_buf[5], self.rx_buf[6])))[0]
    return False

  def get_vin(self, id):
    self.uart.read()
    tx_buf = [0x55,0x55]
    tx_buf.append(id)
    tx_buf.append(3)
    tx_buf.append(SERVO_VIN_READ)
    tx_buf.append(self.check_sum(tx_buf))
    
    self.send_data(tx_buf)
    
    time_now = time.ticks_ms()
    while self.uart.any() == 0:
      if time.ticks_ms() - time_now > 50:
        return False
    if self.servo_receive_handle():
      return byte_to_hw(self.rx_buf[5], self.rx_buf[6])
    return False

  def adjust_offset(self, id,offset):
    tx_buf = [0x55,0x55]
    tx_buf.append(id)
    tx_buf.append(4)
    tx_buf.append(SERVO_ANGLE_OFFSET_ADJUST)
    tx_buf.append(offset)
    tx_buf.append(self.check_sum(tx_buf))
    self.send_data(tx_buf)

  def save_offset(self, id):
    tx_buf = [0x55,0x55]
    tx_buf.append(id)
    tx_buf.append(3)
    tx_buf.append(SERVO_ANGLE_OFFSET_WRITE)
    tx_buf.append(self.check_sum(tx_buf))
    self.send_data(tx_buf)

  def get_offset(self, id):
    self.uart.read()
    tx_buf = [0x55, 0x55]
    tx_buf.append(id)
    tx_buf.append(3)
    tx_buf.append(SERVO_ANGLE_OFFSET_READ)
    tx_buf.append(self.check_sum(tx_buf))
    self.send_data(tx_buf)

    time_now = time.ticks_ms()
    while self.uart.any() == 0:
      if time.ticks_ms() - time_now > 50:
        return False
    if self.servo_receive_handle():
      return ustruct.unpack('b',ustruct.pack('B',self.rx_buf[5]))[0]
    return False


if __name__ == '__main__':
  b = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)#建立一個名叫b的BusServo物件,傳入__init__所需參數
  # #b.run(1,600)#執行run方法:def run(self, id, p, servo_run_time = 1000):
  # servo_position1=[500,500,500,500,500,500]
  # servo_run_time1=1000
  # servo_position2=[400,500,500,500,500,500]
  # servo_run_time2=1000
  # b.run_mult(servo_position1,servo_run_time1)
  # b.run_mult(servo_position2,servo_run_time2)
  # 
  # print(b.get_position(1))#pos = self.get_position(id)[97]
  # print(b.get_position(2))
  # print(b.get_position(3))
  
  # actions = [
        # {'id': 1, 'position': 300, 'time': 1000},
        # {'id': 2, 'position': 500, 'time': 1000},
        # {'id': 3, 'position': 280, 'time': 1000},
        # {'id': 4, 'position': 900, 'time': 1000},
        # {'id': 5, 'position': 700, 'time': 1000},
        # {'id': 6, 'position': 500, 'time': 1000}
    # ]
    # 
  # b.run_mult(actions)
  # action_groups = [
      # [
          # {'id': 1, 'position': 300, 'time': 1000},
          # {'id': 2, 'position': 500, 'time': 1000},
          # {'id': 3, 'position': 280, 'time': 1000},
          # {'id': 4, 'position': 900, 'time': 1000},
          # {'id': 5, 'position': 700, 'time': 1000},
          # {'id': 6, 'position': 500, 'time': 1000}
      # ],
      # [
          # {'id': 1, 'position': 300, 'time': 600},
          # {'id': 2, 'position': 500, 'time': 600},
          # {'id': 3, 'position': 170, 'time': 600},
          # {'id': 4, 'position': 820, 'time': 600},
          # {'id': 5, 'position': 460, 'time': 600},
          # {'id': 6, 'position': 480, 'time': 600}
      # ],
      # [
          # {'id': 1, 'position': 550, 'time': 600},
          # {'id': 2, 'position': 500, 'time': 600},
          # {'id': 3, 'position': 170, 'time': 600},
          # {'id': 4, 'position': 820, 'time': 600},
          # {'id': 5, 'position': 460, 'time': 600},
          # {'id': 6, 'position': 480, 'time': 600}
      # ],
      # [
          # {'id': 1, 'position': 550, 'time': 600},
          # {'id': 2, 'position': 500, 'time': 600},
          # {'id': 3, 'position': 280, 'time': 600},
          # {'id': 4, 'position': 910, 'time': 600},
          # {'id': 5, 'position': 700, 'time': 600},
          # {'id': 6, 'position': 500, 'time': 600}
      # ],
      # [
          # {'id': 1, 'position': 550, 'time': 600},
          # {'id': 2, 'position': 500, 'time': 600},
          # {'id': 3, 'position': 280, 'time': 600},
          # {'id': 4, 'position': 910, 'time': 600},
          # {'id': 5, 'position': 700, 'time': 600},
          # {'id': 6, 'position': 20, 'time': 600}
      # ],
      # [
          # {'id': 1, 'position': 550, 'time': 600},
          # {'id': 2, 'position': 500, 'time': 600},
          # {'id': 3, 'position': 290, 'time': 600},
          # {'id': 4, 'position': 940, 'time': 600},
          # {'id': 5, 'position': 540, 'time': 600},
          # {'id': 6, 'position': 20, 'time': 600}
      # ],
      # [
          # {'id': 1, 'position': 300, 'time': 600},
          # {'id': 2, 'position': 500, 'time': 600},
          # {'id': 3, 'position': 280, 'time': 600},
          # {'id': 4, 'position': 940, 'time': 600},
          # {'id': 5, 'position': 530, 'time': 600},
          # {'id': 6, 'position': 20, 'time': 600}
      # ],
      # [
          # {'id': 1, 'position': 300, 'time': 600},
          # {'id': 2, 'position': 500, 'time': 600},
          # {'id': 3, 'position': 280, 'time': 600},
          # {'id': 4, 'position': 920, 'time': 600},
          # {'id': 5, 'position': 700, 'time': 600},
          # {'id': 6, 'position': 20, 'time': 600}
      # ],
      # [
          # {'id': 1, 'position': 300, 'time': 600},
          # {'id': 2, 'position': 500, 'time': 600},
          # {'id': 3, 'position': 280, 'time': 600},
          # {'id': 4, 'position': 920, 'time': 600},
          # {'id': 5, 'position': 700, 'time': 600},
          # {'id': 6, 'position': 500, 'time': 600}
      # ]
  # ]

  b.run_multiple_groups(action_groups)
    
  










