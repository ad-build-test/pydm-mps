from os import path
from pydm import Display
from pydm.widgets.channel import PyDMChannel
from mps_manager_protocol import *
from threshold_manager_client import ThresholdManagerClient
import socket

class AdjustThresholds(Display):
  def __init__(self, parent=None, args=None, macros=None):
    super(AdjustThresholds, self).__init__(parent=parent, args=args, macros=macros)
    if path.exists('/afs/slac/g/lcls'):
      self.host = 'lcls-dev1'
    else:
      self.host = 'lcls-daemon2'
    self.device = '{DEVICE}'.format(**macros)
    self.integrator = int('{INT}'.format(**macros))
    self.ui.DeviceName.setText('{0} Thresholds for Integrator {1}'.format(self.device, self.integrator))   
    self.display_current_thresholds()
    self.ui.ch_int.setText('{0}'.format(self.integrator))
    self.facilityPopulate()
    self.ui.ch_accl.activated.connect(self.changeFacility)
    self.ui.ch_doit.clicked.connect(self.doit)

    self.currentFacility = 0
    self.changeFacility(self.currentFacility)   
    

  def ui_filename(self):
      # Point to our UI file
      return 'AdjustThresholds.ui'

  def ui_filepath(self):
      # Return the full path to the UI file
      return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())

  def display_current_thresholds(self):
    tm = ThresholdManagerClient(host=self.host,port=1975)
    if (tm.check_device(-1, self.device, int(MpsManagerRequestType.GET_THRESHOLD.value))==False):
      exit(2)
    t = tm.get_thresholds()
    self.ui.lc1Lo.setText('{0}'.format(self.extract_threshold(0,self.integrator,t.lc1_value,t.lc1_active)))
    self.ui.lc1Hi.setText('{0}'.format(self.extract_threshold(1,self.integrator,t.lc1_value,t.lc1_active)))
    t_count = len(t.lc2_value)/2
    self.ui.lc2_t0_lo.setText('{0}'.format(self.extract_threshold(0,self.integrator,t.lc2_value,t.lc2_active)))
    self.ui.lc2_t1_lo.setText('{0}'.format(self.extract_threshold(1,self.integrator,t.lc2_value,t.lc2_active)))
    self.ui.lc2_t2_lo.setText('{0}'.format(self.extract_threshold(2,self.integrator,t.lc2_value,t.lc2_active)))
    self.ui.lc2_t3_lo.setText('{0}'.format(self.extract_threshold(3,self.integrator,t.lc2_value,t.lc2_active)))
    self.ui.lc2_t4_lo.setText('{0}'.format(self.extract_threshold(4,self.integrator,t.lc2_value,t.lc2_active)))
    self.ui.lc2_t5_lo.setText('{0}'.format(self.extract_threshold(5,self.integrator,t.lc2_value,t.lc2_active)))
    self.ui.lc2_t6_lo.setText('{0}'.format(self.extract_threshold(6,self.integrator,t.lc2_value,t.lc2_active)))
    self.ui.lc2_t0_hi.setText('{0}'.format(self.extract_threshold(t_count+0,self.integrator,t.lc2_value,t.lc2_active)))
    self.ui.lc2_t1_hi.setText('{0}'.format(self.extract_threshold(t_count+1,self.integrator,t.lc2_value,t.lc2_active)))
    self.ui.lc2_t2_hi.setText('{0}'.format(self.extract_threshold(t_count+2,self.integrator,t.lc2_value,t.lc2_active)))
    self.ui.lc2_t3_hi.setText('{0}'.format(self.extract_threshold(t_count+3,self.integrator,t.lc2_value,t.lc2_active)))
    self.ui.lc2_t4_hi.setText('{0}'.format(self.extract_threshold(t_count+4,self.integrator,t.lc2_value,t.lc2_active)))
    self.ui.lc2_t5_hi.setText('{0}'.format(self.extract_threshold(t_count+5,self.integrator,t.lc2_value,t.lc2_active)))
    self.ui.lc2_t6_hi.setText('{0}'.format(self.extract_threshold(t_count+6,self.integrator,t.lc2_value,t.lc2_active)))
     

  def extract_threshold(self,threshold, integrator, values, active):
    if active[threshold][integrator]:
       return values[threshold][integrator]
    else:
       return "Not Active"
  
  def facilityPopulate(self):
    self.ui.ch_accl.addItem('NC') #0
    self.ui.ch_accl.addItem('SC') #1
    self.ui.ch_lohi.addItem('Low Threshold') #0
    self.ui.ch_lohi.addItem('High Threshold') #1
    self.ui.ch_active.addItem('Active') #0
    self.ui.ch_active.addItem('Deactivate') #1

  def changeFacility(self, facl):
    self.currentFacility = facl
    self.updateThresh()

  def updateThresh(self):
    self.ui.ch_thresh.clear()
    if self.currentFacility == 0:
        self.ui.ch_thresh.addItem('T0')
    elif self.currentFacility == 1:
        self.ui.ch_thresh.addItem('T0')
        self.ui.ch_thresh.addItem('T1')
        self.ui.ch_thresh.addItem('T2')
        self.ui.ch_thresh.addItem('T3')
        self.ui.ch_thresh.addItem('T4')
        self.ui.ch_thresh.addItem('T5')
        self.ui.ch_thresh.addItem('T6')
    else:
        self.ui.ch_thresh.addItem("Choose Facility")

  def doit(self):
    self.OutputText("Changing Threshold for {0}, please wait...".format(self.device))
    cfacility = self.ui.ch_accl.currentText()
    cint = 'i{0}'.format(self.ui.ch_int.text())
    cthresh = self.ui.ch_thresh.currentText().lower()
    clohi = self.ui.ch_lohi.currentText()
    cnewValue = self.ui.ch_newValue.text()
    cactive = self.ui.ch_active.currentText()
    name = self.ui.ch_name.text()
    reason = self.ui.ch_reason.text()
    proceed = False
    try:
      float(cnewValue)
      proceed = True
    except ValueError:
      self.OutputText('Error: Please enter a valid number for new threshold value')
    if not name:
        self.OutputText("Error: Please enter your username")
        proceed = False
    if not reason:
        proceed = False
        self.OutputText("Error: Please enter a reason")
    if cfacility == "NC":
        table = 'lc1'
    elif cfacility == "SC":
        table = 'lc2'
    else:
        table = ""   
    if clohi == "Low Threshold":
        newlo = "lolo"
    elif clohi == "High Threshold":
        newlo = "hihi"
    else:
        newlo = ""
    if cactive == "Active":
      act = False
    elif cactive == "Deactivate":
      act = True
    else:
      self.OutputText("Could not understand active command")
    if proceed:
        tm = ThresholdManagerClient(host=self.host,port=1975)
        if(tm.build_threshold_table_py(table, cthresh, cint, newlo, cnewValue) == False):
          self.OutputText("ERROR BUILDING THRESHOLD TABLE")
        if( tm.check_device(-1, self.device, int(MpsManagerRequestType.CHANGE_THRESHOLD.value)) == False):
          self.OutputText("ERROR: DEVICE NOT VALID")
        if( tm.change_thresholds(str(name), str(reason), -1, self.device, act) == False):
          self.OutputText("ERROR CHANGING THRESHOLD")
        else:
          self.OutputText("Threshold changed successfully")
        self.display_current_thresholds()
    self.ui.ch_reason.setText("")
    self.ui.ch_name.setText("")
    
  def OutputText(self, text):
    self.ui.output_text.setText(text)    
