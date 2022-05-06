# Libraries
import pyvisa
from tkinter import messagebox, ttk
import tkinter as tk
import pyBen

debug = False
developing = False

# Class definition
class TMC300:
    def __init__(self, port=None, name='Bentham TMC300', info=None):
        self.info = {}
        self.info['Name'] = name
        if info is not None:
            self.info.update(info)

        ## Initialise monochromator
        pyBen.build_system_model("C:/Program Files (x86)/Bentham/SDK/Configuration Files/system.cfg")
        pyBen.load_setup("C:/Program Files (x86)/Bentham/SDK/Configuration Files/system.atr")
        pyBen.initialise()
        print('Connected to TMC300.')
        pyBen.park()

    def move(self, target, speed='Normal'):
        pyBen.select_wavelength(float(target),5) # 5s timeout to complete operation

    def close(self):
        pyBen.close()

    def interface(self, master):
        # Top level elements
        acton_window = tk.Toplevel(master.window)
        acton_window.geometry('+100+100')
        acton_window.resizable(False, False)
        acton_window.protocol('WM_DELETE_WINDOW', self.no_quit)  # Used to force a "safe closing" of the program
        acton_window.option_add('*tearOff', False)  # Prevents tearing the menus
        acton_window.title('Select the options:')

        # Creates the main frame
        config_frame = ttk.Frame(master=acton_window, padding=(15, 15, 15, 15))
        config_frame.grid(column=0, row=0, sticky=(tk.EW))
        config_frame.columnconfigure(0, weight=1)

        # Create the buttons
        ttk.Button(master=config_frame, text='Update', command=self.update_grating_settings).grid(column=1,row=3, sticky=tk.EW)
        ttk.Button(master=config_frame, text='Cancel', command=acton_window.destroy).grid(column=2, row=3, sticky=tk.EW)


        ttk.Label(master=config_frame, text='Grating 1 (250-1100 nm):').grid(column=0, row=1, sticky=tk.E)
        ttk.Label(master=config_frame, text='Grating 2 (800-2500 nm):').grid(column=0, row=2, sticky=tk.E)

        ttk.Label(master=config_frame, text='Min. wavelength (nm):').grid(column=1, row=0, sticky=tk.E)
        ttk.Label(master=config_frame, text='Max. wavelength (nm):').grid(column=2, row=0, sticky=tk.E)

        #min_WL_1 = tk.StringVar()
        #max_WL_1 = tk.StringVar()
        #min_WL_2 = tk.StringVar()
        #max_WL_2 = tk.StringVar()

        # pyBen get function: name of component, token for required value, index for part in component
        # tokens are integer values. Minimum grating wavelengths = 23, Maximum grating wavelength = 24
        # These values can be found in the dlltoken.h file from the Bentham SDK

        # There are two gratings in the turret for this version of the monochromator, because they are
        # in turret '1' all their indices are prexifed with '1'. So 11 is grating 1 and 12 is grating 2.

        # get current values, to fill out the table
        min_WL_1_cur = pyBen.get('mchromator', 23, 11)['value']
        max_WL_1_cur = pyBen.get('mchromator', 24, 11)['value']

        min_WL_2_cur = pyBen.get('mchromator', 23, 12)['value']
        max_WL_2_cur = pyBen.get('mchromator', 24, 12)['value']

        # set new values
        self.min_WL_1_entry = ttk.Entry(master=config_frame, width=15)
        self.max_WL_1_entry = ttk.Entry(master=config_frame, width=15)
        self.min_WL_1_entry.grid(column=1, row=1, columnspan=1, sticky=tk.EW)
        self.max_WL_1_entry.grid(column=2, row=1, columnspan=1, sticky=tk.EW)
        self.min_WL_1_entry.insert(0, min_WL_1_cur)
        self.max_WL_1_entry.insert(0, max_WL_1_cur)

        self.min_WL_2_entry = ttk.Entry(master=config_frame, width=15)
        self.max_WL_2_entry = ttk.Entry(master=config_frame, width=15)
        self.min_WL_2_entry.grid(column=1, row=2, columnspan=1, sticky=tk.EW)
        self.max_WL_2_entry.grid(column=2, row=2, columnspan=1, sticky=tk.EW)
        self.min_WL_2_entry.insert(0, min_WL_2_cur)
        self.max_WL_2_entry.insert(0, max_WL_2_cur)

        # These commands give the control to the HW window. I am not sure what they do exactly.
        acton_window.lift(master.window)  # Brings the hardware window to the top
        acton_window.transient(master.window)  # ?
        acton_window.grab_set()  # ?
        #master.wait_window(acton_window)  # Freezes the main window until this one is closed.

    def update_grating_settings(self):
        min_WL_1 = float(self.min_WL_1_entry.get())
        max_WL_1 = float(self.max_WL_1_entry.get())
        min_WL_2 = float(self.min_WL_2_entry.get())
        max_WL_2 = float(self.max_WL_2_entry.get())

        pyBen.set('mchromator', 23, 11, min_WL_1)
        pyBen.set('mchromator', 24, 11, max_WL_1)
        pyBen.set('mchromator', 23, 12, min_WL_2)
        pyBen.set('mchromator', 24, 12, max_WL_2)
        print('Updated min/max wavelengths for gratings.')

    def no_quit(self):
        pass

class New(TMC300):
    """ Standarised name for the TMC300 class"""
    pass

# Testing
if __name__=="__main__":
    test = New()
    print(test.update_integration_time(0.800))
