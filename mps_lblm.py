from os import path
from pydm import Display
from pyqtgraph import InfiniteLine
from pydm.widgets.channel import PyDMChannel
import numpy as np

class mps_blm_main(Display):
  def __init__(self, parent=None, args=None, macros=None):
    super(mps_blm_main, self).__init__(parent=parent, args=args, macros=macros)
    PV = "ca://{P}:DM{BAY}_BUFFER_SIZE_RBV".format(**macros)
    self.num_points_channel = PyDMChannel(address=PV, value_slot=self.num_points_change)
    self.num_points_channel.connect()

    PV = "ca://{P}:BAY{BAY}_ADC{CH}_WF-BUF".format(**macros)
    self.data_channel = PyDMChannel(address=PV, value_slot=self.data_change)
    self.data_channel.connect()

    self.jesd_clock = 175.4 #MHz
    self.ns_spacing = self.jesd_clock* 2 * 1e6 / 1e6
    self.c = self.waveform.curveAtIndex(0)

    self.full_adc_range = 65536.
    self.full_mv_range = 1200.
    self.adc_factor = self.full_mv_range / self.full_adc_range
    self.adc_factor = 1

  def ui_filename(self):
      # Point to our UI file
      return 'mps_lblm.ui'

  def ui_filepath(self):
      # Return the full path to the UI file
      return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())

  def num_points_change(self, new_point_value):
      start = 0
      stop = new_point_value / self.ns_spacing
      x_axis_waveform = np.linspace(start, stop, new_point_value)
      self.c.receiveXWaveform(x_axis_waveform)
  
  def data_change(self, new_data):
      data_converted = self.adc_factor * new_data
      self.c.receiveYWaveform(data_converted)
    	
