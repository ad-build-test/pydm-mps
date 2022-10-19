from os import path
from pydm import Display

from pydm.widgets.checkbox import PyDMCheckbox
from pydm.widgets.slider import PyDMSlider

class LBLMmain(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(LBLMmain, self).__init__(parent=parent, args=args, macros=macros)

        self.gray_out()
        self.ui.bypass.toggled.connect(self.gray_out)
        """
        if bool(int(self.macros()["IS_WS"])):
            self.ui.vis_test.show()
        else:
            self.ui.vis_test.hide()
        """

    def gray_out(self):
        print(self.bypass.isChecked())
        print("gray_out test")
        if self.bypass.isChecked():
            self.gain_request_slid.setEnabled(False)
            self.gain_request_edit.setEnabled(False)
            print("false")
        else:
            self.gain_request_slid.setEnabled(True)
            self.gain_request_edit.setEnabled(True)
            print("True")

    @staticmethod
    def ui_filename():
        return 'test_waveform.ui'

    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())
