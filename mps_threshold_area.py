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

class ThresholdSetup(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(ThresholdSetup, self).__init__(parent=parent, args=args, macros=macros)

        self.setup_tabs()

    def setup_tabs(self):
        self.setup_blm_tab()
        self.setup_bpm_tab()
        self.setup_bcm_tab()
        self.setup_magnet_tab()

    def setup_blm_tab(self):
        '''
        Checks if the blm JSON object contains information, hides the tab if not
        Author: Kyle Leleux (kleleux)
        '''
        # Checking to see if the JSON dictionary is empty
        if not(self.ui.PyDMTemplateRepeater.data):
            self.tabWidget.setTabEnabled(0, False)

    def setup_bpm_tab(self):
        '''
        Checks if the bpm JSON object contains information, hides the tab if not
        Author: Kyle Leleux (kleleux)
        '''
        # Checking to see if the JSON dictionary is empty
        if not(self.ui.PyDMTemplateRepeater_2.data):
            self.tabWidget.setTabEnabled(1, False)

    def setup_bcm_tab(self):
        '''
        Checks if the bcm/blen JSON object contains information, hides the tab if not
        Author: Kyle Leleux (kleleux)
        '''
        # Checking to see if the JSON dictionary is empty
        if not(self.ui.PyDMTemplateRepeater_3.data):
            self.tabWidget.setTabEnabled(2, False)

    def setup_magnet_tab(self):
        '''
        Checks if the magnet JSON object contains information, hides the tab if not
        Author: Kyle Leleux (kleleux)
        '''
        # Checking to see if the JSON dictionary is empty
        if not(self.ui.PyDMTemplateRepeater_4.data):
            self.tabWidget.setTabEnabled(3, False)

    @staticmethod
    def ui_filename():
        return 'mps_threshold_area.ui'

    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())
