from os import path
from pydm import Display
from pyqtgraph import InfiniteLine
from pydm.widgets.channel import PyDMChannel

class WaveformPlot(Display):
  def __init__(self, parent=None, args=None):
    super(WaveformPlot, self).__init__(parent=parent, args=args)
    self.coarse_delay_line = InfiniteLine(pos=0, angle=90, movable=False,pen={'color': (218,243,186), 'width': 2})
    self.coarse_position_channel = PyDMChannel(address="ca://MPLN:BSYH:MP03:1:B0_C0_COARSE_DLY_SAM", value_slot=self.move_coarse)
    self.waveform.addItem(self.coarse_delay_line)
    self.coarse_position_channel.connect()

    self.peak_delay_line = InfiniteLine(pos=0, angle=90, movable=False,pen={'color': (11,135,161), 'width': 2})
    self.peak_position_channel = PyDMChannel(address="ca://MPLN:BSYH:MP03:1:LC1_ANA_PK_DEL_TRG_0_RBV", value_slot=self.move_peak)
    self.waveform.addItem(self.peak_delay_line)
    self.peak_position_channel.connect()

    self.peak_width_line = InfiniteLine(pos=0, angle=90, movable=False,pen={'color': (157,207,217), 'width': 2})
    self.peak_width_channel = PyDMChannel(address="ca://MPLN:BSYH:MP03:1:LC1_ANA_PK_WDT_TRG_0_RBV", value_slot=self.width_peak)
    self.waveform.addItem(self.peak_width_line)
    self.peak_width_channel.connect()

    self.ped_delay_line = InfiniteLine(pos=0, angle=90, movable=False,pen={'color': (223,116,237), 'width': 2})
    self.ped_position_channel = PyDMChannel(address="ca://MPLN:BSYH:MP03:1:LC1_ANA_PD_DEL_TRG_0_RBV", value_slot=self.move_ped)
    self.waveform.addItem(self.ped_delay_line)
    self.ped_position_channel.connect()

    self.ped_width_line = InfiniteLine(pos=0, angle=90, movable=False,pen={'color': (226,200,230), 'width': 2})
    self.ped_width_channel = PyDMChannel(address="ca://MPLN:BSYH:MP03:1:LC1_ANA_PD_WDT_TRG_0_RBV", value_slot=self.width_ped)
    self.waveform.addItem(self.ped_width_line)
    self.ped_width_channel.connect()

    self.coarse_val = 0
    self.peak_val = 0
    self.peak_width = 0
    self.ped_val = 0
    self.ped_width = 0


  def ui_filename(self):
      # Point to our UI file
      return 'WaveformDisp.ui'

  def ui_filepath(self):
      # Return the full path to the UI file
      return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())
  
  def move_coarse(self, new_line_value):
      self.coarse_val = new_line_value
      self.update_lines()     

  def move_peak(self, new_line_value):
    self.peak_val = new_line_value*2
    self.update_lines()

  def width_peak(self, new_line_value):
    self.peak_width = new_line_value*2
    self.update_lines()

  def move_ped(self, new_line_value):
    self.ped_val = new_line_value*2
    self.update_lines()

  def width_ped(self, new_line_value):
    self.ped_width = new_line_value*2
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


