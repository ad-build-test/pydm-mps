from os import path
from pydm import Display
from epics import caget
import time
from pydm.widgets.slider import PyDMSlider
from pydm.widgets.label import PyDMLabel
from pyqtgraph import InfiniteLine
from pydm.widgets.channel import PyDMChannel
import numpy as np


class CBLMmain(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(CBLMmain, self).__init__(parent=parent, args=args, macros=macros)

        self.scale_plots()
        self.initialize_plots()
        self.connect_line_edit()
        #self.init_gain_request()
        self.connect_checkboxes()

        #self.ws_visibility()
        #self.ui.freeze.toggled.connect(self.freeze_plot)
        self.mode = 0
        """
        Initializing a bunch of stuff for having the plots display in time instead of raw counts
        Author: Ryan McClanahan
        """
    
    def scale_plots(self):

        self.jesd_clock = 175.4
        self.ns_spacing = self.jesd_clock* 2 * 1e6 / 1e9
        print(self.macros())
        PV_raw_buf = "ca://" + self.macros()["DEVICE"] + ":FAST_WF_RAW-BUF.NELM"
        self.num_points_channel_raw_buf = PyDMChannel(address=PV_raw_buf, value_slot=self.num_points_raw_buf_change)
        self.num_points_channel_raw_buf.connect()

        self.main_raw_buf = self.MainRawBuf.curveAtIndex(0)
        self.raw_buf = self.RawBuf.curveAtIndex(0)

        #PV_raw = "ca://{DEVICE}:FAST_WF_RAW.NELM".format(**macros)
        #self.num_points_channel_raw = PyDMChannel(address=PV_raw, value_slot=self.num_points_raw_change)
        #self.num_points_channel_raw.connect()

        #self.main_raw = self.MainRaw.curveAtIndex(0)
        #self.raw = self.Raw.curveAtIndex(0)

        #PV_egu = "ca://{DEVICE}:FAST_WF.NELM".format(**macros)
        #self.num_points_channel_egu = PyDMChannel(address=PV_egu, value_slot=self.num_points_egu_change)
        #self.num_points_channel_egu.connect()

        #self.main_egu = self.MainEgu.curveAtIndex(0)
        #self.egu = self.Egu.curveAtIndex(0)
        """
        End of Initializing a bunch of stuff for having the plots display in time instead of raw counts
        Author: Ryan McClanahan
        """

    def initialize_plots(self):
        # TODO: READ MODE. do i set it up like in line 42?
        #self.mode =
        self.initialize_coarse_delay()
        self.initialize_peak_delay()
        self.initialize_peak_width()
        self.initialize_pedestal_delay()
        self.initialize_pedestal_width()

    def connect_line_edit(self):
        self.ui.coarse_delay_sc.returnPressed.connect(self.update_coarse_delay)
        self.ui.peak_delay_sc.returnPressed.connect(self.update_peak_delay)
        self.ui.peak_width_sc.returnPressed.connect(self.update_peak_width)
        self.ui.pedestal_delay_sc.returnPressed.connect(self.update_pedestal_delay)
        self.ui.pedestal_width_sc.returnPressed.connect(self.update_pedestal_width)
        self.ui.coarse_delay_nc.returnPressed.connect(self.update_coarse_delay)
        self.ui.peak_delay_nc.returnPressed.connect(self.update_peak_delay)
        self.ui.peak_width_nc.returnPressed.connect(self.update_peak_width)
        self.ui.pedestal_delay_nc.returnPressed.connect(self.update_pedestal_delay)
        self.ui.pedestal_width_nc.returnPressed.connect(self.update_pedestal_width)

    def connect_checkboxes(self):
        self.ui.coarse_delay_vis.toggled.connect(self.toggle_coarse_delay_visibility)
        self.ui.peak_delay_vis.toggled.connect(self.toggle_peak_delay_visibility)
        self.ui.peak_width_vis.toggled.connect(self.toggle_peak_width_visibility)
        self.ui.pedestal_delay_vis.toggled.connect(self.toggle_pedestal_delay_visibility)
        self.ui.pedestal_width_vis.toggled.connect(self.toggle_pedestal_width_visibility)
        self.ui.lcls_mode.toggled.connect(self.switch_mode)

    def initialize_coarse_delay(self):
        #self.peak_delay = caget(self.macros['DEVICE'] + ':NC_ANA_PK_DEL_TRG')
        # TODO: GET DELAY VALUE FOR SPECIFIC MODE - KEL
        #if self.mode = 0:
        #    self.coarse_delay_val = 
        #else:
        #    self.coarse_delay_val = 
        self.coarse_delay_val = 15000
        coarse_delay_color = (153,0,0)
        self.coarse_delay_curve1 = InfiniteLine(self.coarse_delay_val, angle=90, pen={'color': coarse_delay_color, 'width':2, 'dash': [2,4]})
        self.coarse_delay_curve2 = InfiniteLine(self.coarse_delay_val, angle=90, pen={'color': coarse_delay_color, 'width':2, 'dash': [2,4]})
        self.coarse_delay_curve3 = InfiniteLine(self.coarse_delay_val, angle=90, pen={'color': coarse_delay_color, 'width':2, 'dash': [2,4]})
        self.coarse_delay_curve4 = InfiniteLine(self.coarse_delay_val, angle=90, pen={'color': coarse_delay_color, 'width':2, 'dash': [2,4]})
        self.coarse_delay_curve5 = InfiniteLine(self.coarse_delay_val, angle=90, pen={'color': coarse_delay_color, 'width':2, 'dash': [2,4]})
        self.coarse_delay_curve6 = InfiniteLine(self.coarse_delay_val, angle=90, pen={'color': coarse_delay_color, 'width':2, 'dash': [2,4]})
        self.ui.MainRawBuf.curveAtIndex(0).getViewBox().addItem(self.coarse_delay_curve1)
        self.ui.MainRaw.curveAtIndex(0).getViewBox().addItem(self.coarse_delay_curve2)
        self.ui.MainEgu.curveAtIndex(0).getViewBox().addItem(self.coarse_delay_curve3)
        self.ui.RawBuf.curveAtIndex(0).getViewBox().addItem(self.coarse_delay_curve4)
        self.ui.Raw.curveAtIndex(0).getViewBox().addItem(self.coarse_delay_curve5)
        self.ui.Egu.curveAtIndex(0).getViewBox().addItem(self.coarse_delay_curve6)

    def initialize_peak_delay(self):
        #self.peak_delay = caget(self.macros['DEVICE'] + ':NC_ANA_PK_DEL_TRG')
        # TODO: GET DELAY VALUE FOR SPECIFIC MODE - KEL
        #if self.mode = 0:
        #    self.peak_delay_val = 
        #else:
        #    self.peak_delay_val = 
        self.peak_delay_val = self.coarse_delay_val + 15000
        peak_delay_color = (0,102,0)
        self.peak_delay_curve1 = InfiniteLine(self.ui.peak_delay_val, angle=90, pen={'color': peak_delay_color, 'width':2, 'dash': [2,4]})
        self.peak_delay_curve2 = InfiniteLine(self.ui.peak_delay_val, angle=90, pen={'color': peak_delay_color, 'width':2, 'dash': [2,4]})
        self.peak_delay_curve3 = InfiniteLine(self.ui.peak_delay_val, angle=90, pen={'color': peak_delay_color, 'width':2, 'dash': [2,4]})
        self.peak_delay_curve4 = InfiniteLine(self.ui.peak_delay_val, angle=90, pen={'color': peak_delay_color, 'width':2, 'dash': [2,4]})
        self.peak_delay_curve5 = InfiniteLine(self.ui.peak_delay_val, angle=90, pen={'color': peak_delay_color, 'width':2, 'dash': [2,4]})
        self.peak_delay_curve6 = InfiniteLine(self.ui.peak_delay_val, angle=90, pen={'color': peak_delay_color, 'width':2, 'dash': [2,4]})
        self.ui.MainRawBuf.curveAtIndex(0).getViewBox().addItem(self.peak_delay_curve1)
        self.ui.MainRaw.curveAtIndex(0).getViewBox().addItem(self.peak_delay_curve2)
        self.ui.MainEgu.curveAtIndex(0).getViewBox().addItem(self.peak_delay_curve3)
        self.ui.RawBuf.curveAtIndex(0).getViewBox().addItem(self.peak_delay_curve4)
        self.ui.Raw.curveAtIndex(0).getViewBox().addItem(self.peak_delay_curve5)
        self.ui.Egu.curveAtIndex(0).getViewBox().addItem(self.peak_delay_curve6)

    def initialize_peak_width(self):
        #self.peak_delay = caget(self.macros['DEVICE'] + ':NC_ANA_PK_DEL_TRG')
        # TODO: GET DELAY VALUE FOR SPECIFIC MODE - KEL
        #if self.mode = 0:
        #    self.peak_width_val = 
        #else:
        #    self.peak_width_val = 
        self.peak_width_val = self.peak_delay_val + 16000
        peak_width_color = (0,76,153)
        self.peak_width_curve1 = InfiniteLine(self.ui.peak_width_val, angle=90, pen={'color': peak_width_color, 'width':2, 'dash': [2,4]})
        self.peak_width_curve2 = InfiniteLine(self.ui.peak_width_val, angle=90, pen={'color': peak_width_color, 'width':2, 'dash': [2,4]})
        self.peak_width_curve3 = InfiniteLine(self.ui.peak_width_val, angle=90, pen={'color': peak_width_color, 'width':2, 'dash': [2,4]})
        self.peak_width_curve4 = InfiniteLine(self.ui.peak_width_val, angle=90, pen={'color': peak_width_color, 'width':2, 'dash': [2,4]})
        self.peak_width_curve5 = InfiniteLine(self.ui.peak_width_val, angle=90, pen={'color': peak_width_color, 'width':2, 'dash': [2,4]})
        self.peak_width_curve6 = InfiniteLine(self.ui.peak_width_val, angle=90, pen={'color': peak_width_color, 'width':2, 'dash': [2,4]})
        self.ui.MainRawBuf.curveAtIndex(0).getViewBox().addItem(self.peak_width_curve1)
        self.ui.MainRaw.curveAtIndex(0).getViewBox().addItem(self.peak_width_curve2)
        self.ui.MainEgu.curveAtIndex(0).getViewBox().addItem(self.peak_width_curve3)
        self.ui.RawBuf.curveAtIndex(0).getViewBox().addItem(self.peak_width_curve4)
        self.ui.Raw.curveAtIndex(0).getViewBox().addItem(self.peak_width_curve5)
        self.ui.Egu.curveAtIndex(0).getViewBox().addItem(self.peak_width_curve6)

    def initialize_pedestal_delay(self):
        #self.peak_delay = caget(self.macros['DEVICE'] + ':NC_ANA_PK_DEL_TRG')
        # TODO: GET DELAY VALUE FOR SPECIFIC MODE - KEL
        #if self.mode = 0:
        #    self.pedestal_delay_val = 
        #else:
        #    self.pedestal_delay_val = 
        self.pedestal_delay_val = self.peak_width_val + 15500
        pedestal_delay_color = (153,0,153)
        self.pedestal_delay_curve1 = InfiniteLine(self.ui.pedestal_delay_val, angle=90, pen={'color': pedestal_delay_color, 'width':2, 'dash': [2,4]})
        self.pedestal_delay_curve2 = InfiniteLine(self.ui.pedestal_delay_val, angle=90, pen={'color': pedestal_delay_color, 'width':2, 'dash': [2,4]})
        self.pedestal_delay_curve3 = InfiniteLine(self.ui.pedestal_delay_val, angle=90, pen={'color': pedestal_delay_color, 'width':2, 'dash': [2,4]})
        self.pedestal_delay_curve4 = InfiniteLine(self.ui.pedestal_delay_val, angle=90, pen={'color': pedestal_delay_color, 'width':2, 'dash': [2,4]})
        self.pedestal_delay_curve5 = InfiniteLine(self.ui.pedestal_delay_val, angle=90, pen={'color': pedestal_delay_color, 'width':2, 'dash': [2,4]})
        self.pedestal_delay_curve6 = InfiniteLine(self.ui.pedestal_delay_val, angle=90, pen={'color': pedestal_delay_color, 'width':2, 'dash': [2,4]})
        self.ui.MainRawBuf.curveAtIndex(0).getViewBox().addItem(self.pedestal_delay_curve1)
        self.ui.MainRaw.curveAtIndex(0).getViewBox().addItem(self.pedestal_delay_curve2)
        self.ui.MainEgu.curveAtIndex(0).getViewBox().addItem(self.pedestal_delay_curve3)
        self.ui.RawBuf.curveAtIndex(0).getViewBox().addItem(self.pedestal_delay_curve4)
        self.ui.Raw.curveAtIndex(0).getViewBox().addItem(self.pedestal_delay_curve5)
        self.ui.Egu.curveAtIndex(0).getViewBox().addItem(self.pedestal_delay_curve6)
    
    def initialize_pedestal_width(self):
        #self.peak_delay = caget(self.macros['DEVICE'] + ':NC_ANA_PK_DEL_TRG')
        # TODO: GET DELAY VALUE FOR SPECIFIC MODE - KEL
        #if self.mode = 0:
        #    self.pedestal_width_val = 
        #else:
        #    self.pedestal_width_val = 
        # TODO: GET VALUE FROM PYDM CHANNEL
        self.pedestal_width_val = self.pedestal_delay_val + 15000
        pedestal_width_color = (204,102,0)
        self.pedestal_width_curve1 = InfiniteLine(self.ui.pedestal_width_val, angle=90, pen={'color': pedestal_width_color, 'width':2, 'dash': [2,4]})
        self.pedestal_width_curve2 = InfiniteLine(self.ui.pedestal_width_val, angle=90, pen={'color': pedestal_width_color, 'width':2, 'dash': [2,4]})
        self.pedestal_width_curve3 = InfiniteLine(self.ui.pedestal_width_val, angle=90, pen={'color': pedestal_width_color, 'width':2, 'dash': [2,4]})
        self.pedestal_width_curve4 = InfiniteLine(self.ui.pedestal_width_val, angle=90, pen={'color': pedestal_width_color, 'width':2, 'dash': [2,4]})
        self.pedestal_width_curve5 = InfiniteLine(self.ui.pedestal_width_val, angle=90, pen={'color': pedestal_width_color, 'width':2, 'dash': [2,4]})
        self.pedestal_width_curve6 = InfiniteLine(self.ui.pedestal_width_val, angle=90, pen={'color': pedestal_width_color, 'width':2, 'dash': [2,4]})
        self.ui.MainRawBuf.curveAtIndex(0).getViewBox().addItem(self.pedestal_width_curve1)
        self.ui.MainRaw.curveAtIndex(0).getViewBox().addItem(self.pedestal_width_curve2)
        self.ui.MainEgu.curveAtIndex(0).getViewBox().addItem(self.pedestal_width_curve3)
        self.ui.RawBuf.curveAtIndex(0).getViewBox().addItem(self.pedestal_width_curve4)
        self.ui.Raw.curveAtIndex(0).getViewBox().addItem(self.pedestal_width_curve5)
        self.ui.Egu.curveAtIndex(0).getViewBox().addItem(self.pedestal_width_curve6)

    def update_coarse_delay(self):
        # TODO: dont know which mode is which now. find out what is 1 and what is 0 -KEL

        if self.mode == 0:
            self.coarse_delay_val = int(self.ui.coarse_delay_nc.text()) 
            self.coarse_delay_curve1.setValue(str(self.coarse_delay_val))
            self.coarse_delay_curve2.setValue(str(self.coarse_delay_val))
            self.coarse_delay_curve3.setValue(str(self.coarse_delay_val))
            self.coarse_delay_curve4.setValue(str(self.coarse_delay_val))
            self.coarse_delay_curve5.setValue(str(self.coarse_delay_val))
            self.coarse_delay_curve6.setValue(str(self.coarse_delay_val))
        else:
            self.coarse_delay_val = int(self.ui.coarse_delay_sc.text()) 
            self.coarse_delay_curve1.setValue(str(self.coarse_delay_val))
            self.coarse_delay_curve2.setValue(str(self.coarse_delay_val))
            self.coarse_delay_curve3.setValue(str(self.coarse_delay_val))
            self.coarse_delay_curve4.setValue(str(self.coarse_delay_val))
            self.coarse_delay_curve5.setValue(str(self.coarse_delay_val))
            self.coarse_delay_curve6.setValue(str(self.coarse_delay_val))
        print(self.coarse_delay_val)
        self.update_peak_delay()

    def update_peak_delay(self):

        if self.mode == 0:
            self.peak_delay_val = int(self.ui.peak_delay_nc.text()) + self.coarse_delay_val
            self.peak_delay_curve1.setValue(str(self.peak_delay_val))
            self.peak_delay_curve2.setValue(str(self.peak_delay_val))
            self.peak_delay_curve3.setValue(str(self.peak_delay_val))
            self.peak_delay_curve4.setValue(str(self.peak_delay_val))
            self.peak_delay_curve5.setValue(str(self.peak_delay_val))
            self.peak_delay_curve6.setValue(str(self.peak_delay_val))
        else:
            self.peak_delay_val = int(self.ui.peak_delay_sc.text()) + self.coarse_delay_val
            self.peak_delay_curve1.setValue(str(self.peak_delay_val))
            self.peak_delay_curve2.setValue(str(self.peak_delay_val))
            self.peak_delay_curve3.setValue(str(self.peak_delay_val))
            self.peak_delay_curve4.setValue(str(self.peak_delay_val))
            self.peak_delay_curve5.setValue(str(self.peak_delay_val))
            self.peak_delay_curve6.setValue(str(self.peak_delay_val))
           
        print(self.peak_delay_val)
        self.update_peak_width()
    
    def update_peak_width(self):

        if self.mode == 0:
            self.peak_width_val = int(self.ui.peak_width_nc.text()) + self.peak_delay_val
            self.peak_width_curve1.setValue(str(self.peak_width_val))
            self.peak_width_curve2.setValue(str(self.peak_width_val))
            self.peak_width_curve3.setValue(str(self.peak_width_val))
            self.peak_width_curve4.setValue(str(self.peak_width_val))
            self.peak_width_curve5.setValue(str(self.peak_width_val))
            self.peak_width_curve6.setValue(str(self.peak_width_val))
        else:
            self.peak_width_val = int(self.ui.peak_width_sc.text()) + self.peak_delay_val
            self.peak_width_curve1.setValue(str(self.peak_width_val))
            self.peak_width_curve2.setValue(str(self.peak_width_val))
            self.peak_width_curve3.setValue(str(self.peak_width_val))
            self.peak_width_curve4.setValue(str(self.peak_width_val))
            self.peak_width_curve5.setValue(str(self.peak_width_val))
            self.peak_width_curve6.setValue(str(self.peak_width_val))

        print(self.peak_width_val)
        self.update_pedestal_delay()
    
    def update_pedestal_delay(self):
        
        if self.mode == 0:
            self.pedestal_delay_val = int(self.ui.pedestal_delay_nc.text()) + self.coarse_delay_val
            self.pedestal_delay_curve1.setValue(str(self.pedestal_delay_val))
            self.pedestal_delay_curve2.setValue(str(self.pedestal_delay_val))
            self.pedestal_delay_curve3.setValue(str(self.pedestal_delay_val))
            self.pedestal_delay_curve4.setValue(str(self.pedestal_delay_val))
            self.pedestal_delay_curve5.setValue(str(self.pedestal_delay_val))
            self.pedestal_delay_curve6.setValue(str(self.pedestal_delay_val))
        else:
            self.pedestal_delay_val = int(self.ui.pedestal_delay_sc.text()) + self.coarse_delay_val
            self.pedestal_delay_curve1.setValue(str(self.pedestal_delay_val))
            self.pedestal_delay_curve2.setValue(str(self.pedestal_delay_val))
            self.pedestal_delay_curve3.setValue(str(self.pedestal_delay_val))
            self.pedestal_delay_curve4.setValue(str(self.pedestal_delay_val))
            self.pedestal_delay_curve5.setValue(str(self.pedestal_delay_val))
            self.pedestal_delay_curve6.setValue(str(self.pedestal_delay_val))
        
        print(self.pedestal_delay_val)
        self.update_pedestal_width()

    def update_pedestal_width(self):
        
        if self.mode == 0:
            self.pedestal_width_val = int(self.ui.peak_width_nc.text()) + self.pedestal_delay_val
            self.pedestal_width_curve1.setValue(str(self.pedestal_width_val))
            self.pedestal_width_curve2.setValue(str(self.pedestal_width_val))
            self.pedestal_width_curve3.setValue(str(self.pedestal_width_val))
            self.pedestal_width_curve4.setValue(str(self.pedestal_width_val))
            self.pedestal_width_curve5.setValue(str(self.pedestal_width_val))
            self.pedestal_width_curve6.setValue(str(self.pedestal_width_val))
        else:
            self.pedestal_width_val = int(self.ui.peak_width_sc.text()) + self.pedestal_delay_val
            self.pedestal_width_curve1.setValue(str(self.pedestal_width_val))
            self.pedestal_width_curve2.setValue(str(self.pedestal_width_val))
            self.pedestal_width_curve3.setValue(str(self.pedestal_width_val))
            self.pedestal_width_curve4.setValue(str(self.pedestal_width_val))
            self.pedestal_width_curve5.setValue(str(self.pedestal_width_val))
            self.pedestal_width_curve6.setValue(str(self.pedestal_width_val))

        print(self.pedestal_width_val)

    def toggle_coarse_delay_visibility(self):

        if self.ui.coarse_delay_vis.isChecked():
            self.ui.MainRawBuf.curveAtIndex(0).getViewBox().addItem(self.coarse_delay_curve1)
            self.ui.MainRaw.curveAtIndex(0).getViewBox().addItem(self.coarse_delay_curve2)
            self.ui.MainEgu.curveAtIndex(0).getViewBox().addItem(self.coarse_delay_curve3)
            self.ui.RawBuf.curveAtIndex(0).getViewBox().addItem(self.coarse_delay_curve4)
            self.ui.Raw.curveAtIndex(0).getViewBox().addItem(self.coarse_delay_curve5)
            self.ui.Egu.curveAtIndex(0).getViewBox().addItem(self.coarse_delay_curve6)
        else:   
            self.ui.MainRawBuf.curveAtIndex(0).getViewBox().removeItem(self.coarse_delay_curve1)
            self.ui.MainRaw.curveAtIndex(0).getViewBox().removeItem(self.coarse_delay_curve2)
            self.ui.MainEgu.curveAtIndex(0).getViewBox().removeItem(self.coarse_delay_curve3)
            self.ui.RawBuf.curveAtIndex(0).getViewBox().removeItem(self.coarse_delay_curve4)
            self.ui.Raw.curveAtIndex(0).getViewBox().removeItem(self.coarse_delay_curve5)
            self.ui.Egu.curveAtIndex(0).getViewBox().removeItem(self.coarse_delay_curve6)

    def toggle_peak_delay_visibility(self):
        #TODO: Should check whether it is already plotted as well.
        if self.ui.peak_delay_vis.isChecked():
            self.ui.MainRawBuf.curveAtIndex(0).getViewBox().addItem(self.peak_delay_curve1)
            self.ui.MainRaw.curveAtIndex(0).getViewBox().addItem(self.peak_delay_curve2)
            self.ui.MainEgu.curveAtIndex(0).getViewBox().addItem(self.peak_delay_curve3)
            self.ui.RawBuf.curveAtIndex(0).getViewBox().addItem(self.peak_delay_curve4)
            self.ui.Raw.curveAtIndex(0).getViewBox().addItem(self.peak_delay_curve5)
            self.ui.Egu.curveAtIndex(0).getViewBox().addItem(self.peak_delay_curve6)
        else:   
            self.ui.MainRawBuf.curveAtIndex(0).getViewBox().removeItem(self.peak_delay_curve1)
            self.ui.MainRaw.curveAtIndex(0).getViewBox().removeItem(self.peak_delay_curve2)
            self.ui.MainEgu.curveAtIndex(0).getViewBox().removeItem(self.peak_delay_curve3)
            self.ui.RawBuf.curveAtIndex(0).getViewBox().removeItem(self.peak_delay_curve4)
            self.ui.Raw.curveAtIndex(0).getViewBox().removeItem(self.peak_delay_curve5)
            self.ui.Egu.curveAtIndex(0).getViewBox().removeItem(self.peak_delay_curve6)

    def toggle_peak_width_visibility(self):
        #TODO: Should check whether it is already plotted as well.
        if self.ui.peak_width_vis.isChecked():
            self.ui.MainRawBuf.curveAtIndex(0).getViewBox().addItem(self.peak_width_curve1)
            self.ui.MainRaw.curveAtIndex(0).getViewBox().addItem(self.peak_width_curve2)
            self.ui.MainEgu.curveAtIndex(0).getViewBox().addItem(self.peak_width_curve3)
            self.ui.RawBuf.curveAtIndex(0).getViewBox().addItem(self.peak_width_curve4)
            self.ui.Raw.curveAtIndex(0).getViewBox().addItem(self.peak_width_curve5)
            self.ui.Egu.curveAtIndex(0).getViewBox().addItem(self.peak_width_curve6)
        else:   
            self.ui.MainRawBuf.curveAtIndex(0).getViewBox().removeItem(self.peak_width_curve1)
            self.ui.MainRaw.curveAtIndex(0).getViewBox().removeItem(self.peak_width_curve2)
            self.ui.MainEgu.curveAtIndex(0).getViewBox().removeItem(self.peak_width_curve3)
            self.ui.RawBuf.curveAtIndex(0).getViewBox().removeItem(self.peak_width_curve4)
            self.ui.Raw.curveAtIndex(0).getViewBox().removeItem(self.peak_width_curve5)
            self.ui.Egu.curveAtIndex(0).getViewBox().removeItem(self.peak_width_curve6)

    def toggle_pedestal_delay_visibility(self):
        #TODO: Should check whether it is already plotted as well.
        if self.ui.pedestal_delay_vis.isChecked():
            self.ui.MainRawBuf.curveAtIndex(0).getViewBox().addItem(self.pedestal_delay_curve1)
            self.ui.MainRaw.curveAtIndex(0).getViewBox().addItem(self.pedestal_delay_curve2)
            self.ui.MainEgu.curveAtIndex(0).getViewBox().addItem(self.pedestal_delay_curve3)
            self.ui.RawBuf.curveAtIndex(0).getViewBox().addItem(self.pedestal_delay_curve4)
            self.ui.Raw.curveAtIndex(0).getViewBox().addItem(self.pedestal_delay_curve5)
            self.ui.Egu.curveAtIndex(0).getViewBox().addItem(self.pedestal_delay_curve6)
        else:   
            self.ui.MainRawBuf.curveAtIndex(0).getViewBox().removeItem(self.pedestal_delay_curve1)
            self.ui.MainRaw.curveAtIndex(0).getViewBox().removeItem(self.pedestal_delay_curve2)
            self.ui.MainEgu.curveAtIndex(0).getViewBox().removeItem(self.pedestal_delay_curve3)
            self.ui.RawBuf.curveAtIndex(0).getViewBox().removeItem(self.pedestal_delay_curve4)
            self.ui.Raw.curveAtIndex(0).getViewBox().removeItem(self.pedestal_delay_curve5)
            self.ui.Egu.curveAtIndex(0).getViewBox().removeItem(self.pedestal_delay_curve6)

    def toggle_pedestal_width_visibility(self):
        #TODO: Should check whether it is already plotted as well.
        if self.ui.pedestal_width_vis.isChecked():
            self.ui.MainRawBuf.curveAtIndex(0).getViewBox().addItem(self.pedestal_width_curve1)
            self.ui.MainRaw.curveAtIndex(0).getViewBox().addItem(self.pedestal_width_curve2)
            self.ui.MainEgu.curveAtIndex(0).getViewBox().addItem(self.pedestal_width_curve3)
            self.ui.RawBuf.curveAtIndex(0).getViewBox().addItem(self.pedestal_width_curve4)
            self.ui.Raw.curveAtIndex(0).getViewBox().addItem(self.pedestal_width_curve5)
            self.ui.Egu.curveAtIndex(0).getViewBox().addItem(self.pedestal_width_curve6)
        else:   
            self.ui.MainRawBuf.curveAtIndex(0).getViewBox().removeItem(self.pedestal_width_curve1)
            self.ui.MainRaw.curveAtIndex(0).getViewBox().removeItem(self.pedestal_width_curve2)
            self.ui.MainEgu.curveAtIndex(0).getViewBox().removeItem(self.pedestal_width_curve3)
            self.ui.RawBuf.curveAtIndex(0).getViewBox().removeItem(self.pedestal_width_curve4)
            self.ui.Raw.curveAtIndex(0).getViewBox().removeItem(self.pedestal_width_curve5)
            self.ui.Egu.curveAtIndex(0).getViewBox().removeItem(self.pedestal_width_curve6)

    def switch_mode(self):
        # fetch readback value and call update value with mode:
        # TODO: need to initialize with mode as well
        #       need to gray out disabled mode

        self.mode = self.ui.lcls_mode.isChecked()
        self.switch_mode_display()
        self.update_coarse_delay()
        self.update_peak_delay()
        self.updated_peak_width()
        self.update_pedestal_delay()
        self.update_pedestal_width()
    
    def switch_mode_display(self):
        
        self.ui.coarse_delay_nc.setEnabled(not(self.mode))
        self.ui.peak_delay_nc.setEnabled(not(self.mode))
        self.ui.peak_width_nc.setEnabled(not(self.mode))
        self.ui.pedestal_delay_nc.setEnabled(not(self.mode))
        self.ui.pedestal_width_nc.setEnabled(not(self.mode))
        self.ui.coarse_delay_nc_rbv.setEnabled(not(self.mode))
        self.ui.peak_delay_nc_rbv.setEnabled(not(self.mode))
        self.ui.peak_width_nc_rbv.setEnabled(not(self.mode))
        self.ui.pedestal_delay_nc_rbv.setEnabled(not(self.mode))
        self.ui.pedestal_width_nc_rbv.setEnabled(not(self.mode))
        self.ui.coarse_delay_sc.setEnabled(self.mode)
        self.ui.peak_delay_sc.setEnabled(self.mode)
        self.ui.peak_width_sc.setEnabled(self.mode)
        self.ui.pedestal_delay_sc.setEnabled(self.mode)
        self.ui.pedestal_width_sc.setEnabled(self.mode)
        self.ui.coarse_delay_sc_rbv.setEnabled(self.mode)
        self.ui.peak_delay_sc_rbv.setEnabled(self.mode)
        self.ui.peak_width_sc_rbv.setEnabled(self.mode)
        self.ui.pedestal_delay_sc_rbv.setEnabled(self.mode)
        self.ui.pedestal_width_sc_rbv.setEnabled(self.mode)


    def num_points_egu_change(self, new_point_value):
        self.num_points_egu = new_point_value
        self.newXaxisEgu()
 
    def newXaxisEgu(self):
        start = 0
        stop = self.num_points_egu / self.ns_spacing
        x_axis_waveform = np.linspace(start, stop, int(self.num_points_egu))
        self.main_egu.receiveXWaveform(x_axis_waveform)
        self.egu.receiveXWaveform(x_axis_waveform)
 
    def num_points_raw_change(self, new_point_value):
        self.num_points_raw = new_point_value
        self.newXaxisRaw()
 
    def newXaxisRaw(self):
        start = 0
        stop = self.num_points_raw / self.ns_spacing
        x_axis_waveform = np.linspace(start, stop, int(self.num_points_raw))
        self.main_raw.receiveXWaveform(x_axis_waveform)
        self.raw.receiveXWaveform(x_axis_waveform)
 
    def num_points_raw_buf_change(self, new_point_value):
 
        self.num_points_raw_buf = new_point_value
        self.newXaxisRawBuf()
 
    def newXaxisRawBuf(self):
        start = 0
        stop = self.num_points_raw_buf / self.ns_spacing
        x_axis_waveform = np.linspace(start, stop, int(self.num_points_raw_buf))
        self.main_raw_buf.receiveXWaveform(x_axis_waveform)
        self.raw_buf.receiveXWaveform(x_axis_waveform)
 
 
    def init_gain_request(self):
        '''
        Fixes bug on startup that causes mismatch with gain slider being enabled or disabled.
        Normal enabling and disabling is done through pydm rules. 
        Author: Kyle Leleux
        '''
        self.ui.gain_request_edit.check_enable_state = lambda: None
        self.ui.gain_request_slid.check_enable_state = lambda: None
        self.ui.gain_request_slid.set_enable_state = lambda: None
        self.ui.gain_request_slid._slider.setEnabled(False)
        
    def ws_visibility(self):
        """
        Hides and shows wirescaner specific widges
        """
        
        if bool(int(self.macros()["IS_WS"])):
            self.ui.ws_widgets.show()
        else:
            self.ui.ws_widgets.hide()
        
 
 
    def freeze_plot(self):
        self.ui.MainRawBuf.pausePlotting()
        self.ui.RawBuf.pausePlotting()
        self.ui.MainRaw.pausePlotting()
        self.ui.Raw.pausePlotting()
        self.ui.MainEgu.pausePlotting()
        self.ui.Egu.pausePlotting()
 

    @staticmethod
    def ui_filename():
        return '_cblm_global_waveform.ui'

    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())
