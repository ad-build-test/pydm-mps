import time
import yaml
import datetime
import sys
from os import path, listdir, environ
from PyQt5.QtWidgets import QComboBox, QPushButton
from epics import caget, caput
from pydm import Display
from mps_database.mps_config import MPSConfig, models, runtime
from mps_database.tools.mps_names import MpsName
from mps_database.tools.mps_reader import MpsDbReader
from sqlalchemy import MetaData

class ComboBoxMacroSelector(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(ComboBoxMacroSelector, self).__init__(parent=parent, args=args, macros=macros)
        
        self.lblm_selection = 0
        
        self.load_database()
        self.get_sorted_lblms()
        #self.ui.PyDMTimePlot.clearCurves()
        self.init_comboBox()
        self.read_comboBox()
#        self.write_macros()
        self.ui.comboBox.activated.connect(self.read_comboBox)
        self.ui.Next.clicked.connect(self.next_lblm)
        self.ui.Previous.clicked.connect(self.prev_lblm)

    def load_database(self):
        #first, find the path 
        for file in listdir(environ.get("PHYSICS_TOP") + "/mps_configuration/current"):
            if file.endswith(".db"):
                self.db_file = environ.get("PHYSICS_TOP") + "/mps_configuration/current/" + file

    def get_lblm_type(self):
        #we want to query the database again, but this time we want all lblms
        #because we want to note which ones are lblms and which are wire scanners
        # lblms appear 4 times
        # ws appear 2
        # can use contains and make a list of these "types" 
        
        pass

    def get_sorted_lblms(self):
        
        #reader = MPSConfig(self.db_file)
        
        #reader = MpsDbReader(self.db_file)
        #dt = reader.session.query(models.DeviceType).filter(models.DeviceType.name=='BLM').one()
        with MpsDbReader(self.db_file) as session:
            dt_blm = session.query(models.DeviceType).filter(models.DeviceType.name=='BLM').one()
            all_devices = session.query(models.Device).filter(models.Device.device_type_id==dt_blm.id).order_by(models.Device.z_location).all()
            dt_wf = session.query(models.DeviceType).filter(models.DeviceType.name=='WF').one()
            wf_lblms = session.query(models.Device).filter(models.Device.device_type_id==dt_wf.id).all()
            
            self.get_all_devices(all_devices)
  
            self.get_lblm_wf_list(wf_lblms)

            self.get_lblm_type_list()
            
            self.label_devices()

    def get_all_devices(self, devices_db):
        
        self.all_lblms = []

        for dev in devices_db:

            if dev.name.find('LBLM') > -1:
                
                if dev.name.endswith('S'):
                    self.all_lblms.append(dev.name[4:-1])
                elif dev.name.endswith('A') or dev.name.endswith('B'):
                    self.all_lblms.append(dev.name[4:])

    def get_lblm_wf_list(self, lblms_wf_db):
        
        self.lblm_wf_list = []
        
        for wf in lblms_wf_db:
            
            if wf.name.find('WF') > -1:
                self.lblm_wf_list.append(wf.name[3:])
                print(wf.name[3:])
        #for lblm in lblms:
        #    if lblm.name[3:] in self.all_lblms:
        #        #then it is not a ws
        #        ws_list.append(0)
        #    else:
        #        print(lblm.name[3:])
        #        #it is a ws
        #        ws_list.append(1)
    
    def get_lblm_type_list(self):
        self.lblm_type = []

        for dev in self.all_lblms:
            
            if dev in self.lblm_wf_list:
                self.lblm_type.append(0)
            else:
                self.lblm_type.append(1)
        
    def label_devices(self):
        self.lblm_label_list = []
        
        for i, dev in enumerate(self.all_lblms):
            
            if self.lblm_type[i]:
                self.lblm_label_list.append(dev + " (WS)")
            else:
                self.lblm_label_list.append(dev)

    def init_comboBox(self):
        #ca://BLEN:HTR:350:10:RWF_U16.VALA
        
        #get this list from macros probably, if it is just the name, we will need to append :FAST_WF to the end.
        #lblm_list = ['-Select LBLM-', 'BLEN:HTR:350:10', 'ca://test2', 'ca://test3']
        self.ui.comboBox.addItems(self.lblm_label_list)
        if self.macros()['DEVICE'] != 'None':
            start_index = self.all_lblms.index(self.macros()['DEVICE'])
            self.ui.comboBox.setCurrentIndex(start_index)
            # get index of item in all_lblm list
            # set the index in combobox
            # write_macros but might already be doing it.
            #start at the index of that item
        #set previous button to disabled
        self.set_nav_buttons()

    def read_comboBox(self):
        # Dont think im actually using prev_text
        #self.macros()['DEVICE'] = self.all_lblms[self.ui.comboBox.currentIndex()]
        #print(self.macros()['DEVICE'])
        self.macros()['IS_WS'] = self.lblm_type[self.ui.comboBox.currentIndex()]
        
        if self.macros()['DEVICE'] == '-Select LBLM-':
            print('Not Writing')
        else:
            self.write_macros()
        
    def write_macros(self):
        
        self.set_nav_buttons()

        print('writing')
        self.ui.PyDMEmbeddedDisplay._needs_load = True
        self.ui.PyDMEmbeddedDisplay.load_if_needed()

    def next_lblm(self):
        
        lblm_index = self.ui.comboBox.currentIndex()
        next_lblm = lblm_index + 1
        if next_lblm < self.ui.comboBox.count():
            self.ui.Next.setEnabled(True)
            self.ui.comboBox.setCurrentIndex(next_lblm)
            self.macros()['DEVICE'] = self.all_lblms[next_lblm]
            self.write_macros()

            self.set_nav_buttons()


    def prev_lblm(self):

        lblm_index = self.ui.comboBox.currentIndex()
        prev_lblm = lblm_index - 1
        if (prev_lblm) >= 0:
            self.ui.comboBox.setCurrentIndex(prev_lblm)
            self.macros()['DEVICE'] = self.all_lblms[prev_lblm]
            self.write_macros()

            self.set_nav_buttons()
    
    def set_nav_buttons(self):
        
        if self.ui.comboBox.currentIndex() < (self.ui.comboBox.count()-1):
            self.ui.Next.setEnabled(True)
        else:
            self.ui.Next.setEnabled(False)
        if self.ui.comboBox.currentIndex() > 0:
            self.ui.Previous.setEnabled(True)
        else:
            self.ui.Previous.setEnabled(False)

    @staticmethod
    def ui_filename():
        return 'test_combobox.ui'

    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())

