__author__ = 'D. Alonso-Álvarez'

import pyvisa

def visa_ports():

    rm = pyvisa.ResourceManager()
    port_list = [p for p in rm.list_resources()]

    if port_list == ['']:
        port_list = ['None']

    return port_list
