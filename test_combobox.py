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
        self.get_lblms()
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
                print(self.db_file) 

    def get_lblm_type(self):
        #we want to query the database again, but this time we want all lblms
        #because we want to note which ones are lblms and which are wire scanners
        # lblms appear 4 times
        # ws appear 2
        # can use contains and make a list of these "types" 
        
        pass

    def get_lblms(self):
        
        #reader = MPSConfig(self.db_file)
        
        #reader = MpsDbReader(self.db_file)
        #dt = reader.session.query(models.DeviceType).filter(models.DeviceType.name=='BLM').one()
        self.lblms = []
        with MpsDbReader(self.db_file) as session:
              dt = session.query(models.DeviceType).filter(models.DeviceType.name=='BLM').one()
              print(dt)
              devices = session.query(models.Device).filter(models.Device.device_type_id==dt.id).all()
              for d in devices:
                  if d.name.find('LBLM') > -1:
                      self.lblms.append(d.name[4:])
                      print(d.name)
        #query the mps_database to get list of lblms

    def sort_lblms(self):
        #order by z position
        pass
    
    def init_comboBox(self):
        #ca://BLEN:HTR:350:10:RWF_U16.VALA
        #get this list from macros probably, if it is just the name, we will need to append :FAST_WF to the end.
        #lblm_list = ['-Select LBLM-', 'BLEN:HTR:350:10', 'ca://test2', 'ca://test3']
        self.ui.comboBox.addItems(self.lblms)
        
        #set previous button to disabled
        self.ui.Previous.setEnabled(False)

    def read_comboBox(self):
        #
        self.prev_text = self.macros()['DEVICE']
        self.macros()['DEVICE'] = self.ui.comboBox.currentText()
        if self.macros()['DEVICE'] == '-Select LBLM-' or None:
            print('Not Writing')
        else:
            self.write_macros()
        
    def write_macros(self):
        
        self.reset_nav_buttons()

        print('writing')
        print(self.macros()['DEVICE'])
        print(self.prev_text + ':RWF_U16.VALA') 
        self.ui.PyDMEmbeddedDisplay._needs_load = True
        self.ui.PyDMEmbeddedDisplay.load_if_needed()

    def next_lblm(self):
        
        lblm_index = self.ui.comboBox.currentIndex()
        next_lblm = lblm_index + 1
        if next_lblm < self.ui.comboBox.count():
            self.ui.Next.setEnabled(True)
            print(self.ui.comboBox.count())
            print(next_lblm)
            self.ui.comboBox.setCurrentIndex(next_lblm)
            self.macros()['DEVICE'] = self.lblms[next_lblm]
            self.write_macros()
            if next_lblm == (self.ui.comboBox.count()-1):
                self.ui.Next.setEnabled(False)

    def prev_lblm(self):

        lblm_index = self.ui.comboBox.currentIndex()
        prev_lblm = lblm_index - 1
        if (prev_lblm) >= 0:
            print(lblm_index)
            print(prev_lblm)
            self.ui.comboBox.setCurrentIndex(prev_lblm)
            self.macros()['DEVICE'] = self.lblms[prev_lblm]
            self.write_macros()
            if prev_lblm == 0:
                self.ui.Previous.setEnabled(False)

    def reset_nav_buttons(self):
        
        if self.ui.comboBox.currentIndex() < self.ui.comboBox.count() and self.ui.comboBox.currentIndex() > 0:
            self.ui.Next.setEnabled(True)
            self.ui.Previous.setEnabled(True)

    @staticmethod
    def ui_filename():
        return 'test_combobox.ui'

    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())

