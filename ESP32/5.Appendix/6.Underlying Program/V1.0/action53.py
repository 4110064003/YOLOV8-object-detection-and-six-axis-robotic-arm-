from machine import Pin,UART
from micropython import const
import time, ustruct

SERVO_MOVE_TIME_WRITE       = const(1)
SERVO_POS_READ              = const(28)

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
  def run_mult(self, actions):
        for action in actions:
            servo_id = action['id']
            position = action['position']
            run_time = action['time']
            self.run(servo_id, position, run_time)
            #time.sleep(run_time / 1000.0)  # 等待动作完成

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

if __name__ == '__main__':
  b = BusServo(tx=26, rx=35, tx_en=25, rx_en=12)#建立一個名叫b的BusServo物件,傳入__init__所需參數
  # #b.run(1,600)#執行run方法:def run(self, id, p, servo_run_time = 1000):
  #servo_position1=[500,500,500,500,500,500]
  #servo_run_time1=1000
  # servo_position2=[400,500,500,500,500,500]
  # servo_run_time2=1000
  #b.run_mult(servo_position1,servo_run_time1)
  # b.run_mult(servo_position2,servo_run_time2)
  # 
  # print(b.get_position(1))#pos = self.get_position(id)[97]
  # print(b.get_position(2))
  # print(b.get_position(3))
  actions = [
        {'id': 1, 'position': 300, 'time': 1000},
        {'id': 2, 'position': 500, 'time': 1000},
        {'id': 3, 'position': 280, 'time': 1000},
        {'id': 4, 'position': 900, 'time': 1000},
        {'id': 5, 'position': 700, 'time': 1000},
        {'id': 6, 'position': 500, 'time': 1000}
    ]
    
  b.run_mult(actions)


