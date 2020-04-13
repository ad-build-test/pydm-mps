from os import path
from pydm import Display
from pydm.widgets.channel import PyDMChannel
import numpy as np

class inline_threshold(Display):
  def __init__(self, parent=None, args=None, macros=None):
    super(inline_threshold, self).__init__(parent=parent, args=args, macros=macros)

    self.ana_channel = int(macros['CH_NUM'])
    self.int0_ch = self.ana_channel * 4 + 0
    self.int1_ch = self.ana_channel * 4 + 1    

    PV = "ca://{p}:LC1_ANA_INTCNT_{int0ch}_RBV".format(p=macros['P'],int0ch=self.int0_ch)
    self.int0_channel = PyDMChannel(address=PV, value_slot=self.int0_update)
    self.int0_channel.connect()

    PV = "ca://{p}:LC1_ANA_INTCNT_{int1ch}_RBV".format(p=macros['P'],int1ch=self.int1_ch)
    self.int0_channel = PyDMChannel(address=PV, value_slot=self.int1_update)
    self.int0_channel.connect()

  def ui_filename(self):
      # Point to our UI file
      return 'inline_threshold.ui'

  def ui_filepath(self):
      # Return the full path to the UI file
      return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())

  def int0_update(self, new_value):
      newTime = (new_value + 1) * (2.778)
      self.ui.integrator0_time.setText('{val} ms'.format(val=newTime))

  def int1_update(self, new_value):
      newTime = (new_value + 1) * (2.778)
      self.ui.integrator1_time.setText('{val} ms'.format(val=newTime))
