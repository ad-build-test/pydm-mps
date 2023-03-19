from pydm import Display
from pydm.widgets.channel import PyDMChannel
from os import path

class ThresholdDisplayFormat(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(ThresholdDisplayFormat, self).__init__(parent=parent, args=args, macros=macros)
        self.slope = -1
        PV_slope = "ca://" + self.macros()['P'] + '_SS_RBV'
        #self.coarse_delay_val_nc = caget(self.macros()['DEVICE'] + ':NC_COARSE_DEL_RBV')
        self.slope_channel = PyDMChannel(address=PV_slope, value_slot=self.order_thresholds)
        self.slope_channel.connect()

        self.set_display_format()

        #self.order_thresholds()

    def order_thresholds(self, slope):
        '''
        Sets the threshold positioning to be consistent where the min
        and max still make sense when the slope is negative while keeping
        the overall display consistent. (See diagram below)

        When the slope is positive:
        Min -- Low Threshold
        Max -- High Threshold
        When the slope is negative:
        Min -- High Threshold
        Max -- Low Threshold
        The overall pv does not change functionality. 
        
        Author: Kyle Leleux (kleleux)
        '''
        if slope > 0:
            self.ui.min_ctrl.channel = 'ca://' + self.macros()['P'] + '_' + self.macros()['THR'] + '_L' 
            self.ui.min_rbv.channel = 'ca://' + self.macros()['P'] + '_' + self.macros()['THR'] + '_L_RBV' 
            self.ui.min_en.channel = 'ca://' + self.macros()['P'] + '_' + self.macros()['THR'] + '_L_EN' 
            self.ui.min_en_rbv.channel = 'ca://' + self.macros()['P'] + '_' + self.macros()['THR'] + '_L_EN_RBV' 
            self.ui.max_ctrl.channel = 'ca://' + self.macros()['P'] + '_' + self.macros()['THR'] + '_H' 
            self.ui.max_rbv.channel = 'ca://' + self.macros()['P'] + '_' + self.macros()['THR'] + '_H_RBV' 
            self.ui.max_en.channel = 'ca://' + self.macros()['P'] + '_' + self.macros()['THR'] + '_H_EN' 
            self.ui.max_en_rbv.channel = 'ca://' + self.macros()['P'] + '_' + self.macros()['THR'] + '_H_EN_RBV' 
        elif slope < 0:
            self.ui.min_ctrl.channel = 'ca://' + self.macros()['P'] + '_' + self.macros()['THR'] + '_H' 
            self.ui.min_rbv.channel = 'ca://' + self.macros()['P'] + '_' + self.macros()['THR'] + '_H_RBV' 
            self.ui.min_en.channel = 'ca://' + self.macros()['P'] + '_' + self.macros()['THR'] + '_H_EN' 
            self.ui.min_en_rbv.channel = 'ca://' + self.macros()['P'] + '_' + self.macros()['THR'] + '_H_EN_RBV' 
            self.ui.max_ctrl.channel = 'ca://' + self.macros()['P'] + '_' + self.macros()['THR'] + '_L' 
            self.ui.max_rbv.channel = 'ca://' + self.macros()['P'] + '_' + self.macros()['THR'] + '_L_RBV' 
            self.ui.max_en.channel = 'ca://' + self.macros()['P'] + '_' + self.macros()['THR'] + '_L_EN' 
            self.ui.max_en_rbv.channel = 'ca://' + self.macros()['P'] + '_' + self.macros()['THR'] + '_L_EN_RBV' 

    def set_display_format(self):
        if self.macros()['FORMAT'] == 'EXP':
            self.ui.min_ctrl.displayFormat = 3
            self.ui.min_rbv.displayFormat = 3
            self.ui.max_ctrl.displayFormat = 3
            self.ui.max_rbv.displayFormat = 3
        elif self.macros()['FORMAT'] == 'DEFAULT':
            self.ui.min_ctrl.displayFormat = 0
            self.ui.min_rbv.displayFormat = 0
            self.ui.max_ctrl.displayFormat = 0
            self.ui.max_rbv.displayFormat = 0
        else:
            pass
    @staticmethod
    def ui_filename():
        return 'mps_inline_threshold_rbv.ui'

    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())
