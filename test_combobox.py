from os import path
from PyQt5.QtWidgets import QComboBox
from epics import caget, caput
from pydm import Display

class ComboBoxMacroSelector(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(ComboBoxMacroSelector, self).__init__(parent=parent, args=args, macros=macros)
        
        #self.ui.PyDMTimePlot.clearCurves()
        self.init_comboBox()
        self.read_comboBox()
#        self.write_macros()
        self.ui.comboBox.activated.connect(self.read_comboBox)

    def init_comboBox(self):
        #ca://BLEN:HTR:350:10:RWF_U16.VALA
        #get this list from macros probably, if it is just the name, we will need to append :FAST_WF to the end.
        lblm_list = ['-Select LBLM-', 'BLEN:HTR:350:10', 'ca://test2', 'ca://test3']
        self.ui.comboBox.addItems(lblm_list)

    def read_comboBox(self):

        self.prev_text = self.macros()['DEVICE']
        self.macros()['DEVICE'] = self.ui.comboBox.currentText()
        if self.macros()['DEVICE'] == '-Select LBLM-':
            print('Not Writing')
        else:
            self.write_macros()
        
    def write_macros(self):
        #self.ui.PyDMTimePlot.clearCurves() 
        print('writing')
        print(self.macros()['DEVICE'])
        #self.macros()['DEVICE'] = 'ca://' + self.text + ':RWF_U16.VALA'
        print(self.prev_text + ':RWF_U16.VALA') 
        #curve = self.ui.PyDMTimePlot.findCurve(self.prev_text + ':RWF_U16.VALA')
        #curve = self.ui.PyDMTimePlot.getCurves()
        #self.ui.PyDMTimePlot.refreshCurve(curve)
        #self.ui.PyDMTimePlot.set_needs_redraw()
        #self.ui.PyDMTimePlot.redrawPlot()
        #self.ui.PyDMTimePlot.addYChannel(self.text, plot_style='Line')
        #print(self.ui.PyDMTimePlot.getCurves())
        self.ui.PyDMEmbeddedDisplay._needs_load = True
        self.ui.PyDMEmbeddedDisplay.load_if_needed()
        #self.ui.PyDMTimePlot.createCurveItem(self.text, plot_style='Line')
        #self.ui.PyDMTimePlot._curves.address = self.text
        #print(self.ui.PyDMTimePlot.getCurves())
        #print(self.ui.PyDMTimePlot.channel)
        # when we write the macros, we need to remove the previous plot and add the new one.
        # might need to do this by keeping track of the index. if they select the one that is 
        # currently plotted, it ignores.
        #self.ui.PyDMTimePlot.addYChannel(self.text)
        #self.ui.PyDMTimePlot.channel = self.text

    @staticmethod
    def ui_filename():
        return 'test_combobox.ui'

    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())

