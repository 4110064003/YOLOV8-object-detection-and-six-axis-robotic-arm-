import time
from os import stat
from BusServo import have_got_servo_pos



class RobotControl:
  
  def __init__(self, pwm_servo  = None, bus_servo  = None):
    self.bus_servo = bus_servo
    self.pwm_servo = pwm_servo
    
    self.online = False
    self.f_runActionGroup = False
    self.act_name = None
    self.act_run_times = 1
    self.acts = []
    self.act_index = 1
    self.run_loop = self._run_loop()
  
  def _run_loop(self):
    repo = ["$$>", "", "<$$"]
    act_run_times_now = 0
    time_over = time.ticks_ms()
    def fun():
      nonlocal repo
      nonlocal act_run_times_now
      nonlocal time_over

      if self.f_runActionGroup:
        if act_run_times_now < self.act_run_times:
          if time_over < time.ticks_ms():
            try:
              act = self.acts[self.act_index - 1]
              repo[1] = str(self.act_index)
              if self.online == True:
                print("".join(repo))
              act = tuple(map(int, act))
              
              time_over = time.ticks_ms() + act[0]
              if self.pwm_servo != None:
                self.pwm_servo.run_mult(act[1:], act[0])
              if self.bus_servo != None:
                self.bus_servo.run_mult(act[1:], act[0])
              self.act_index += 1
            except:
              self.act_index = 1
              act_run_times_now += 1
              pass
        else:
          self.f_runActionGroup = False
          repo[1] = 'end'
          print("".join(repo))
      else:
        act_run_times_now = 0
        self.act_run_times = 0
        self.act_name = None
        self.act_index = 1
    return fun    
        
  @staticmethod
  def generate_pos(act_name):
    acts = []
    fp = open(act_name, 'r') 
    fp.readline()
    ST = fp.readlines()
    fp.close()
    for st in ST:
      st = st.replace("\r\n", "")
      if st == "end":
        return acts
      acts.append(st.split(" "))
      
  @staticmethod
  def get_servo_num_on_file(act_name):
    with open(act_name, 'r') as fp: 
      line1 = fp.readline().replace('\r\n', '').split('=')
      servo_num = -1
      if line1[0] != 'servos':
        return False
      try:
        servo_num = int(line1[1])
      except:
        return False
      return servo_num
        
  def runActionGroup(self, act_name, times = 1, online=False):
    self.online = online
    try:
      stat(act_name)
    except:
      print("no such file or directory ", act_name)
      return False
    servo_num = RobotControl.get_servo_num_on_file(act_name)
    if servo_num == False:
      print("invalid action group file, servo num")
      return False 
    acts = RobotControl.generate_pos(act_name)
    servo_num += 1
    for act in acts:
      if len(act) != servo_num:
        print("invalid action group file, action data", len(act), servo_num)
        return False
        
    if self.act_name != act_name:
      self.acts = RobotControl.generate_pos(act_name)
      self.act_index = 1

    self.act_name = act_name
    self.act_run_times = times  
    self.f_runActionGroup = True
    
    have_got_servo_pos.clear()
    return True
    
    
  def stopActionGroup(self):
    self.f_runActionGroup = False
    
    
    








