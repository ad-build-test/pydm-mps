from os import path
from pydm import Display

from pydm.widgets.checkbox import PyDMCheckbox
from pydm.widgets.slider import PyDMSlider

class LBLMmain(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(LBLMmain, self).__init__(parent=parent, args=args, macros=macros)

        self.bypass_gain_request()
        self.ws_visibility()
        self.ui.bypass.toggled.connect(self.bypass_gain_request)
        self.ui.freeze.toggled.connect(self.freeze_plot)


    def bypass_gain_request(self):
        """
        disables the gain request controls when the bypass box is checked
        """
        print(self.bypass.isChecked())
        print("bypass_gain_request test")
        if self.bypass.isChecked():
            self.gain_request_slid.setEnabled(False)
            self.gain_request_edit.setEnabled(False)
            print("false")
        else:
            self.gain_request_slid.setEnabled(True)
            self.gain_request_edit.setEnabled(True)
            print("True")

    def ws_visibility(self):
        """
        Hides and shows wirescaner specific widges
        """
        
        if bool(int(self.macros()["IS_WS"])):
            self.ui.ws_widgets.show()
        else:
            self.ui.ws_widgets.hide()
        


    def freeze_plot(self):
        print('Freezing plots')
        self.ui.PyDMWaveformPlot.pausePlotting()
        self.ui.PyDMWaveformPlot_2.pausePlotting()
        self.ui.PyDMWaveformPlot_3.pausePlotting()
        self.ui.PyDMWaveformPlot_4.pausePlotting()
        self.ui.PyDMWaveformPlot_5.pausePlotting()

    @staticmethod
    def ui_filename():
        return 'test_waveform.ui'

    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())
