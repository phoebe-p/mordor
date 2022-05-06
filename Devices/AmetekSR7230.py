import pyvisa
# https://www.ameteksi.com/-/media/ameteksi/download_links/documentations/7225/an1002_using_the_model_7225_and_7265_lock-in_amplifiers_with_software_written_for_the_sr830.pdf
import numpy as np


class AmetekSR7230:
    """Represents a Signal Recovery Model 7230 lock-in amplifier

    Note that several instances can be created representing the same
    instrument. Be careful.
    Instance variables:
      pyvisa -- a pyvisa object for the connection, avoid using.
      status_byte -- status byte after the last read operation.
      overload_byte -- overload byte after the last read operation.
    Methods:
      read, write -- Read and write strings to/from the instrument.
      get_X, get_Y, get_R, get_T -- get measurements from the instrument.
      get_noise -- get the estimated measurement noise
    """

    def __init__(self, port='USB0::0x0A2D::0x0027::11265268::RAW', name='AmetekSR7230', info=None):
        """ Connects to the lockin amplifier

        Connects to the lockin, and checks that the lockin is present and
        correct. An error will be raised if the lockin is not there, or
        if it fails to identify itself as a model 7230
        Arguments:
          visaName -- A Visa Resource ID, like 'TCPIP0::10.0.0.2::50000::SOCKET'
        """
        rm = pyvisa.ResourceManager()
        self.pyvisa = rm.open_resource(port)
        self.pyvisa.read_termination='\00'
        #self.write('ID') # uses this not '*IDN?'
        #resp = self.read()

        self.info = {}
        self.info['Name'] = name
        if info is not None:
            self.info.update(info)
        self.min_wavelength = 0.
        self.build_timeconstants()
        self.timeconstant = self.get_time_constant()
        print('Connected to SR7230')

    def write(self,string):
        """Write string to the instrument."""
        self.pyvisa.write(string)

    def read(self):
        """Read string from the instrument. Also sets status bytes"""
        # replies seem to be: response LF NUL then two status bytes
        resp = self.pyvisa.read().strip()
        status = self.pyvisa.visalib.read(self.pyvisa.session,2)[0]
        self.status_byte = status[0]
        self.overload_byte = status[1]
        return resp


    def build_timeconstants(self):
        self.timeconstants = []
        for p in range(-5,4):
            self.timeconstants.append(10**p)
            self.timeconstants.append(2*10**p)
            self.timeconstants.append(5*10**p)

        self.timeconstants = np.array(self.timeconstants)
        self.timeconstants = self.timeconstants[self.timeconstants < 1.01e3]

    def get_time_constant(self):
        self.write("TC")
        resp = self.read()
        return self.timeconstants[int(resp)]

    def measure(self):
        self.write('MAG.')
        mag = float(self.read())
        self.write('PHA.')
        phase = float(self.read())
        return (mag, phase)

    def update_integration_time(self, new_time):
        """ Updates the integration time in the lockin based on the selection in the program
        :param new_time: the new integration time selected in the program (in ms)
        :return:
        """
        idx = np.argmin(abs(self.timeconstants-new_time/1000.))
        command = 'TC ' + str(idx)
        print(command)
        self.write(command)
        self.read()

        self.timeconstant = self.get_time_constant()
        print('Integration time: {0:.2f} ms'.format(self.timeconstant*1000))
        return self.timeconstant*1000


class New(AmetekSR7230):
    """ Standarised name for the SR7230 class"""
    pass
