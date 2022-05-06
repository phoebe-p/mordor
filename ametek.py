#from pymeasure.instruments.ametek import Ametek7270

#import usbtmc
#import subprocess

#subprocess.check_output()


import pyvisa


class WrongInstrumentError(Exception):
    """The wrong instrument is connected

    A connection was successfuly established, and the instrument responded
    to a request to identify itself, but the ID recieved was wrong.
    Probably the instrument at the given VISA identifier is not the one
    you wanted.
    """
    pass


class Instrument:
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

    def __init__(self,visaName):
        """ Connects to the lockin amplifier

        Connects to the lockin, and checks that the lockin is present and
        correct. An error will be raised if the lockin is not there, or
        if it fails to identify itself as a model 7230
        Arguments:
          visaName -- A Visa Resource ID, like 'TCPIP0::10.0.0.2::50000::SOCKET'
        """
        rm = pyvisa.ResourceManager()
        self.pyvisa = rm.open_resource(visaName)
        self.pyvisa.read_termination='\00'
        self.write('ID') # uses this not '*IDN?'
        resp = self.read()
        if resp != '7230':
            raise WrongInstrumentError(
                'Wrote "ID" Expected "7230" got "{}"'.format(resp))

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

    def get_X(self):
        """Get X value from the instrument, returns a float"""
        self.write('X.')
        return float(self.read())

    def get_Y(self):
        """Get Y value from the instrument, returns a float"""
        self.write('Y.')
        return float(self.read())

    def get_R(self):
        """Get R value from the instrument, returns a float"""
        self.write('MAG.')
        return float(self.read())

    def get_T(self):
        """Get theta value from the instrument, returns a float"""
        self.write('PHA.')
        return float(self.read())

    def get_noise(self):
        """Get Y noise from the instrument, in v/sqrtHz, returns a float"""
        self.write('NHZ.')
        return float(self.read())
import pyvisa


class WrongInstrumentError(Exception):
    """The wrong instrument is connected

    A connection was successfuly established, and the instrument responded
    to a request to identify itself, but the ID recieved was wrong.
    Probably the instrument at the given VISA identifier is not the one
    you wanted.
    """
    pass


class Instrument:
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

    def __init__(self,visaName):
        """ Connects to the lockin amplifier

        Connects to the lockin, and checks that the lockin is present and
        correct. An error will be raised if the lockin is not there, or
        if it fails to identify itself as a model 7230
        Arguments:
          visaName -- A Visa Resource ID, like 'TCPIP0::10.0.0.2::50000::SOCKET'
        """
        rm = pyvisa.ResourceManager()
        self.pyvisa = rm.open_resource(visaName)
        self.pyvisa.read_termination='\00'
        self.write('ID') # uses this not '*IDN?'
        resp = self.read()
        if resp != '7230':
            raise WrongInstrumentError(
                'Wrote "ID" Expected "7230" got "{}"'.format(resp))

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

    def get_X(self):
        """Get X value from the instrument, returns a float"""
        self.write('X.')
        return float(self.read())

    def get_Y(self):
        """Get Y value from the instrument, returns a float"""
        self.write('Y.')
        return float(self.read())

    def get_R(self):
        """Get R value from the instrument, returns a float"""
        self.write('MAG.')
        return float(self.read())

    def get_T(self):
        """Get theta value from the instrument, returns a float"""
        self.write('PHA.')
        return float(self.read())

    def get_noise(self):
        """Get Y noise from the instrument, in v/sqrtHz, returns a float"""
        self.write('NHZ.')
        return float(self.read())

if __name__=="__main__":
    inst = Instrument('USB0::0x0A2D::0x0027::11265268::RAW')

