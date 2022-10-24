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
        '''
        Query the MPS database for both all BLM devices and all waveform
        PVs. BLM devices are sorted by z-location.
        Author: Kyle Leleux (kleleux)
        '''
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
        '''
        Gets a list of all devices and parses out some repeats. 
        Devices ending in H and S provide the same waveform (???),
        so we remove repeated and remove the "BLM:" prefix.
        Author: Kyle Leleux (kleleux)
        ''' 
        self.all_lblms = []

        for dev in devices_db:

            if dev.name.find('LBLM') > -1:
                
                if dev.name.endswith('S'):
                    self.all_lblms.append(dev.name[4:-1])
                elif dev.name.endswith('A') or dev.name.endswith('B'):
                    self.all_lblms.append(dev.name[4:])

    def get_lblm_wf_list(self, lblms_wf_db):
        '''
        Gets the waveform pv list, which are only available for the LBLMs
        so we use this to label LBLMs and WS. Also, we remove the "WF:"
        from the string.
        Author: Kyle Leleux (kleleux)
        '''     
        self.lblm_wf_list = []
        
        for wf in lblms_wf_db:
            
            if wf.name.find('WF') > -1:
                self.lblm_wf_list.append(wf.name[3:])
                print(wf.name[3:])
    
    def get_lblm_type_list(self):
        '''
        Compares a list of non-LBLMs and tests it with the full device 
        list to label WS and LBLMs
        Author: Kyle Leleux (kleleux)
        '''
        self.lblm_type = []

        for dev in self.all_lblms:
            
            if dev in self.lblm_wf_list:
                self.lblm_type.append(0)
            else:
                self.lblm_type.append(1)
        
    def label_devices(self):
        '''
        Take the lblm_type list and use it to clearly label the WS devices
        on the display.
        Author: Kyle Leleux (kleleux)
        '''
        self.lblm_label_list = []
        
        for i, dev in enumerate(self.all_lblms):
            
            if self.lblm_type[i]:
                self.lblm_label_list.append(dev + " (WS)")
            else:
                self.lblm_label_list.append(dev)

    def init_comboBox(self):
        '''
        Launches the combobox whether macros are defined or not and 
        sets the navigation buttons accordingly.
        Author: Kyle Leleux (kleleux)
        ''' 
        self.ui.comboBox.addItems(self.lblm_label_list)
        if self.macros() == {}:
            # Note: This should not be done this way, but there is no setter. 
            #       A request has been made to the pydm team - KEL
            self._macros = {'DEVICE': None, 'IS_WS': self.lblm_type[self.ui.comboBox.currentIndex()]}
            # get index of item in all_lblm list
            print(self.macros())
        else:
            start_index = self.all_lblms.index(self.macros()['DEVICE'])
            self.ui.comboBox.setCurrentIndex(start_index)
            self.macros()['IS_WS'] = self.lblm_type[start_index]
        
        self.set_nav_buttons()

    def read_comboBox(self):
        self.macros()['DEVICE'] = self.all_lblms[self.ui.comboBox.currentIndex()]
        self.macros()['IS_WS'] = self.lblm_type[self.ui.comboBox.currentIndex()]
        
        print(self.macros()) 
        self.write_macros()
        
    def write_macros(self):
        '''
        Write the macros to the PyDMEmbeddedDisplay by reloading 
        the PyDMEmbeddedDisplay.
        Note: PyDM now has a feature that should be used in place of 
        loading it manually - KEL (10/21/22)
        Author: Kyle Leleux (kelelux)
        ''' 
        self.set_nav_buttons()

        print('writing')
        self.ui.PyDMEmbeddedDisplay._needs_load = True
        self.ui.PyDMEmbeddedDisplay.load_if_needed()

    def next_lblm(self):
        '''
        Increments the combobox index by 1 to move to the next device
        and reloads the embedded display to update the macros.
        Author: Kyle Leleux (kleleux)
        ''' 
        lblm_index = self.ui.comboBox.currentIndex()
        next_lblm = lblm_index + 1
        if next_lblm < self.ui.comboBox.count():
            self.ui.Next.setEnabled(True)
            self.ui.comboBox.setCurrentIndex(next_lblm)
            self.macros()['DEVICE'] = self.all_lblms[next_lblm]
            self.macros()['IS_WS'] = self.lblm_type[next_lblm]
            self.write_macros()

            self.set_nav_buttons()


    def prev_lblm(self):
        '''
        Decrements the combobox index by 1 to move to the previous device
        and reloads the embedded display to update the macros.
        Author: Kyle Leleux (kleleux)
        ''' 

        lblm_index = self.ui.comboBox.currentIndex()
        prev_lblm = lblm_index - 1
        if (prev_lblm) >= 0:
            self.ui.comboBox.setCurrentIndex(prev_lblm)
            self.macros()['DEVICE'] = self.all_lblms[prev_lblm]
            self.macros()['IS_WS'] = self.lblm_type[prev_lblm]
            self.write_macros()

            self.set_nav_buttons()
    
    def set_nav_buttons(self):
        '''
        Grays out the next or previous push buttons based on if the 
        combobox index is at the limits of the list.
        Author: Kyle Leleux (kleleux)
        ''' 
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

