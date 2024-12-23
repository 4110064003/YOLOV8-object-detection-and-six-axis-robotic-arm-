from machine import Pin, Timer
from HiwonderV2 import PWM#该PWM的duty范围0~16383
import time

PWMServo_IO_list = [23, 22, 21, 19, 18, 5]

class PWMServo:
  def __init__(self,PWMServo_IO_list = PWMServo_IO_list,first_id_is_one = True):

    self.servo = []
    self.servo_pwm_duty_now = []
    self.servo_pwm_duty_set = []
    self.servo_pwm_duty_inc = []
    self.servo_run_time = 20
    self.servo_pwm_duty_have_changed = False
    self.f_work_with_time = False
    
    self.ServoPwmDutyIncTimes = 0
    self.ServoRunning = False
    
    if first_id_is_one == True:
        self.servo.append(None)
        self.servo_pwm_duty_now.append(None)
        self.servo_pwm_duty_set.append(None)
        self.servo_pwm_duty_inc.append(None)
    
    for io in PWMServo_IO_list:
      self.servo.append(PWM(Pin(io), freq=50, duty=0))
      self.servo_pwm_duty_now.append(0)
      self.servo_pwm_duty_set.append(0)
      self.servo_pwm_duty_inc.append(0)
      
  def conver_duty(self, input):
    return (int(input * 16383 / 20000))
    
  def run(self, id, p, servo_run_time = 1000):
    if servo_run_time < 20:servo_run_time = 20
    if servo_run_time > 30000:servo_run_time = 30000
    if p < 400 or p > 2600:
      return False
    self.servo_run_time = servo_run_time
    self.servo_pwm_duty_set[id] = p
    self.servo_pwm_duty_have_changed = True
    if self.f_work_with_time == False:
      self.servo_pwm_duty_now[id] = p
      self.servo[id].duty(self.conver_duty(p))
  
  def run_mult(self, pp, servo_run_time):
    for p in enumerate(pp):
      if self.servo[0] == None:
        self.run(p[0] + 1, p[1], servo_run_time)
      else:
        self.run(p[0], p[1], servo_run_time)
  def work_with_time(self):
    self.f_work_with_time = True
    self.tim = Timer(0)
    self.tim.init(period=20, mode=Timer.PERIODIC, callback=self.callback)

  def callback(self,t):
    if self.servo_pwm_duty_have_changed:
      self.servo_pwm_duty_have_changed = False
      self.ServoPwmDutyIncTimes = self.servo_run_time // 20

      for item in enumerate(zip(self.servo_pwm_duty_now, self.servo_pwm_duty_set)):
        if item[1][0] != None:
          self.servo_pwm_duty_inc[item[0]] = (item[1][0] - item[1][1]) / self.ServoPwmDutyIncTimes
      self.ServoRunning = True
    
    if self.ServoRunning:
      self.ServoPwmDutyIncTimes -= 1
      for item in enumerate(zip(self.servo_pwm_duty_inc,self.servo_pwm_duty_set)):
        if item[1][0] != None:
          if self.ServoPwmDutyIncTimes == 0:
            self.servo_pwm_duty_now[item[0]] = item[1][1]
            self.ServoRunning = False
          else:
            self.servo_pwm_duty_now[item[0]] = item[1][1] + int(item[1][0] * self.ServoPwmDutyIncTimes)
          self.servo[item[0]].duty(self.conver_duty(self.servo_pwm_duty_now[item[0]]))

  def __del__(self):
    self.tim.deinit()

