# Libraries
from __future__ import absolute_import, division, print_function

import os
import tkinter as tk
from tkinter import messagebox

from mcculw.device_info import DaqDeviceInfo
from mcculw import ul
from mcculw.enums import InterfaceType, ErrorCode, DigitalIODirection
from mcculw.ul import ULError


def show_ul_error(ul_error):
    message = 'A UL Error occurred.\n\n' + str(ul_error)
    messagebox.showerror("Error", message)


def validate_float_entry(p):
    valid = False if p is None else True
    if p:
        try:
            float(p)
        except ValueError:
            valid = False
    return valid


# Class definition
class MCC_DAQ():
    def __init__(self, port=None, name="MCC DAQ", info=None):
        # By default, the example detects all available devices and selects the
        # first device listed.
        # If use_device_detection is set to False, the board_num property needs
        # to match the desired board number configured with Instacal.

        self.info = {}
        self.info['Name'] = name
        if info is not None:
            self.info.update(info)

        use_device_detection = True
        self.board_num = 0

        try:
            if use_device_detection:
                self.configure_first_detected_device()

            self.device_info = DaqDeviceInfo(self.board_num)
            self.ao_info = self.device_info.get_ao_info()
            dio_info = self.device_info.get_dio_info()

            self.port = next((port for port in dio_info.port_info
                              if port.supports_output), None)

            if self.port is not None:
                # If the port is configurable, configure it for output
                if self.port.is_port_configurable:
                    try:
                        ul.d_config_port(self.board_num, self.port.type,
                                         DigitalIODirection.OUT)
                    except ULError as e:
                        show_ul_error(e)

        except ULError as e:
            show_ul_error(e)


    def configure_first_detected_device(self):
        ul.ignore_instacal()
        devices = ul.get_daq_device_inventory(InterfaceType.ANY)
        if not devices:
            raise ULError(ErrorCode.BADBOARD)

        # Add the first DAQ device to the UL with the specified board number
        ul.create_daq_device(self.board_num, devices[0])

    def update_value(self):
        channel = self.get_channel_num()
        ao_range = self.ao_info.supported_ranges[0]
        data_value = self.data_value_entry_analog
        print('chan, val:', channel, data_value)

        try:
            # Send the value to the device (optional parameter omitted)
            ul.v_out(self.board_num, channel, ao_range, data_value)
        except ULError as e:
            show_ul_error(e)

    # def get_data_value_analog(self):
    #     try:
    #         return float(self.data_value_entry_analog.get())
    #     except ValueError:
    #         return 0

    def get_data_value_digital(self):
        try:
            return int(self.data_value_entry_digital.get())
        except ValueError:
            return 0

    def data_value_changed(self, *args):
        try:
            # Get the data value
            data_value = self.get_data_value_digital()
            # Send the value to the device
            ul.d_out(self.board_num, self.port.type, data_value)
        except ULError as e:
            show_ul_error(e)

    def get_channel_num(self):
        if self.ao_info.num_chans == 1:
            return 0
        try:
            return int(self.channel_entry)
        except ValueError:
            return 0

    def validate_channel_entry(self, p):
        if p == '':
            return True
        try:
            value = int(p)
            if value < 0 or value > self.ao_info.num_chans - 1:
                return False
        except ValueError:
            return False

        return True

    def move(self):
        return 0

    def close(self):
        pass

class New(MCC_DAQ):
    """ Standarised name for the MCC DAQ class"""
    pass

# Testing
if __name__=="__main__":
    test = New()
