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

class CBLMSelector(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(CBLMSelector, self).__init__(parent=parent, args=args, macros=macros)
        
        self.load_database()
        self.get_sorted_cblms()
        self.init_comboBox()
        self.ui.comboBox.activated.connect(self.read_comboBox)
        self.ui.Next.clicked.connect(self.next_cblm)
        self.ui.Previous.clicked.connect(self.prev_cblm)
        self.read_comboBox()


    def load_database(self):
        '''
        Loading the most recent mps database
        Author: Kyle Leleux (kleleux)
        '''
        for file in listdir(environ.get("PHYSICS_TOP") + "/mps_configuration/current"):
            if file.endswith(".db"):
                self.db_file = environ.get("PHYSICS_TOP") + "/mps_configuration/current/" + file
                #should pass when found.
    
    def get_sorted_cblms(self):
        '''
        Query the MPS database for both all BLM devices and all waveform
        PVs. BLM devices are sorted by z-location.
        Author: Kyle Leleux (kleleux)
        '''
        with MpsDbReader(self.db_file) as session:
            dt_blm = session.query(models.DeviceType).filter(models.DeviceType.name=='BLM').one()
            #all_devices = session.query(models.Device).filter(models.Device.device_type_id==dt_blm.id).order_by(models.Device.z_location).all()
            all_devices = session.query(models.Device).filter(models.Device.device_type_id==dt_blm.id).order_by(models.Device.name).all()
            
            self.get_all_devices(all_devices)
  
            #self.get_cblm_wf_list(wf_cblms)

            #self.get_cblm_type_list()
            
            #self.label_devices()

    def get_all_devices(self, devices_db):
        '''
        Gets a list of all devices and parses out some repeats. 
        Devices ending in H and S provide the same waveform (???),
        so we remove repeated and remove the "BLM:" prefix.
        Author: Kyle Leleux (kleleux)
        ''' 
        self.all_cblms = []

        for dev in devices_db:

            if dev.name.find('CBLM') > -1:
                #TODO: Remove the BLM: from beginning to get the PV Name 
                self.all_cblms.append(dev.name[4:])
        print(self.all_cblms)

    def init_comboBox(self):
        '''
        Launches the combobox whether macros are defined or not and 
        sets the navigation buttons accordingly.
        Author: Kyle Leleux (kleleux)
        ''' 
        self.ui.comboBox.addItems(self.all_cblms)
        if self.macros() == {}:
            # Note: This should not be done this way, but there is no setter. 
            #       A request has been made to the pydm team - KEL
            #self._macros = {'DEVICE': None, 'IS_WS': self.cblm_type[self.ui.comboBox.currentIndex()]}
            self._macros = {"DEVICE": None}
            # get index of item in all_cblm list
        else:
            start_index = self.all_cblms.index(self.macros()["DEVICE"])
            self.ui.comboBox.setCurrentIndex(start_index)
            #self.macros()['IS_WS'] = self.cblm_type[start_index]
        
        self.set_nav_buttons()

    def read_comboBox(self):
        self.macros()["DEVICE"] = self.all_cblms[self.ui.comboBox.currentIndex()]
        #self.macros()['IS_WS'] = self.cblm_type[self.ui.comboBox.currentIndex()]
        
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

        self.ui.PyDMEmbeddedDisplay._needs_load = True
        self.ui.PyDMEmbeddedDisplay.load_if_needed()

    def next_cblm(self):
        '''
        Increments the combobox index by 1 to move to the next device
        and reloads the embedded display to update the macros.
        Author: Kyle Leleux (kleleux)
        ''' 
        cblm_index = self.ui.comboBox.currentIndex()
        next_cblm = cblm_index + 1
        if next_cblm < self.ui.comboBox.count():
            self.ui.Next.setEnabled(True)
            self.ui.comboBox.setCurrentIndex(next_cblm)
            self.macros()["DEVICE"] = self.all_cblms[next_cblm]
            #self.macros()['IS_WS'] = self.cblm_type[next_cblm]
            self.write_macros()

            self.set_nav_buttons()


    def prev_cblm(self):
        '''
        Decrements the combobox index by 1 to move to the previous device
        and reloads the embedded display to update the macros.
        Author: Kyle Leleux (kleleux)
        ''' 

        cblm_index = self.ui.comboBox.currentIndex()
        prev_cblm = cblm_index - 1
        if (prev_cblm) >= 0:
            self.ui.comboBox.setCurrentIndex(prev_cblm)
            self.macros()["DEVICE"] = self.all_cblms[prev_cblm]
            #self.macros()['IS_WS'] = self.cblm_type[prev_cblm]
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
        return 'cblm_global.ui'

    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())
