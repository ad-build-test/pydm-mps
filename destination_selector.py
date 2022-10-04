from os import path
from PyQt5.QtWidgets import QCheckBox
from epics import caget, caput
from pydm import Display

class DestinationSelectorDisplay(Display):

    def __init__(self, parent=None, args=[], macros=None):
        super(DestinationSelectorDisplay, self).__init__(parent=parent, args=args, macros=macros)
        
        #need to initialize the bit names
        self.init_display() 
        self.init_maskBits()
        self.ui.save_btn.clicked.connect(self.save_content)

    def init_display(self):
        #Check if there are macros defined and change visibility if not:
        dest_used = []

        for dest in range(16):
            if self.macros()['DEST'+str(dest)] == str(0):
                dest_used.append(0)
            else:
                dest_used.append(1)

        self.ui.dest0.setVisible(dest_used[0])
        self.ui.dest1.setVisible(dest_used[1])
        self.ui.dest2.setVisible(dest_used[2])
        self.ui.dest3.setVisible(dest_used[3])
        self.ui.dest4.setVisible(dest_used[4])
        self.ui.dest5.setVisible(dest_used[5])
        self.ui.dest6.setVisible(dest_used[6])
        self.ui.dest7.setVisible(dest_used[7])
        self.ui.dest8.setVisible(dest_used[8])
        self.ui.dest9.setVisible(dest_used[9])
        self.ui.dest10.setVisible(dest_used[10])
        self.ui.dest11.setVisible(dest_used[11])
        self.ui.dest12.setVisible(dest_used[12])
        self.ui.dest13.setVisible(dest_used[13])
        self.ui.dest14.setVisible(dest_used[14])
        self.ui.dest15.setVisible(dest_used[15])

        self.ui.checkbox_bitpos0.setVisible(dest_used[0])
        self.ui.checkbox_bitpos1.setVisible(dest_used[1])
        self.ui.checkbox_bitpos2.setVisible(dest_used[2])
        self.ui.checkbox_bitpos3.setVisible(dest_used[3])
        self.ui.checkbox_bitpos4.setVisible(dest_used[4])
        self.ui.checkbox_bitpos5.setVisible(dest_used[5])
        self.ui.checkbox_bitpos6.setVisible(dest_used[6])
        self.ui.checkbox_bitpos7.setVisible(dest_used[7])
        self.ui.checkbox_bitpos8.setVisible(dest_used[8])
        self.ui.checkbox_bitpos9.setVisible(dest_used[9])
        self.ui.checkbox_bitpos10.setVisible(dest_used[10])
        self.ui.checkbox_bitpos11.setVisible(dest_used[11])
        self.ui.checkbox_bitpos12.setVisible(dest_used[12])
        self.ui.checkbox_bitpos13.setVisible(dest_used[13])
        self.ui.checkbox_bitpos14.setVisible(dest_used[14])
        self.ui.checkbox_bitpos15.setVisible(dest_used[15])

    def init_maskBits(self):
        '''
        Read in the current value of the destination and set the toggles.
        '''
        dest_value = caget(self.macros()['MPS_PREFIX'] + ':BEAM_DEST_MASK_RBV')
        #test dest_value:
        #dest_value = 3

        bit_list = []
        for pos in range(16):
            if dest_value is not None:
                bit_list.append(bool(dest_value & (1<<pos)))
        
        #check that the list isn't empty
        if bit_list:
            self.ui.checkbox_bitpos0.setChecked(bit_list[0])
            self.ui.checkbox_bitpos1.setChecked(bit_list[1])
            self.ui.checkbox_bitpos2.setChecked(bit_list[2])
            self.ui.checkbox_bitpos3.setChecked(bit_list[3])
            self.ui.checkbox_bitpos4.setChecked(bit_list[4])
            self.ui.checkbox_bitpos5.setChecked(bit_list[5])
            self.ui.checkbox_bitpos6.setChecked(bit_list[6])
            self.ui.checkbox_bitpos7.setChecked(bit_list[7])
            self.ui.checkbox_bitpos8.setChecked(bit_list[8])
            self.ui.checkbox_bitpos9.setChecked(bit_list[9])
            self.ui.checkbox_bitpos10.setChecked(bit_list[10])
            self.ui.checkbox_bitpos11.setChecked(bit_list[11])
            self.ui.checkbox_bitpos12.setChecked(bit_list[12])
            self.ui.checkbox_bitpos13.setChecked(bit_list[13])
            self.ui.checkbox_bitpos14.setChecked(bit_list[14])
            self.ui.checkbox_bitpos15.setChecked(bit_list[15])

    def read_maskBits(self):
        bit_list = []
        bit_list.append(self.ui.checkbox_bitpos0.isChecked())
        bit_list.append(self.ui.checkbox_bitpos1.isChecked())
        bit_list.append(self.ui.checkbox_bitpos2.isChecked())
        bit_list.append(self.ui.checkbox_bitpos3.isChecked())
        bit_list.append(self.ui.checkbox_bitpos4.isChecked())
        bit_list.append(self.ui.checkbox_bitpos5.isChecked())
        bit_list.append(self.ui.checkbox_bitpos6.isChecked())
        bit_list.append(self.ui.checkbox_bitpos7.isChecked())
        bit_list.append(self.ui.checkbox_bitpos8.isChecked())
        bit_list.append(self.ui.checkbox_bitpos9.isChecked())
        bit_list.append(self.ui.checkbox_bitpos10.isChecked())
        bit_list.append(self.ui.checkbox_bitpos11.isChecked())
        bit_list.append(self.ui.checkbox_bitpos12.isChecked())
        bit_list.append(self.ui.checkbox_bitpos13.isChecked())
        bit_list.append(self.ui.checkbox_bitpos14.isChecked())
        bit_list.append(self.ui.checkbox_bitpos15.isChecked())
        
        self.dest_value = 0
        for pos in range(16):
            self.dest_value += bit_list[pos]<<pos & (1<<pos)
    
    def save_content(self):
        self.read_maskBits()
         
    @staticmethod
    def ui_filename():
        return 'destination_selector.ui'

    def ui_filepath(self):
        return path.join(path.dirname(path.realpath(__file__)), self.ui_filename())
