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

    PV = "ca://TPR:{LOCA}:{IOC_UNIT}:{INST}:TRG1{CH_NUM}_SYS0_TDES".format(**macros)
    self.coarse_delay_line = InfiniteLine(pos=0, angle=90, movable=False,pen={'color': (218,243,186), 'width': 2})
    self.coarse_position_channel = PyDMChannel(address=PV, value_slot=self.move_coarse)
    self.waveform.addItem(self.coarse_delay_line)
    self.coarse_position_channel.connect()

    self.peak_delay_line = InfiniteLine(pos=0, angle=90, movable=False,pen={'color': (11,135,161), 'width': 2})
    PV = "ca://{P}:LC1_ANA_PK_DEL_TRG_{CH_NUM}_RBV".format(**macros)
    self.peak_position_channel = PyDMChannel(address=PV, value_slot=self.move_peak)
    self.waveform.addItem(self.peak_delay_line)
    self.peak_position_channel.connect()

    self.peak_width_line = InfiniteLine(pos=0, angle=90, movable=False,pen={'color': (157,207,217), 'width': 2})
    PV = "ca://{P}:LC1_ANA_PK_WDT_TRG_{CH_NUM}_RBV".format(**macros)
    self.peak_width_channel = PyDMChannel(address=PV, value_slot=self.width_peak)
    self.waveform.addItem(self.peak_width_line)
    self.peak_width_channel.connect()

    self.ped_delay_line = InfiniteLine(pos=0, angle=90, movable=False,pen={'color': (223,116,237), 'width': 2})
    PV = "ca://{P}:LC1_ANA_PD_DEL_TRG_{CH_NUM}_RBV".format(**macros)
    self.ped_position_channel = PyDMChannel(address=PV, value_slot=self.move_ped)
    self.waveform.addItem(self.ped_delay_line)
    self.ped_position_channel.connect()

    self.ped_width_line = InfiniteLine(pos=0, angle=90, movable=False,pen={'color': (226,200,230), 'width': 2})
    PV = "ca://{P}:LC1_ANA_PD_WDT_TRG_{CH_NUM}_RBV".format(**macros)
    self.ped_width_channel = PyDMChannel(address=PV, value_slot=self.width_ped)
    self.waveform.addItem(self.ped_width_line)
    self.ped_width_channel.connect()

    self.coarse_val = 0
    self.peak_val = 0
    self.peak_width = 0
    self.ped_val = 0
    self.ped_width = 0
    self.init = 0

  def ui_filename(self):
      # Point to our UI file
      return 'mps_blm_main.ui'

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
 
  def move_coarse(self, new_line_value):
      self.coarse_val = new_line_value/1000.
      self.update_lines()     

  def move_peak(self, new_line_value):
    self.peak_val = new_line_value
    self.update_lines()

  def width_peak(self, new_line_value):
    self.peak_width = new_line_value
    self.update_lines()

  def move_ped(self, new_line_value):
    self.ped_val = new_line_value
    self.update_lines()

  def width_ped(self, new_line_value):
    self.ped_width = new_line_value
    self.update_lines()

  def update_lines(self):
    line1_pos = self.coarse_val
    line2_pos = self.peak_val + line1_pos
    line3_pos = self.peak_width + line2_pos
    line4_pos = self.ped_val + line1_pos
    line5_pos = self.ped_width + line4_pos
    self.coarse_delay_line.setValue(line1_pos)
    self.peak_delay_line.setValue(line2_pos)
    self.peak_width_line.setValue(line3_pos)
    self.ped_delay_line.setValue(line4_pos)
    self.ped_width_line.setValue(line5_pos)
    if (self.init < 5):
    	self.waveform.setXRange(line2_pos-1, line3_pos+1)
    	self.init += 1
    if line3_pos == 373.631699:
    	self.waveform.enableAutoRange()
    	
