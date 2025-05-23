from os import path
from pydm import Display
from epics import caget
import time
from pydm.widgets.slider import PyDMSlider
from pydm.widgets.label import PyDMLabel
from pyqtgraph import InfiniteLine
from pydm.widgets.channel import PyDMChannel
import numpy as np

#TODO: Come up with better color pallette - Kyle Leleux (kleleux 08/24/23)

class CBLMmain(Display):
    def __init__(self, parent=None, args=[], macros=None):
        super(CBLMmain, self).__init__(parent=parent, args=args, macros=macros)
        self.called = 0
        self.initialize = 1
        self.initialize_coarse_delay_flag = 1 
        self.initialize_peak_delay_flag = 1 
        self.initialize_peak_width_flag = 1 
        self.initialize_pedestal_delay_flag = 1 
        self.initialize_pedestal_width_flag = 1 
        self.initialize_cursor_start_flag = 1 
        self.initialize_cursor_end_flag = 1 

        self.scale_plots()
        self.connect_mode()
        self.connect_plot_channels()
        #self.init_gain_request()
        self.connect_checkboxes()
        self.connect_cursor_line_edit()
        self.initialize_cursor_plots()
        self.switch_mode_display()

        """
        Initializing a bunch of stuff for having the plots display in time instead of raw counts
        Author: Ryan McClanahan
        """
    
    def connect_mode(self):
        PV_mode = "ca://" + self.macros()['IOC'] + ':FACMODE_RBV'
        self.mode = caget(self.macros()['IOC'] + ':FACMODE_RBV')
        self.mode_channel = PyDMChannel(address=PV_mode, value_slot=self.switch_mode)
        self.mode_channel.connect()
        #self.switch_mode_display()
    
    def connect_plot_channels(self):
        '''
        Connects all of the channels used in infinite lines.
        Author: Kyle Leleux
        '''
        #Loading the Normal-conducting Channels
        PV_coarse_delay_nc = "ca://" + self.macros()['DEVICE'] + ':NC_COARSE_DEL_RBV'
        self.coarse_delay_val_nc = caget(self.macros()['DEVICE'] + ':NC_COARSE_DEL_RBV')
        self.coarse_delay_nc_channel = PyDMChannel(address=PV_coarse_delay_nc, value_slot=self.update_coarse_delay_val_nc)
        self.coarse_delay_nc_channel.connect()
        
        PV_peak_delay_nc = "ca://" + self.macros()['DEVICE'] + ':NC_ANA_PK_DEL_TRG_RBV'
        self.peak_delay_val_nc = caget(self.macros()['DEVICE'] + ':NC_ANA_PK_DEL_TRG_RBV')
        self.peak_delay_nc_channel = PyDMChannel(address=PV_peak_delay_nc, value_slot=self.update_peak_delay_val_nc)
        self.peak_delay_nc_channel.connect()
        
        PV_peak_width_nc = "ca://" + self.macros()['DEVICE'] + ':NC_ANA_PK_WDT_TRG_RBV'
        self.peak_width_val_nc = caget(self.macros()['DEVICE'] + ':NC_ANA_PK_WDT_TRG_RBV')
        self.peak_width_nc_channel = PyDMChannel(address=PV_peak_width_nc, value_slot=self.update_peak_width_val_nc)
        self.peak_width_nc_channel.connect()
        
        PV_pedestal_delay_nc = "ca://" + self.macros()['DEVICE'] + ':NC_ANA_PD_DEL_TRG_RBV'
        self.pedestal_delay_val_nc = caget(self.macros()['DEVICE'] + ':NC_ANA_PD_DEL_TRG_RBV')
        self.pedestal_delay_nc_channel = PyDMChannel(address=PV_pedestal_delay_nc, value_slot=self.update_pedestal_delay_val_nc)
        self.pedestal_delay_nc_channel.connect()
        
        PV_pedestal_width_nc = "ca://" + self.macros()['DEVICE'] + ':NC_ANA_PD_WDT_TRG_RBV'
        self.pedestal_width_val_nc = caget(self.macros()['DEVICE'] + ':NC_ANA_PD_WDT_TRG_RBV')
        self.pedestal_width_nc_channel = PyDMChannel(address=PV_pedestal_width_nc, value_slot=self.update_pedestal_width_val_nc)
        self.pedestal_width_nc_channel.connect()
        
        # Loading the Super-conducting Channels
        PV_coarse_delay_sc = "ca://" + self.macros()['DEVICE'] + ':SC_COARSE_DEL_RBV'
        self.coarse_delay_val_sc = caget(self.macros()['DEVICE'] + ':SC_COARSE_DEL_RBV')
        self.coarse_delay_sc_channel = PyDMChannel(address=PV_coarse_delay_sc, value_slot=self.update_coarse_delay_val_sc)
        self.coarse_delay_sc_channel.connect()
        
        PV_peak_delay_sc = "ca://" + self.macros()['DEVICE'] + ':SC_ANA_PK_DEL_TRG_RBV'
        self.peak_delay_val_sc = caget(self.macros()['DEVICE'] + ':SC_ANA_PK_DEL_TRG_RBV')
        self.peak_delay_sc_channel = PyDMChannel(address=PV_peak_delay_sc, value_slot=self.update_peak_delay_val_sc)
        self.peak_delay_sc_channel.connect()
        
        PV_peak_width_sc = "ca://" + self.macros()['DEVICE'] + ':SC_ANA_PK_WDT_TRG_RBV'
        self.peak_width_val_sc = caget(self.macros()['DEVICE'] + ':SC_ANA_PK_WDT_TRG_RBV')
        self.peak_width_sc_channel = PyDMChannel(address=PV_peak_width_sc, value_slot=self.update_peak_width_val_sc)
        self.peak_width_sc_channel.connect()
        
        PV_pedestal_delay_sc = "ca://" + self.macros()['DEVICE'] + ':SC_ANA_PD_DEL_TRG_RBV'
        self.pedestal_delay_val_sc = caget(self.macros()['DEVICE'] + ':SC_ANA_PD_DEL_TRG_RBV')
        self.pedestal_delay_sc_channel = PyDMChannel(address=PV_pedestal_delay_sc, value_slot=self.update_pedestal_delay_val_sc)
        self.pedestal_delay_sc_channel.connect()
        
        PV_pedestal_width_sc = "ca://" + self.macros()['DEVICE'] + ':SC_ANA_PD_WDT_TRG_RBV'
        self.pedestal_width_val_sc = caget(self.macros()['DEVICE'] + ':SC_ANA_PD_WDT_TRG_RBV')
        self.pedestal_width_sc_channel = PyDMChannel(address=PV_pedestal_width_sc, value_slot=self.update_pedestal_width_val_sc)
        self.pedestal_width_sc_channel.connect()

        self.cursor_start_val = 0
        self.cursor_end_val = 0
        self.ui.cursor_start.setText(str(self.cursor_start_val))
        self.ui.cursor_end.setText(str(self.cursor_end_val))

    def scale_plots(self):

        self.jesd_clock = 175.4
        self.ns_spacing = self.jesd_clock* 2 * 1e6 / 1e9
        #self.ns_spacing = 1
        PV_raw_buf = "ca://" + self.macros()["DEVICE"] + ":FAST_WF_RAW-BUF.NELM"
        PV_raw_buf = "ca://" + self.macros()["DEVICE"] + ":MPS_WF_RAW-BUF.NELM"
        self.num_points_channel_raw_buf = PyDMChannel(address=PV_raw_buf, value_slot=self.num_points_raw_buf_change)
        self.num_points_channel_raw_buf.connect()

        self.main_raw_buf = self.MainRawBuf.curveAtIndex(0)
        self.raw_buf = self.RawBuf.curveAtIndex(0)

        #PV_raw = "ca://{DEVICE}:MPS_WF_RAW.NELM".format(**macros)
        #self.num_points_channel_raw = PyDMChannel(address=PV_raw, value_slot=self.num_points_raw_change)
        #self.num_points_channel_raw.connect()

        #self.main_raw = self.MainRaw.curveAtIndex(0)
        #self.raw = self.Raw.curveAtIndex(0)

        #PV_egu = "ca://{DEVICE}:MPS_WF.NELM".format(**macros)
        #self.num_points_channel_egu = PyDMChannel(address=PV_egu, value_slot=self.num_points_egu_change)
        #self.num_points_channel_egu.connect()

        #self.main_egu = self.MainEgu.curveAtIndex(0)
        #self.egu = self.Egu.curveAtIndex(0)
        """
        End of Initializing a bunch of stuff for having the plots display in time instead of raw counts
        Author: Ryan McClanahan
        """

    def initialize_cursor_plots(self):
        # TODO: READ MODE. do i set it up like in line 42?
        #self.mode =
        #self.initialize_coarse_delay()
        #self.initialize_peak_delay()
        #self.initialize_peak_width()
        #self.initialize_pedestal_delay()
        #self.initialize_pedestal_width()
        self.update_cursor_start()
        self.update_cursor_end()
        self.set_cursor_start_invisible()
        self.set_cursor_end_invisible()

    def connect_cursor_line_edit(self):
        # Won't need once using channels - KEL
        #self.ui.coarse_delay_sc.returnPressed.connect(self.update_coarse_delay)
        #self.ui.peak_delay_sc.returnPressed.connect(self.update_peak_delay)
        #self.ui.peak_width_sc.returnPressed.connect(self.update_peak_width)
        #self.ui.pedestal_delay_sc.returnPressed.connect(self.update_pedestal_delay)
        #self.ui.pedestal_width_sc.returnPressed.connect(self.update_pedestal_width)
        #self.ui.coarse_delay_nc.returnPressed.connect(self.update_coarse_delay)
        #self.ui.peak_delay_nc.returnPressed.connect(self.update_peak_delay)
        #self.ui.peak_width_nc.returnPressed.connect(self.update_peak_width)
        #self.ui.pedestal_delay_nc.returnPressed.connect(self.update_pedestal_delay)
        #self.ui.pedestal_width_nc.returnPressed.connect(self.update_pedestal_width)
        self.ui.cursor_start.returnPressed.connect(self.update_cursor_start)
        self.ui.cursor_end.returnPressed.connect(self.update_cursor_end)

    def connect_checkboxes(self):
        self.ui.coarse_delay_vis.toggled.connect(self.toggle_coarse_delay_visibility)
        self.ui.peak_delay_vis.toggled.connect(self.toggle_peak_delay_visibility)
        self.ui.peak_width_vis.toggled.connect(self.toggle_peak_width_visibility)
        self.ui.pedestal_delay_vis.toggled.connect(self.toggle_pedestal_delay_visibility)
        self.ui.pedestal_width_vis.toggled.connect(self.toggle_pedestal_width_visibility)
        self.ui.cursor_start_vis.toggled.connect(self.toggle_cursor_start_visibility)
        self.ui.cursor_end_vis.toggled.connect(self.toggle_cursor_end_visibility)
        self.ui.freeze.toggled.connect(self.freeze_plot)

    def initialize_coarse_delay(self, coarse_delay_val):
        #self.peak_delay = caget(self.macros['DEVICE'] + ':NC_ANA_PK_DEL_TRG')
        # TODO: GET DELAY VALUE FOR SPECIFIC MODE - KEL
        #if self.mode = 0:
        #    self.coarse_delay_val = 
        #else:
        #    self.coarse_delay_val = 
        coarse_delay_color = (153,0,0)
        self.coarse_delay_curve1 = InfiniteLine(coarse_delay_val, angle=90, pen={'color': coarse_delay_color, 'width':2, 'dash': [2,4]})
        self.coarse_delay_curve2 = InfiniteLine(coarse_delay_val, angle=90, pen={'color': coarse_delay_color, 'width':2, 'dash': [2,4]})
        self.coarse_delay_curve3 = InfiniteLine(coarse_delay_val, angle=90, pen={'color': coarse_delay_color, 'width':2, 'dash': [2,4]})
        self.coarse_delay_curve4 = InfiniteLine(coarse_delay_val, angle=90, pen={'color': coarse_delay_color, 'width':2, 'dash': [2,4]})
        self.coarse_delay_curve5 = InfiniteLine(coarse_delay_val, angle=90, pen={'color': coarse_delay_color, 'width':2, 'dash': [2,4]})
        self.coarse_delay_curve6 = InfiniteLine(coarse_delay_val, angle=90, pen={'color': coarse_delay_color, 'width':2, 'dash': [2,4]})
        self.ui.MainRawBuf.curveAtIndex(0).getViewBox().addItem(self.coarse_delay_curve1)
        self.ui.MainRaw.curveAtIndex(0).getViewBox().addItem(self.coarse_delay_curve2)
        self.ui.MainEgu.curveAtIndex(0).getViewBox().addItem(self.coarse_delay_curve3)
        self.ui.RawBuf.curveAtIndex(0).getViewBox().addItem(self.coarse_delay_curve4)
        self.ui.Raw.curveAtIndex(0).getViewBox().addItem(self.coarse_delay_curve5)
        self.ui.Egu.curveAtIndex(0).getViewBox().addItem(self.coarse_delay_curve6)

    def initialize_peak_delay(self, peak_delay_val):
        #self.peak_delay = caget(self.macros['DEVICE'] + ':NC_ANA_PK_DEL_TRG')
        # TODO: GET DELAY VALUE FOR SPECIFIC MODE - KEL
        #if self.mode = 0:
        #    self.peak_delay_val = 
        #else:
        #    self.peak_delay_val = 
        peak_delay_color = (0,102,0)
        self.peak_delay_curve1 = InfiniteLine(peak_delay_val, angle=90, pen={'color': peak_delay_color, 'width':2, 'dash': [2,4]})
        self.peak_delay_curve2 = InfiniteLine(peak_delay_val, angle=90, pen={'color': peak_delay_color, 'width':2, 'dash': [2,4]})
        self.peak_delay_curve3 = InfiniteLine(peak_delay_val, angle=90, pen={'color': peak_delay_color, 'width':2, 'dash': [2,4]})
        self.peak_delay_curve4 = InfiniteLine(peak_delay_val, angle=90, pen={'color': peak_delay_color, 'width':2, 'dash': [2,4]})
        self.peak_delay_curve5 = InfiniteLine(peak_delay_val, angle=90, pen={'color': peak_delay_color, 'width':2, 'dash': [2,4]})
        self.peak_delay_curve6 = InfiniteLine(peak_delay_val, angle=90, pen={'color': peak_delay_color, 'width':2, 'dash': [2,4]})
        self.ui.MainRawBuf.curveAtIndex(0).getViewBox().addItem(self.peak_delay_curve1)
        self.ui.MainRaw.curveAtIndex(0).getViewBox().addItem(self.peak_delay_curve2)
        self.ui.MainEgu.curveAtIndex(0).getViewBox().addItem(self.peak_delay_curve3)
        self.ui.RawBuf.curveAtIndex(0).getViewBox().addItem(self.peak_delay_curve4)
        self.ui.Raw.curveAtIndex(0).getViewBox().addItem(self.peak_delay_curve5)
        self.ui.Egu.curveAtIndex(0).getViewBox().addItem(self.peak_delay_curve6)

    def initialize_peak_width(self, peak_width_val):
        #self.peak_delay = caget(self.macros['DEVICE'] + ':NC_ANA_PK_DEL_TRG')
        # TODO: GET DELAY VALUE FOR SPECIFIC MODE - KEL
        #if self.mode = 0:
        #    self.peak_width_val = 
        #else:
        #    self.peak_width_val = 
        peak_width_color = (0,76,153)
        self.peak_width_curve1 = InfiniteLine(peak_width_val, angle=90, pen={'color': peak_width_color, 'width':2, 'dash': [2,4]})
        self.peak_width_curve2 = InfiniteLine(peak_width_val, angle=90, pen={'color': peak_width_color, 'width':2, 'dash': [2,4]})
        self.peak_width_curve3 = InfiniteLine(peak_width_val, angle=90, pen={'color': peak_width_color, 'width':2, 'dash': [2,4]})
        self.peak_width_curve4 = InfiniteLine(peak_width_val, angle=90, pen={'color': peak_width_color, 'width':2, 'dash': [2,4]})
        self.peak_width_curve5 = InfiniteLine(peak_width_val, angle=90, pen={'color': peak_width_color, 'width':2, 'dash': [2,4]})
        self.peak_width_curve6 = InfiniteLine(peak_width_val, angle=90, pen={'color': peak_width_color, 'width':2, 'dash': [2,4]})
        self.ui.MainRawBuf.curveAtIndex(0).getViewBox().addItem(self.peak_width_curve1)
        self.ui.MainRaw.curveAtIndex(0).getViewBox().addItem(self.peak_width_curve2)
        self.ui.MainEgu.curveAtIndex(0).getViewBox().addItem(self.peak_width_curve3)
        self.ui.RawBuf.curveAtIndex(0).getViewBox().addItem(self.peak_width_curve4)
        self.ui.Raw.curveAtIndex(0).getViewBox().addItem(self.peak_width_curve5)
        self.ui.Egu.curveAtIndex(0).getViewBox().addItem(self.peak_width_curve6)

    def initialize_pedestal_delay(self, pedestal_delay_val):
        pedestal_delay_color = (153,0,153)
        self.pedestal_delay_curve1 = InfiniteLine(pedestal_delay_val, angle=90, pen={'color': pedestal_delay_color, 'width':2, 'dash': [2,4]})
        self.pedestal_delay_curve2 = InfiniteLine(pedestal_delay_val, angle=90, pen={'color': pedestal_delay_color, 'width':2, 'dash': [2,4]})
        self.pedestal_delay_curve3 = InfiniteLine(pedestal_delay_val, angle=90, pen={'color': pedestal_delay_color, 'width':2, 'dash': [2,4]})
        self.pedestal_delay_curve4 = InfiniteLine(pedestal_delay_val, angle=90, pen={'color': pedestal_delay_color, 'width':2, 'dash': [2,4]})
        self.pedestal_delay_curve5 = InfiniteLine(pedestal_delay_val, angle=90, pen={'color': pedestal_delay_color, 'width':2, 'dash': [2,4]})
        self.pedestal_delay_curve6 = InfiniteLine(pedestal_delay_val, angle=90, pen={'color': pedestal_delay_color, 'width':2, 'dash': [2,4]})
        self.ui.MainRawBuf.curveAtIndex(0).getViewBox().addItem(self.pedestal_delay_curve1)
        self.ui.MainRaw.curveAtIndex(0).getViewBox().addItem(self.pedestal_delay_curve2)
        self.ui.MainEgu.curveAtIndex(0).getViewBox().addItem(self.pedestal_delay_curve3)
        self.ui.RawBuf.curveAtIndex(0).getViewBox().addItem(self.pedestal_delay_curve4)
        self.ui.Raw.curveAtIndex(0).getViewBox().addItem(self.pedestal_delay_curve5)
        self.ui.Egu.curveAtIndex(0).getViewBox().addItem(self.pedestal_delay_curve6)
    
    def initialize_pedestal_width(self, pedestal_width_val):
        pedestal_width_color = (204,102,0)
        self.pedestal_width_curve1 = InfiniteLine(pedestal_width_val, angle=90, pen={'color': pedestal_width_color, 'width':2, 'dash': [2,4]})
        self.pedestal_width_curve2 = InfiniteLine(pedestal_width_val, angle=90, pen={'color': pedestal_width_color, 'width':2, 'dash': [2,4]})
        self.pedestal_width_curve3 = InfiniteLine(pedestal_width_val, angle=90, pen={'color': pedestal_width_color, 'width':2, 'dash': [2,4]})
        self.pedestal_width_curve4 = InfiniteLine(pedestal_width_val, angle=90, pen={'color': pedestal_width_color, 'width':2, 'dash': [2,4]})
        self.pedestal_width_curve5 = InfiniteLine(pedestal_width_val, angle=90, pen={'color': pedestal_width_color, 'width':2, 'dash': [2,4]})
        self.pedestal_width_curve6 = InfiniteLine(pedestal_width_val, angle=90, pen={'color': pedestal_width_color, 'width':2, 'dash': [2,4]})
        self.ui.MainRawBuf.curveAtIndex(0).getViewBox().addItem(self.pedestal_width_curve1)
        self.ui.MainRaw.curveAtIndex(0).getViewBox().addItem(self.pedestal_width_curve2)
        self.ui.MainEgu.curveAtIndex(0).getViewBox().addItem(self.pedestal_width_curve3)
        self.ui.RawBuf.curveAtIndex(0).getViewBox().addItem(self.pedestal_width_curve4)
        self.ui.Raw.curveAtIndex(0).getViewBox().addItem(self.pedestal_width_curve5)
        self.ui.Egu.curveAtIndex(0).getViewBox().addItem(self.pedestal_width_curve6)

    def initialize_cursor_start(self, cursor_start_val):
        #TODO: can set these as moveable but will need to grab the value it moves to. -Kyle Leleux (kleleux 08/24/23)
        cursor_start_color = (0,0,0)
        self.cursor_start_curve1 = InfiniteLine(cursor_start_val, angle=90, pen={'color': cursor_start_color, 'width':2, 'dash': [2,4]})
        self.cursor_start_curve2 = InfiniteLine(cursor_start_val, angle=90, pen={'color': cursor_start_color, 'width':2, 'dash': [2,4]})
        self.cursor_start_curve3 = InfiniteLine(cursor_start_val, angle=90, pen={'color': cursor_start_color, 'width':2, 'dash': [2,4]})
        self.cursor_start_curve4 = InfiniteLine(cursor_start_val, angle=90, pen={'color': cursor_start_color, 'width':2, 'dash': [2,4]})
        self.cursor_start_curve5 = InfiniteLine(cursor_start_val, angle=90, pen={'color': cursor_start_color, 'width':2, 'dash': [2,4]})
        self.cursor_start_curve6 = InfiniteLine(cursor_start_val, angle=90, pen={'color': cursor_start_color, 'width':2, 'dash': [2,4]})
        self.ui.MainRawBuf.curveAtIndex(0).getViewBox().addItem(self.cursor_start_curve1)
        self.ui.MainRaw.curveAtIndex(0).getViewBox().addItem(self.cursor_start_curve2)
        self.ui.MainEgu.curveAtIndex(0).getViewBox().addItem(self.cursor_start_curve3)
        self.ui.RawBuf.curveAtIndex(0).getViewBox().addItem(self.cursor_start_curve4)
        self.ui.Raw.curveAtIndex(0).getViewBox().addItem(self.cursor_start_curve5)
        self.ui.Egu.curveAtIndex(0).getViewBox().addItem(self.cursor_start_curve6)

    def initialize_cursor_end(self, cursor_end_val):
        cursor_end_color = (0,0,0)
        self.cursor_end_curve1 = InfiniteLine(cursor_end_val, angle=90, pen={'color': cursor_end_color, 'width':2, 'dash': [2,4]})
        self.cursor_end_curve2 = InfiniteLine(cursor_end_val, angle=90, pen={'color': cursor_end_color, 'width':2, 'dash': [2,4]})
        self.cursor_end_curve3 = InfiniteLine(cursor_end_val, angle=90, pen={'color': cursor_end_color, 'width':2, 'dash': [2,4]})
        self.cursor_end_curve4 = InfiniteLine(cursor_end_val, angle=90, pen={'color': cursor_end_color, 'width':2, 'dash': [2,4]})
        self.cursor_end_curve5 = InfiniteLine(cursor_end_val, angle=90, pen={'color': cursor_end_color, 'width':2, 'dash': [2,4]})
        self.cursor_end_curve6 = InfiniteLine(cursor_end_val, angle=90, pen={'color': cursor_end_color, 'width':2, 'dash': [2,4]})
        self.ui.MainRawBuf.curveAtIndex(0).getViewBox().addItem(self.cursor_end_curve1)
        self.ui.MainRaw.curveAtIndex(0).getViewBox().addItem(self.cursor_end_curve2)
        self.ui.MainEgu.curveAtIndex(0).getViewBox().addItem(self.cursor_end_curve3)
        self.ui.RawBuf.curveAtIndex(0).getViewBox().addItem(self.cursor_end_curve4)
        self.ui.Raw.curveAtIndex(0).getViewBox().addItem(self.cursor_end_curve5)
        self.ui.Egu.curveAtIndex(0).getViewBox().addItem(self.cursor_end_curve6)

###################################################################################
###############################UPDATE PLOT SETTINGS################################
###################################################################################

    def update_coarse_delay_val_nc(self, coarse_delay_val):
        self.coarse_delay_val_nc = coarse_delay_val
        self.update_coarse_delay()

    def update_coarse_delay_val_sc(self, coarse_delay_val):
        self.coarse_delay_val_sc = coarse_delay_val
        self.update_coarse_delay()

    def update_coarse_delay(self):

        if self.mode == 0:
            if self.initialize_coarse_delay_flag == 0:
                self.called += 1

                self.coarse_delay_curve1.setValue(str(self.coarse_delay_val_nc))
                self.coarse_delay_curve2.setValue(str(self.coarse_delay_val_nc))
                self.coarse_delay_curve3.setValue(str(self.coarse_delay_val_nc))
                self.coarse_delay_curve4.setValue(str(self.coarse_delay_val_nc))
                self.coarse_delay_curve5.setValue(str(self.coarse_delay_val_nc))
                self.coarse_delay_curve6.setValue(str(self.coarse_delay_val_nc))
                self.update_peak_delay_val_nc(self.peak_delay_val_nc)
            elif self.initialize_coarse_delay_flag == 1:
                self.initialize_coarse_delay(self.coarse_delay_val_nc)
                self.initialize_coarse_delay_flag = 0

        elif self.mode == 1:
            if self.initialize_coarse_delay_flag == 0:
                self.coarse_delay_curve1.setValue(str(self.coarse_delay_val_sc))
                self.coarse_delay_curve2.setValue(str(self.coarse_delay_val_sc))
                self.coarse_delay_curve3.setValue(str(self.coarse_delay_val_sc))
                self.coarse_delay_curve4.setValue(str(self.coarse_delay_val_sc))
                self.coarse_delay_curve5.setValue(str(self.coarse_delay_val_sc))
                self.coarse_delay_curve6.setValue(str(self.coarse_delay_val_sc))
                self.update_peak_delay_val_sc(self.peak_delay_val_sc)
            elif self.initialize_coarse_delay_flag == 1:
                self.initialize_coarse_delay(self.coarse_delay_val_sc)
                self.initialize_coarse_delay_flag = 0

    def update_peak_delay_val_nc(self, peak_delay_val):
        self.peak_delay_val_nc = peak_delay_val
        self.peak_delay_val_nc_offset = self.peak_delay_val_nc + self.coarse_delay_val_nc
        self.update_peak_delay()

    def update_peak_delay_val_sc(self, peak_delay_val):
        self.peak_delay_val_sc = peak_delay_val
        self.peak_delay_val_sc_offset = self.peak_delay_val_sc + self.coarse_delay_val_sc
        self.update_peak_delay()

    def update_peak_delay(self):

        if self.mode == 0:
            if self.initialize_peak_delay_flag == 0:
                self.peak_delay_curve1.setValue(str(self.peak_delay_val_nc_offset))
                self.peak_delay_curve2.setValue(str(self.peak_delay_val_nc_offset))
                self.peak_delay_curve3.setValue(str(self.peak_delay_val_nc_offset))
                self.peak_delay_curve4.setValue(str(self.peak_delay_val_nc_offset))
                self.peak_delay_curve5.setValue(str(self.peak_delay_val_nc_offset))
                self.peak_delay_curve6.setValue(str(self.peak_delay_val_nc_offset))
                self.update_peak_width_val_nc(self.peak_width_val_nc)
            elif self.initialize_peak_delay_flag == 1:
                self.initialize_peak_delay(self.peak_delay_val_nc)
                self.initialize_peak_delay_flag = 0

        elif self.mode == 1:
            if self.initialize_peak_delay_flag == 0:
                self.peak_delay_curve1.setValue(str(self.peak_delay_val_sc_offset))
                self.peak_delay_curve2.setValue(str(self.peak_delay_val_sc_offset))
                self.peak_delay_curve3.setValue(str(self.peak_delay_val_sc_offset))
                self.peak_delay_curve4.setValue(str(self.peak_delay_val_sc_offset))
                self.peak_delay_curve5.setValue(str(self.peak_delay_val_sc_offset))
                self.peak_delay_curve6.setValue(str(self.peak_delay_val_sc_offset))
                self.update_peak_width_val_sc(self.peak_width_val_sc)
            elif self.initialize_peak_delay_flag == 1:
                self.initialize_peak_delay(self.peak_delay_val_sc)
                self.initialize_peak_delay_flag = 0

    def update_peak_width_val_nc(self, peak_width_val):
        self.peak_width_val_nc = peak_width_val
        self.peak_width_val_nc_offset = self.peak_width_val_nc + self.peak_delay_val_nc_offset
        self.update_peak_width()

    def update_peak_width_val_sc(self, peak_width_val):
        self.peak_width_val_sc = peak_width_val
        self.peak_width_val_sc_offset = self.peak_width_val_sc + self.peak_delay_val_sc_offset
        self.update_peak_width()

    def update_peak_width(self):

        if self.mode == 0:
            if self.initialize_peak_width_flag == 0:
                self.peak_width_curve1.setValue(str(self.peak_width_val_nc_offset))
                self.peak_width_curve2.setValue(str(self.peak_width_val_nc_offset))
                self.peak_width_curve3.setValue(str(self.peak_width_val_nc_offset))
                self.peak_width_curve4.setValue(str(self.peak_width_val_nc_offset))
                self.peak_width_curve5.setValue(str(self.peak_width_val_nc_offset))
                self.peak_width_curve6.setValue(str(self.peak_width_val_nc_offset))
                self.update_pedestal_delay_val_nc(self.pedestal_delay_val_nc)
            elif self.initialize_peak_width_flag == 1:
                self.initialize_peak_width(self.peak_width_val_nc)
                self.initialize_peak_width_flag = 0
        elif self.mode == 1:
            if self.initialize_peak_width_flag == 0:
                self.peak_width_curve1.setValue(str(self.peak_width_val_sc_offset))
                self.peak_width_curve2.setValue(str(self.peak_width_val_sc_offset))
                self.peak_width_curve3.setValue(str(self.peak_width_val_sc_offset))
                self.peak_width_curve4.setValue(str(self.peak_width_val_sc_offset))
                self.peak_width_curve5.setValue(str(self.peak_width_val_sc_offset))
                self.peak_width_curve6.setValue(str(self.peak_width_val_sc_offset))
                self.update_pedestal_delay_val_sc(self.pedestal_delay_val_sc)
            elif self.initialize_peak_width_flag == 1:
                self.initialize_peak_width(self.peak_width_val_sc)
                self.initialize_peak_width_flag = 0

    def update_pedestal_delay_val_nc(self, pedestal_delay_val):
        self.pedestal_delay_val_nc = pedestal_delay_val
        self.pedestal_delay_val_nc_offset = self.pedestal_delay_val_nc + self.coarse_delay_val_nc
        self.update_pedestal_delay()

    def update_pedestal_delay_val_sc(self, pedestal_delay_val):
        self.pedestal_delay_val_sc = pedestal_delay_val
        self.pedestal_delay_val_sc_offset = self.pedestal_delay_val_sc + self.coarse_delay_val_sc
        self.update_pedestal_delay()

    def update_pedestal_delay(self):
        
        if self.mode == 0:
            if self.initialize_pedestal_delay_flag == 0:
                self.pedestal_delay_curve1.setValue(str(self.pedestal_delay_val_nc_offset))
                self.pedestal_delay_curve2.setValue(str(self.pedestal_delay_val_nc_offset))
                self.pedestal_delay_curve3.setValue(str(self.pedestal_delay_val_nc_offset))
                self.pedestal_delay_curve4.setValue(str(self.pedestal_delay_val_nc_offset))
                self.pedestal_delay_curve5.setValue(str(self.pedestal_delay_val_nc_offset))
                self.pedestal_delay_curve6.setValue(str(self.pedestal_delay_val_nc_offset))
                self.update_pedestal_width_val_nc(self.pedestal_width_val_nc)
            elif self.initialize_pedestal_delay_flag == 1:
                self.initialize_pedestal_delay(self.pedestal_delay_val_nc)
                self.initialize_pedestal_delay_flag = 0
        elif self.mode == 1:
            if self.initialize_pedestal_delay_flag == 0:
                self.pedestal_delay_curve1.setValue(str(self.pedestal_delay_val_sc_offset))
                self.pedestal_delay_curve2.setValue(str(self.pedestal_delay_val_sc_offset))
                self.pedestal_delay_curve3.setValue(str(self.pedestal_delay_val_sc_offset))
                self.pedestal_delay_curve4.setValue(str(self.pedestal_delay_val_sc_offset))
                self.pedestal_delay_curve5.setValue(str(self.pedestal_delay_val_sc_offset))
                self.pedestal_delay_curve6.setValue(str(self.pedestal_delay_val_sc_offset))
                self.update_pedestal_width_val_sc(self.pedestal_width_val_sc)
            elif self.initialize_pedestal_delay_flag == 1:
                self.initialize_pedestal_delay(self.pedestal_delay_val_sc)
                self.initialize_pedestal_delay_flag = 0

    def update_pedestal_width_val_nc(self, pedestal_width_val):
        self.pedestal_width_val_nc = pedestal_width_val
        self.pedestal_width_val_nc_offset = self.pedestal_width_val_nc + self.pedestal_delay_val_nc_offset
        self.update_pedestal_width()

    def update_pedestal_width_val_sc(self, pedestal_width_val):
        self.pedestal_width_val_sc = pedestal_width_val
        self.pedestal_width_val_sc_offset = self.pedestal_width_val_sc + self.pedestal_delay_val_sc_offset
        self.update_pedestal_width()

    def update_pedestal_width(self):
        
        if self.mode == 0:
            if self.initialize_pedestal_width_flag == 0:
                self.pedestal_width_curve1.setValue(str(self.pedestal_width_val_nc_offset))
                self.pedestal_width_curve2.setValue(str(self.pedestal_width_val_nc_offset))
                self.pedestal_width_curve3.setValue(str(self.pedestal_width_val_nc_offset))
                self.pedestal_width_curve4.setValue(str(self.pedestal_width_val_nc_offset))
                self.pedestal_width_curve5.setValue(str(self.pedestal_width_val_nc_offset))
                self.pedestal_width_curve6.setValue(str(self.pedestal_width_val_nc_offset))
            elif self.initialize_pedestal_width_flag == 1:
                self.initialize_pedestal_width(self.pedestal_width_val_nc)
                self.initialize_pedestal_width_flag = 0
                self.initialize = 0
        elif self.mode == 1:
            if self.initialize_pedestal_width_flag == 0:
                self.pedestal_width_curve1.setValue(str(self.pedestal_width_val_sc_offset))
                self.pedestal_width_curve2.setValue(str(self.pedestal_width_val_sc_offset))
                self.pedestal_width_curve3.setValue(str(self.pedestal_width_val_sc_offset))
                self.pedestal_width_curve4.setValue(str(self.pedestal_width_val_sc_offset))
                self.pedestal_width_curve5.setValue(str(self.pedestal_width_val_sc_offset))
                self.pedestal_width_curve6.setValue(str(self.pedestal_width_val_sc_offset))
            elif self.initialize_pedestal_width_flag == 1:
                self.initialize_pedestal_width(self.pedestal_width_val_sc)
                self.initialize_pedestal_width_flag = 0
                self.initialize = 0

###################################################################################
#########################UPDATE CURSOR PLOT SETTINGS###############################
###################################################################################

    def update_cursor_start(self):
        self.cursor_start_val = self.ui.cursor_start.text()
        self.update_cursor_start_plot()

    def update_cursor_start_plot(self):
        
        if self.initialize_cursor_start_flag == 0:
            self.cursor_start_curve1.setValue(str(self.cursor_start_val))
            self.cursor_start_curve2.setValue(str(self.cursor_start_val))
            self.cursor_start_curve3.setValue(str(self.cursor_start_val))
            self.cursor_start_curve4.setValue(str(self.cursor_start_val))
            self.cursor_start_curve5.setValue(str(self.cursor_start_val))
            self.cursor_start_curve6.setValue(str(self.cursor_start_val))
            if not self.ui.cursor_start_vis.isChecked():
                self.set_cursor_start_visible()
                self.ui.cursor_start_vis.setChecked(True)
        elif self.initialize_cursor_start_flag == 1:
            self.initialize_cursor_start(self.cursor_start_val)
            self.initialize_cursor_start_flag = 0
        self.update_difference()

    def update_cursor_end(self):
        self.cursor_end_val = self.ui.cursor_end.text()
        self.update_cursor_end_plot()

    def update_cursor_end_plot(self):
        
        if self.initialize_cursor_end_flag == 0:
            self.cursor_end_curve1.setValue(str(self.cursor_end_val))
            self.cursor_end_curve2.setValue(str(self.cursor_end_val))
            self.cursor_end_curve3.setValue(str(self.cursor_end_val))
            self.cursor_end_curve4.setValue(str(self.cursor_end_val))
            self.cursor_end_curve5.setValue(str(self.cursor_end_val))
            self.cursor_end_curve6.setValue(str(self.cursor_end_val))
            if not self.ui.cursor_end_vis.isChecked():
                self.set_cursor_end_visible()
                self.ui.cursor_end_vis.setChecked(True)
        elif self.initialize_cursor_end_flag == 1:
            self.initialize_cursor_end(self.cursor_end_val)
            self.initialize_cursor_end_flag = 0
        self.update_difference()


    def update_difference(self):
        self.difference_val = int(self.cursor_end_val) - int(self.cursor_start_val)
        self.ui.difference.setText(str(self.difference_val))

###################################################################################
############################## Visibility Settings ################################
###################################################################################

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

    def toggle_cursor_start_visibility(self):
        if self.ui.cursor_start_vis.isChecked():
            self.ui.MainRawBuf.curveAtIndex(0).getViewBox().addItem(self.cursor_start_curve1)
            self.ui.MainRaw.curveAtIndex(0).getViewBox().addItem(self.cursor_start_curve2)
            self.ui.MainEgu.curveAtIndex(0).getViewBox().addItem(self.cursor_start_curve3)
            self.ui.RawBuf.curveAtIndex(0).getViewBox().addItem(self.cursor_start_curve4)
            self.ui.Raw.curveAtIndex(0).getViewBox().addItem(self.cursor_start_curve5)
            self.ui.Egu.curveAtIndex(0).getViewBox().addItem(self.cursor_start_curve6)
        else:   
            self.ui.MainRawBuf.curveAtIndex(0).getViewBox().removeItem(self.cursor_start_curve1)
            self.ui.MainRaw.curveAtIndex(0).getViewBox().removeItem(self.cursor_start_curve2)
            self.ui.MainEgu.curveAtIndex(0).getViewBox().removeItem(self.cursor_start_curve3)
            self.ui.RawBuf.curveAtIndex(0).getViewBox().removeItem(self.cursor_start_curve4)
            self.ui.Raw.curveAtIndex(0).getViewBox().removeItem(self.cursor_start_curve5)
            self.ui.Egu.curveAtIndex(0).getViewBox().removeItem(self.cursor_start_curve6)

    def toggle_cursor_end_visibility(self):
        if self.ui.cursor_end_vis.isChecked():
            self.ui.MainRawBuf.curveAtIndex(0).getViewBox().addItem(self.cursor_end_curve1)
            self.ui.MainRaw.curveAtIndex(0).getViewBox().addItem(self.cursor_end_curve2)
            self.ui.MainEgu.curveAtIndex(0).getViewBox().addItem(self.cursor_end_curve3)
            self.ui.RawBuf.curveAtIndex(0).getViewBox().addItem(self.cursor_end_curve4)
            self.ui.Raw.curveAtIndex(0).getViewBox().addItem(self.cursor_end_curve5)
            self.ui.Egu.curveAtIndex(0).getViewBox().addItem(self.cursor_end_curve6)
        else:   
            self.ui.MainRawBuf.curveAtIndex(0).getViewBox().removeItem(self.cursor_end_curve1)
            self.ui.MainRaw.curveAtIndex(0).getViewBox().removeItem(self.cursor_end_curve2)
            self.ui.MainEgu.curveAtIndex(0).getViewBox().removeItem(self.cursor_end_curve3)
            self.ui.RawBuf.curveAtIndex(0).getViewBox().removeItem(self.cursor_end_curve4)
            self.ui.Raw.curveAtIndex(0).getViewBox().removeItem(self.cursor_end_curve5)
            self.ui.Egu.curveAtIndex(0).getViewBox().removeItem(self.cursor_start_curve6)

    def set_cursor_start_visible(self):
        self.ui.MainRawBuf.curveAtIndex(0).getViewBox().addItem(self.cursor_start_curve1)
        self.ui.MainRaw.curveAtIndex(0).getViewBox().addItem(self.cursor_start_curve2)
        self.ui.MainEgu.curveAtIndex(0).getViewBox().addItem(self.cursor_start_curve3)
        self.ui.RawBuf.curveAtIndex(0).getViewBox().addItem(self.cursor_start_curve4)
        self.ui.Raw.curveAtIndex(0).getViewBox().addItem(self.cursor_start_curve5)
        self.ui.Egu.curveAtIndex(0).getViewBox().addItem(self.cursor_start_curve6)

    def set_cursor_end_visible(self):
        self.ui.MainRawBuf.curveAtIndex(0).getViewBox().addItem(self.cursor_end_curve1)
        self.ui.MainRaw.curveAtIndex(0).getViewBox().addItem(self.cursor_end_curve2)
        self.ui.MainEgu.curveAtIndex(0).getViewBox().addItem(self.cursor_end_curve3)
        self.ui.RawBuf.curveAtIndex(0).getViewBox().addItem(self.cursor_end_curve4)
        self.ui.Raw.curveAtIndex(0).getViewBox().addItem(self.cursor_end_curve5)
        self.ui.Egu.curveAtIndex(0).getViewBox().addItem(self.cursor_start_curve6)

    def set_cursor_start_invisible(self):
        self.ui.MainRawBuf.curveAtIndex(0).getViewBox().removeItem(self.cursor_start_curve1)
        self.ui.MainRaw.curveAtIndex(0).getViewBox().removeItem(self.cursor_start_curve2)
        self.ui.MainEgu.curveAtIndex(0).getViewBox().removeItem(self.cursor_start_curve3)
        self.ui.RawBuf.curveAtIndex(0).getViewBox().removeItem(self.cursor_start_curve4)
        self.ui.Raw.curveAtIndex(0).getViewBox().removeItem(self.cursor_start_curve5)
        self.ui.Egu.curveAtIndex(0).getViewBox().removeItem(self.cursor_start_curve6)

    def set_cursor_end_invisible(self):
        self.ui.MainRawBuf.curveAtIndex(0).getViewBox().removeItem(self.cursor_end_curve1)
        self.ui.MainRaw.curveAtIndex(0).getViewBox().removeItem(self.cursor_end_curve2)
        self.ui.MainEgu.curveAtIndex(0).getViewBox().removeItem(self.cursor_end_curve3)
        self.ui.RawBuf.curveAtIndex(0).getViewBox().removeItem(self.cursor_end_curve4)
        self.ui.Raw.curveAtIndex(0).getViewBox().removeItem(self.cursor_end_curve5)
        self.ui.Egu.curveAtIndex(0).getViewBox().removeItem(self.cursor_start_curve6)

###################################################################################
################################ Mode Settings ####################################
###################################################################################
    def switch_mode(self, mode):
        # fetch readback value and call update value with mode:
        self.mode = mode
        self.switch_mode_display()
        
        if self.initialize == 0:
            self.update_coarse_delay()
            self.update_peak_delay()
            self.update_peak_width()
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

###################################################################################
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
        print(self.num_points_raw_buf, self.ns_spacing)
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
