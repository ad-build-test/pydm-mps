from os import path
from pydm import Display
from pydm.widgets.channel import PyDMChannel
import numpy as np
from epics import PV

class inline_threshold(Display):
  def __init__(self, parent=None, args=None, macros=None):
    super(inline_threshold, self).__init__(parent=parent, args=args, macros=macros)

    self.ana_channel = int(macros['CH_NUM'])
    self.int0_ch = self.ana_channel * 4 + 0
    self.int1_ch = self.ana_channel * 4 + 1    

    pv = "ca://{p}:LC1_ANA_INTCNT_{int0ch}_RBV".format(p=macros['P'],int0ch=self.int0_ch)
    self.int0_channel = PyDMChannel(address=pv, value_slot=self.int0_update)
    self.int0_channel.connect()

    pv = "ca://{p}:LC1_ANA_INTCNT_{int1ch}_RBV".format(p=macros['P'],int1ch=self.int1_ch)
    self.int0_channel = PyDMChannel(address=pv, value_slot=self.int1_update)
    self.int0_channel.connect()
    
    pv = "ca://{p}:I0_{tp}1H".format(p=macros['P_CH'],tp=macros['P_TYPE'])
    self.int0_val = PyDMChannel(address=pv, value_slot=self.int0_val_calc)
    self.int0_val.connect()
    
    pv = "ca://{p}:I1_{tp}1H".format(p=macros['P_CH'],tp=macros['P_TYPE'])
    self.int1_val = PyDMChannel(address=pv, value_slot=self.int1_val_calc)
    self.int1_val.connect()

  def ui_filename(self):
      # Point to our UI file
      return 'inline_threshold.ui'

  def ui_filepath(self):
      # Return the full path to the UI file
      return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())

  def int0_update(self, new_value):
      newTime = (new_value + 1) * (2.778)
      #self.ui.integrator0_time.setText('{val} ms'.format(val=newTime))

  def int1_update(self, new_value):
      newTime = (new_value + 1) * (2.778)
      #self.ui.integrator1_time.setText('{val} ms'.format(val=newTime))
      
  def int0_val_calc(self, new_value):
  		newVal = (new_value) * 2 * 600 / 65536
  		#self.ui.convert_i0.setText('{val} mV'.format(val=round(newVal,4)))
  		
  def int1_val_calc(self, new_value):
  		newVal = (new_value) * 2 * 600 / 65536
  		#self.ui.convert_i1.setText('{val} mV'.format(val=round(newVal,4)))
