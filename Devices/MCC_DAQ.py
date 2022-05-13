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
        data_value = self.get_data_value_analog()

        try:
            # Send the value to the device (optional parameter omitted)
            ul.v_out(self.board_num, channel, ao_range, data_value)
        except ULError as e:
            show_ul_error(e)

    def get_data_value_analog(self):
        try:
            print(type(self.data_value_entry))
            return float(self.data_value_entry.get())
        except ValueError:
            return 0

    def get_data_value_digital(self):
        try:
            return int(self.data_value_entry.get())
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
            return int(self.channel_entry.get())
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

    # def create_widgets(self):
    #     '''Create the tkinter UI'''
    #     self.device_label = tk.Label(self)
    #     self.device_label.pack(fill=tk.NONE, anchor=tk.NW)
    #     self.device_label["text"] = ('Board Number ' + str(self.board_num)
    #                                  + ": " + self.device_info.product_name
    #                                  + " (" + self.device_info.unique_id + ")")
    #
    #     main_frame = tk.Frame(self)
    #     main_frame.pack(fill=tk.X, anchor=tk.NW)
    #
    #     channel_vcmd = self.register(self.validate_channel_entry)
    #     float_vcmd = self.register(validate_float_entry)
    #
    #     curr_row = 0
    #     if self.ao_info.num_chans > 1:
    #         channel_entry_label = tk.Label(main_frame)
    #         channel_entry_label["text"] = "Channel Number:"
    #         channel_entry_label.grid(row=curr_row, column=0, sticky=tk.W)
    #
    #         self.channel_entry = tk.Spinbox(
    #             main_frame, from_=0, to=max(self.ao_info.num_chans - 1, 0),
    #             validate='key', validatecommand=(channel_vcmd, '%P'))
    #         self.channel_entry.grid(row=curr_row, column=1, sticky=tk.W)
    #         curr_row += 1
    #
    #     data_value_label = tk.Label(main_frame)
    #     data_value_label["text"] = "Value (V):"
    #     data_value_label.grid(row=curr_row, column=0, sticky=tk.W)
    #
    #     self.F = tk.Entry(
    #         main_frame, validate='key', validatecommand=(float_vcmd, '%P'))
    #     self.data_value_entry.grid(row=curr_row, column=1, sticky=tk.W)
    #     self.data_value_entry.insert(0, "0")
    #
    #     update_button = tk.Button(main_frame)
    #     update_button["text"] = "Update"
    #     update_button["command"] = self.update_value
    #     update_button.grid(row=curr_row, column=2, padx=3, pady=3)
    #
    #     button_frame = tk.Frame(self)
    #     button_frame.pack(fill=tk.X, side=tk.RIGHT, anchor=tk.SE)
    #
    #     quit_button = tk.Button(button_frame)
    #     quit_button["text"] = "Quit"
    #     quit_button["command"] = self.master.destroy
    #     quit_button.grid(row=0, column=0, padx=3, pady=3)

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
