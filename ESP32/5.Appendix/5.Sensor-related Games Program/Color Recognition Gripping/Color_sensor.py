from micropython import const
from Color_CONST import *
from time import sleep

class COLOR:
  class GestureData:
    def __init__(self):
      self.u_data = [0] * 32
      self.d_data = [0] * 32
      self.l_data = [0] * 32
      self.r_data = [0] * 32
      self.index = 0
      self.total_gestures = 0
      self.in_threshold = 0
      self.out_threshold = 0

  def __init__(self, bus, address=APDS9960_I2C_ADDR, valid_id=APDS9960_DEV_ID):
    
    self.address = address
    self.bus = bus
    self.gesture_ud_delta_ = 0
    self.gesture_lr_delta_ = 0

    self.gesture_ud_count_ = 0
    self.gesture_lr_count_ = 0

    self.gesture_near_count_ = 0
    self.gesture_far_count_ = 0

    self.gesture_state_ = 0
    self.gesture_motion_ = APDS9960_DIR_NONE

    self.gesture_data_ = COLOR.GestureData()

    
    self.dev_id = self._read_byte_data(APDS9960_REG_ID)
    if not self.dev_id in bytes(valid_id):
      print("raise ADPS9960InvalidDevId",self.dev_id, valid_id)

    
    self.setMode(APDS9960_MODE_ALL, False)

    self._write_byte_data(APDS9960_REG_ATIME, APDS9960_DEFAULT_ATIME)
    self._write_byte_data(APDS9960_REG_WTIME, APDS9960_DEFAULT_WTIME)
    self._write_byte_data(APDS9960_REG_PPULSE, APDS9960_DEFAULT_PROX_PPULSE)
    self._write_byte_data(APDS9960_REG_POFFSET_UR, APDS9960_DEFAULT_POFFSET_UR)
    self._write_byte_data(APDS9960_REG_POFFSET_DL, APDS9960_DEFAULT_POFFSET_DL)
    self._write_byte_data(APDS9960_REG_CONFIG1, APDS9960_DEFAULT_CONFIG1)
    self.setLEDDrive(APDS9960_DEFAULT_LDRIVE)
    self.setProximityGain(APDS9960_DEFAULT_PGAIN)
    self.setAmbientLightGain(APDS9960_DEFAULT_AGAIN)
    self.setProxIntLowThresh(APDS9960_DEFAULT_PILT)
    self.setProxIntHighThresh(APDS9960_DEFAULT_PIHT)
    self.setLightIntLowThreshold(APDS9960_DEFAULT_AILT)
    self.setLightIntHighThreshold(APDS9960_DEFAULT_AIHT)

    self._write_byte_data(APDS9960_REG_PERS, APDS9960_DEFAULT_PERS)
    self._write_byte_data(APDS9960_REG_CONFIG2, APDS9960_DEFAULT_CONFIG2)
    self._write_byte_data(APDS9960_REG_CONFIG3, APDS9960_DEFAULT_CONFIG3)

    
    self.setGestureEnterThresh(APDS9960_DEFAULT_GPENTH)
    self.setGestureExitThresh(APDS9960_DEFAULT_GEXTH)
    self._write_byte_data(APDS9960_REG_GCONF1, APDS9960_DEFAULT_GCONF1)

    self.setGestureGain(APDS9960_DEFAULT_GGAIN)
    self.setGestureLEDDrive(APDS9960_DEFAULT_GLDRIVE)
    self.setGestureWaitTime(APDS9960_DEFAULT_GWTIME)
    self._write_byte_data(APDS9960_REG_GOFFSET_U, APDS9960_DEFAULT_GOFFSET)
    self._write_byte_data(APDS9960_REG_GOFFSET_D, APDS9960_DEFAULT_GOFFSET)
    self._write_byte_data(APDS9960_REG_GOFFSET_L, APDS9960_DEFAULT_GOFFSET)
    self._write_byte_data(APDS9960_REG_GOFFSET_R, APDS9960_DEFAULT_GOFFSET)
    self._write_byte_data(APDS9960_REG_GPULSE, APDS9960_DEFAULT_GPULSE)
    self._write_byte_data(APDS9960_REG_GCONF3, APDS9960_DEFAULT_GCONF3)
    self.setGestureIntEnable(APDS9960_DEFAULT_GIEN)

  def getMode(self):
    return self._read_byte_data(APDS9960_REG_ENABLE)

  def setMode(self, mode, enable=True):
    
    reg_val = self.getMode()

    if mode < 0 or mode > APDS9960_MODE_ALL:
      print("raise ADPS9960InvalidMode",mode)

    if mode == APDS9960_MODE_ALL:
      if enable:
        reg_val = 0x7f
      else:
        reg_val = 0x00
    else:
      if enable:
        reg_val |= (1 << mode);
      else:
        reg_val &= ~(1 << mode);
    
    self._write_byte_data(APDS9960_REG_ENABLE, reg_val)

  def enableLightSensor(self, interrupts=True):
    self.setAmbientLightGain(APDS9960_DEFAULT_AGAIN)
    self.setAmbientLightIntEnable(interrupts)
    self.enablePower()
    self.setMode(APDS9960_MODE_AMBIENT_LIGHT, True)

  def disableLightSensor(self):
    self.setAmbientLightIntEnable(False)
    self.setMode(APDS9960_MODE_AMBIENT_LIGHT, False)

  def enableProximitySensor(self, interrupts=True):
    self.setProximityGain(APDS9960_DEFAULT_PGAIN)
    self.setLEDDrive(APDS9960_DEFAULT_LDRIVE)
    self.setProximityIntEnable(interrupts)
    self.enablePower()
    self.setMode(APDS9960_MODE_PROXIMITY, True)
  
  def disableProximitySensor(self):
    self.setProximityIntEnable(False)
    self.setMode(APDS9960_MODE_PROXIMITY, False)
  
  def enableGestureSensor(self, interrupts=True):
    self.resetGestureParameters()
    self._write_byte_data(APDS9960_REG_WTIME, 0xff)
    self._write_byte_data(APDS9960_REG_PPULSE, APDS9960_DEFAULT_GESTURE_PPULSE)
    self.setLEDBoost(APDS9960_LED_BOOST_300)
    self.setGestureIntEnable(interrupts)
    self.setGestureMode(True)
    self.enablePower()
    self.setMode(APDS9960_MODE_WAIT, True)
    self.setMode(APDS9960_MODE_PROXIMITY, True)
    self.setMode(APDS9960_MODE_GESTURE, True)

  
  def disableGestureSensor(self):
    self.resetGestureParameters()
    self.setGestureIntEnable(False)
    self.setGestureMode(False)
    self.setMode(APDS9960_MODE_GESTURE, False)
  
  def isGestureAvailable(self):
    val = self._read_byte_data(APDS9960_REG_GSTATUS)

    
    val &= APDS9960_BIT_GVALID;

    return (val == APDS9960_BIT_GVALID)

  def readGesture(self):
    fifo_level = 0
    bytes_read = 0
    fifo_data = []

    
    if not (self.getMode() & 0b01000001) or not self.isGestureAvailable():
      return APDS9960_DIR_NONE

    
    while(self.isGestureAvailable()):
      
      fifo_level = self._read_byte_data(APDS9960_REG_GFLVL)

      
      if fifo_level > 0:
        fifo_data = []
        for i in range(0, fifo_level):
          fifo_data += self._read_i2c_block_data(APDS9960_REG_GFIFO_U, 4)

        
        if len(fifo_data) >= 4:
          for i in range(0, len(fifo_data), 4):
            self.gesture_data_.u_data[self.gesture_data_.index] = fifo_data[i + 0]
            self.gesture_data_.d_data[self.gesture_data_.index] = fifo_data[i + 1]
            self.gesture_data_.l_data[self.gesture_data_.index] = fifo_data[i + 2]
            self.gesture_data_.r_data[self.gesture_data_.index] = fifo_data[i + 3]
            self.gesture_data_.index += 1
            self.gesture_data_.total_gestures += 1

          
          if self.processGestureData():
            if self.decodeGesture():
              
              pass

          
          self.gesture_data_.index = 0
          self.gesture_data_.total_gestures = 0

      
      sleep(APDS9960_TIME_FIFO_PAUSE)

    
    sleep(APDS9960_TIME_FIFO_PAUSE)
    self.decodeGesture()
    motion = self.gesture_motion_

    self.resetGestureParameters()
    return motion

  def enablePower(self):
    self.setMode(APDS9960_MODE_POWER, True)


  def disablePower(self):
    
    self.setMode(APDS9960_MODE_POWER, False)

  def readAmbientLight(self):
    
    l = self._read_byte_data(APDS9960_REG_CDATAL)

    
    h = self._read_byte_data(APDS9960_REG_CDATAH)

    return l + (h << 8)

  
  def readRedLight(self):
    
    l = self._read_byte_data(APDS9960_REG_RDATAL)

    
    h = self._read_byte_data(APDS9960_REG_RDATAH)

    return l + (h << 8)

  
  def readGreenLight(self):
    
    l = self._read_byte_data(APDS9960_REG_GDATAL)

    
    h = self._read_byte_data(APDS9960_REG_GDATAH)

    return l + (h << 8)

  
  def readBlueLight(self):
    
    l = self._read_byte_data(APDS9960_REG_BDATAL)

    
    h = self._read_byte_data(APDS9960_REG_BDATAH)

    return l + (h << 8)

  def readProximity(self):
    return self._read_byte_data(APDS9960_REG_PDATA)

  def resetGestureParameters(self):
    self.gesture_data_.index = 0
    self.gesture_data_.total_gestures = 0

    self.gesture_ud_delta_ = 0
    self.gesture_lr_delta_ = 0

    self.gesture_ud_count_ = 0
    self.gesture_lr_count_ = 0

    self.gesture_near_count_ = 0
    self.gesture_far_count_ = 0

    self.gesture_state_ = 0
    self.gesture_motion_ = APDS9960_DIR_NONE


  def processGestureData(self):
    u_first = 0
    d_first = 0
    l_first = 0
    r_first = 0
    u_last = 0
    d_last = 0
    l_last = 0
    r_last = 0
    if self.gesture_data_.total_gestures <= 4:
      return False
    if self.gesture_data_.total_gestures <= 32 and self.gesture_data_.total_gestures > 0:
      
      for i in range(0, self.gesture_data_.total_gestures):
        if self.gesture_data_.u_data[i] > APDS9960_GESTURE_THRESHOLD_OUT and \
                self.gesture_data_.d_data[i] > APDS9960_GESTURE_THRESHOLD_OUT and \
                self.gesture_data_.l_data[i] > APDS9960_GESTURE_THRESHOLD_OUT and \
                self.gesture_data_.r_data[i] > APDS9960_GESTURE_THRESHOLD_OUT:

          u_first = self.gesture_data_.u_data[i]
          d_first = self.gesture_data_.d_data[i]
          l_first = self.gesture_data_.l_data[i]
          r_first = self.gesture_data_.r_data[i]
          break

      
      if u_first == 0 or  d_first == 0 or l_first == 0 or r_first == 0:
        return False

      
      for i in reversed(range(0, self.gesture_data_.total_gestures)):
        if self.gesture_data_.u_data[i] > APDS9960_GESTURE_THRESHOLD_OUT and \
                self.gesture_data_.d_data[i] > APDS9960_GESTURE_THRESHOLD_OUT and \
                self.gesture_data_.l_data[i] > APDS9960_GESTURE_THRESHOLD_OUT and \
                self.gesture_data_.r_data[i] > APDS9960_GESTURE_THRESHOLD_OUT:

          u_last = self.gesture_data_.u_data[i]
          d_last = self.gesture_data_.d_data[i]
          l_last = self.gesture_data_.l_data[i]
          r_last = self.gesture_data_.r_data[i]
          break

      
      ud_ratio_first = ((u_first - d_first) * 100) / (u_first + d_first)
      lr_ratio_first = ((l_first - r_first) * 100) / (l_first + r_first)
      ud_ratio_last = ((u_last - d_last) * 100) / (u_last + d_last)
      lr_ratio_last = ((l_last - r_last) * 100) / (l_last + r_last)

      
      ud_delta = ud_ratio_last - ud_ratio_first
      lr_delta = lr_ratio_last - lr_ratio_first

      
      self.gesture_ud_delta_ += ud_delta
      self.gesture_lr_delta_ += lr_delta

      
      if self.gesture_ud_delta_ >= APDS9960_GESTURE_SENSITIVITY_1:
        self.gesture_ud_count_ = 1
      elif self.gesture_ud_delta_ <= -APDS9960_GESTURE_SENSITIVITY_1:
        self.gesture_ud_count_ = -1
      else:
        self.gesture_ud_count_ = 0

      
      if self.gesture_lr_delta_ >= APDS9960_GESTURE_SENSITIVITY_1:
        self.gesture_lr_count_ = 1
      elif self.gesture_lr_delta_ <= -APDS9960_GESTURE_SENSITIVITY_1:
        self.gesture_lr_count_ = -1
      else:
        self.gesture_lr_count_ = 0

      
      if self.gesture_ud_count_ == 0 and self.gesture_lr_count_ == 0:
        if abs(ud_delta) < APDS9960_GESTURE_SENSITIVITY_2 and \
                abs(lr_delta) < APDS9960_GESTURE_SENSITIVITY_2:

          if ud_delta == 0 and lr_delta == 0:
            self.gesture_near_count_ += 1
          elif ud_delta != 0 or lr_delta != 0:
            self.gesture_far_count_ += 1

          if self.gesture_near_count_ >= 10 and self.gesture_far_count_ >= 2:
            if ud_delta == 0 and lr_delta == 0:
              self.gesture_state_ = APDS9960_STATE_NEAR
            elif ud_delta != 0 and lr_delta != 0:
              self.gesture_state_ = APDS9960_STATE_FAR
            return True
      else:
        if abs(ud_delta) < APDS9960_GESTURE_SENSITIVITY_2 and \
                abs(lr_delta) < APDS9960_GESTURE_SENSITIVITY_2:

          if ud_delta == 0 and lr_delta == 0:
            self.gesture_near_count_ += 1

          if self.gesture_near_count_ >= 10:
            self.gesture_ud_count_ = 0
            self.gesture_lr_count_ = 0
            self.gesture_ud_delta_ = 0
            self.gesture_lr_delta_ = 0

    return False

  def decodeGesture(self):
    if self.gesture_state_ == APDS9960_STATE_NEAR:
      self.gesture_motion_ = APDS9960_DIR_NEAR
      return True

    if self.gesture_state_ == APDS9960_STATE_FAR:
      self.gesture_motion_ = APDS9960_DIR_FAR
      return True
    if self.gesture_ud_count_ == -1 and self.gesture_lr_count_ == 0:
      self.gesture_motion_ = APDS9960_DIR_UP
    elif self.gesture_ud_count_ == 1 and self.gesture_lr_count_ == 0:
      self.gesture_motion_ = APDS9960_DIR_DOWN
    elif self.gesture_ud_count_ == 0 and self.gesture_lr_count_ == 1:
      self.gesture_motion_ = APDS9960_DIR_RIGHT
    elif self.gesture_ud_count_ == 0 and self.gesture_lr_count_ == -1:
      self.gesture_motion_ = APDS9960_DIR_LEFT
    elif self.gesture_ud_count_ == -1 and self.gesture_lr_count_ == 1:
      if abs(self.gesture_ud_delta_) > abs(self.gesture_lr_delta_):
        self.gesture_motion_ = APDS9960_DIR_UP
      else:
        self.gesture_motion_ = APDS9960_DIR_DOWN
    elif self.gesture_ud_count_ == 1 and self.gesture_lr_count_ == -1:
      if abs(self.gesture_ud_delta_) > abs(self.gesture_lr_delta_):
        self.gesture_motion_ = APDS9960_DIR_DOWN
      else:
        self.gesture_motion_ = APDS9960_DIR_LEFT
    elif self.gesture_ud_count_ == -1 and self.gesture_lr_count_ == -1:
      if abs(self.gesture_ud_delta_) > abs(self.gesture_lr_delta_):
        self.gesture_motion_ = APDS9960_DIR_UP
      else:
        self.gesture_motion_ = APDS9960_DIR_LEFT
    elif self.gesture_ud_count_ == 1 and self.gesture_lr_count_ == 1:
      if abs(self.gesture_ud_delta_) > abs(self.gesture_lr_delta_):
        self.gesture_motion_ = APDS9960_DIR_DOWN
      else:
        self.gesture_motion_ = APDS9960_DIR_RIGHT
    else:
      return False

    return True

  def getProxIntLowThresh(self):
    return self._read_byte_data(APDS9960_REG_PILT)

  def setProxIntLowThresh(self, threshold):
    self._write_byte_data(APDS9960_REG_PILT, threshold)


  def getProxIntHighThresh(self):
    return self._read_byte_data(APDS9960_REG_PIHT)

  def setProxIntHighThresh(self, threshold):
    self._write_byte_data(APDS9960_REG_PIHT, threshold)


  def getLEDDrive(self):
    val = self._read_byte_data(APDS9960_REG_CONTROL)
    return (val >> 6) & 0b00000011

  def setLEDDrive(self, drive):
    val = self._read_byte_data(APDS9960_REG_CONTROL)
    drive &= 0b00000011
    drive = drive << 6
    val &= 0b00111111
    val |= drive

    self._write_byte_data(APDS9960_REG_CONTROL, val)


  def getProximityGain(self):
    val = self._read_byte_data(APDS9960_REG_CONTROL)
    return (val >> 2) & 0b00000011

  def setProximityGain(self, drive):
    val = self._read_byte_data(APDS9960_REG_CONTROL)
    drive &= 0b00000011
    drive = drive << 2
    val &= 0b11110011
    val |= drive

    self._write_byte_data(APDS9960_REG_CONTROL, val)


  def getAmbientLightGain(self):
    val = self._read_byte_data(APDS9960_REG_CONTROL)
    return (val & 0b00000011)

  def setAmbientLightGain(self, drive):
    val = self._read_byte_data(APDS9960_REG_CONTROL)
    drive &= 0b00000011
    val &= 0b11111100
    val |= drive
    self._write_byte_data(APDS9960_REG_CONTROL, val)


  def getLEDBoost(self):
    val = self._read_byte_data(APDS9960_REG_CONFIG2)
    return (val >> 4) & 0b00000011

  def setLEDBoost(self, boost):
    val = self._read_byte_data(APDS9960_REG_CONFIG2)
    boost &= 0b00000011
    boost = boost << 4
    val &= 0b11001111
    val |= boost
    self._write_byte_data(APDS9960_REG_CONFIG2, val)


  def getProxGainCompEnable(self):
    val = self._read_byte_data(APDS9960_REG_CONFIG3)
    val = (val >> 5) & 0b00000001
    return val == 1

  def setProxGainCompEnable(self, enable):
    val = self._read_byte_data(APDS9960_REG_CONFIG3)
    val &= 0b11011111
    if enable:
      val |= 0b00100000

    self._write_byte_data(APDS9960_REG_CONFIG3, val)


  def getProxPhotoMask(self):
    val = self._read_byte_data(APDS9960_REG_CONFIG3)
    return val & 0b00001111

  def setProxPhotoMask(self, mask):
    val = self._read_byte_data(APDS9960_REG_CONFIG3)
    mask &= 0b00001111
    val &= 0b11110000
    val |= mask

    self._write_byte_data(APDS9960_REG_CONFIG3, val)

  def getGestureEnterThresh(self):
    return self._read_byte_data(APDS9960_REG_GPENTH)

  def setGestureEnterThresh(self, threshold):
    self._write_byte_data(APDS9960_REG_GPENTH, threshold)

  def getGestureExitThresh(self):
    return self._read_byte_data(APDS9960_REG_GEXTH)

  def setGestureExitThresh(self, threshold):
    self._write_byte_data(APDS9960_REG_GEXTH, threshold)


  def getGestureGain(self):
    val = self._read_byte_data(APDS9960_REG_GCONF2)
    return (val >> 5) & 0b00000011

  def setGestureGain(self, gain):
    val = self._read_byte_data(APDS9960_REG_GCONF2)
    gain &= 0b00000011
    gain = gain << 5
    val &= 0b10011111
    val |= gain
    self._write_byte_data(APDS9960_REG_GCONF2, val)

  def getGestureLEDDrive(self):
    val = self._read_byte_data(APDS9960_REG_GCONF2)
    return (val >> 3) & 0b00000011

  def setGestureLEDDrive(self, drive):
    val = self._read_byte_data(APDS9960_REG_GCONF2)
    drive &= 0b00000011;
    drive = drive << 3;
    val &= 0b11100111;
    val |= drive;

    self._write_byte_data(APDS9960_REG_GCONF2, val)


  def getGestureWaitTime(self):
    val = self._read_byte_data(APDS9960_REG_GCONF2)
    return val & 0b00000111

  def setGestureWaitTime(self, time):
    val = self._read_byte_data(APDS9960_REG_GCONF2)
    time &= 0b00000111
    val &= 0b11111000
    val |= time

    self._write_byte_data(APDS9960_REG_GCONF2, val)

  def getLightIntLowThreshold(self):
    return self._read_byte_data(APDS9960_REG_AILTL) | (self._read_byte_data(APDS9960_REG_AILTH) << 8)

  def setLightIntLowThreshold(self, threshold):
    self._write_byte_data(APDS9960_REG_AILTL, threshold & 0x00ff)
    self._write_byte_data(APDS9960_REG_AILTH, (threshold & 0xff00) >> 8)

  def getLightIntHighThreshold(self):
    return self._read_byte_data(APDS9960_REG_AIHTL) | (self._read_byte_data(APDS9960_REG_AIHTH) << 8)

  def setLightIntHighThreshold(self, threshold):
    self._write_byte_data(APDS9960_REG_AIHTL, threshold & 0x00ff)
    self._write_byte_data(APDS9960_REG_AIHTH, (threshold & 0xff00) >> 8)

  def getProximityIntLowThreshold(self):
    return self._read_byte_data(APDS9960_REG_PILT)

  def setProximityIntLowThreshold(self, threshold):
    self._write_byte_data(APDS9960_REG_PILT, threshold)

  def getProximityIntHighThreshold(self):
    return self._read_byte_data(APDS9960_REG_PIHT)

  def setProximityIntHighThreshold(self, threshold):
    self._write_byte_data(APDS9960_REG_PIHT, threshold)

  def getAmbientLightIntEnable(self):
    val = self._read_byte_data(APDS9960_REG_ENABLE)
    return (val >> 4) & 0b00000001 == 1

  def setAmbientLightIntEnable(self, enable):
    val = self._read_byte_data(APDS9960_REG_ENABLE)
    val &= 0b11101111;
    if enable:
      val |= 0b00010000
    self._write_byte_data(APDS9960_REG_ENABLE, val)


  def getProximityIntEnable(self):
    val = self._read_byte_data(APDS9960_REG_ENABLE)
    return (val >> 5) & 0b00000001 == 1

  def setProximityIntEnable(self, enable):
    val = self._read_byte_data(APDS9960_REG_ENABLE)
    val &= 0b11011111;
    if enable:
      val |= 0b00100000
    self._write_byte_data(APDS9960_REG_ENABLE, val)

  def getGestureIntEnable(self):
    val = self._read_byte_data(APDS9960_REG_GCONF4)
    return (val >> 1) & 0b00000001 == 1

  def setGestureIntEnable(self, enable):
    val = self._read_byte_data(APDS9960_REG_GCONF4)
    val &= 0b11111101
    if enable:
      val |= 0b00000010

    self._write_byte_data(APDS9960_REG_GCONF4, val)

  def clearAmbientLightInt(self):
    self._read_byte_data(APDS9960_REG_AICLEAR)


  def clearProximityInt(self):
    self._read_byte_data(APDS9960_REG_PICLEAR)


  def getGestureMode(self):
    val = self._read_byte_data(APDS9960_REG_GCONF4)
    return val & 0b00000001 == 1

  def setGestureMode(self, enable):
    val = self._read_byte_data(APDS9960_REG_GCONF4)
    val &= 0b11111110
    if enable:
      val |= 0b00000001

    self._write_byte_data(APDS9960_REG_GCONF4, val)

  def _read_byte_data(self, cmd):
    return self.bus.readfrom_mem(self.address, cmd, 1)[0]

  def _write_byte_data(self, cmd, val):
    return self.bus.writeto_mem(self.address, cmd, val.to_bytes(1,'little'))

  def _read_i2c_block_data(self, cmd, num):
    return self.bus.readfrom_mem(self.address, cmd, num)

if __name__ == '__main__':
  from machine import Pin, I2C
  import time
  
  RED = const(1)
  GREEN = const(2)
  BLUE = const(3)
  WHITE = const(4)
  
  R_F = const(8500)
  G_F = const(13000)
  B_F = const(16600)
  r_f = const(140)
  g_f = const(150)
  b_f = const(140)

  i2c = I2C(0, scl=Pin(27), sda=Pin(14), freq=100000)
  print(i2c.scan())
  apds = COLOR(i2c)
  apds.enableLightSensor(False)

  while True:
    c = apds.readAmbientLight()
    r = apds.readRedLight()
    g = apds.readGreenLight()
    b = apds.readBlueLight()
    
    
    r = int(255 * (r - r_f) / (R_F - r_f))
    g = int(255 * (g - g_f) / (G_F - g_f))
    b = int(255 * (b - b_f) / (B_F - b_f))
    
    if r > 25 and r > g and r > b:t = RED
    elif g > 25 and g > r and g > b:t = GREEN
    elif b > 25 and b > g and b > r:t = BLUE
    else:t = 0
    print("Color is ", t)
    print("AmbientLight", c, "RedLight", r,"GreenLight", g, "BlueLight", b)
    time.sleep_ms(500)



