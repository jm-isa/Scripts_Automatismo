import numpy
from math import ceil
import struct
import os

"""
Library based on pycomtrade
"""

class ReadAllComtrade():

    """
    To do:
    - Get signal by ID, currently is by index
    - Check the relation of the channel in analog signal float 32
    """

    def __init__(self, filename):
        """
        pyComtrade constructor:
            Prints a message.
            Clear the variables
            Check if filename exists.
            If so, read the CFG file.
        filename: string with the path for the .cfg file.

        """
        # print('ReadAllComtrade instance created!')
        self.clear()

        if os.path.isfile(filename):
            self.filename = filename
            self.ReadComtrade()
        else:
            print("%s File not found." % (filename))
            return
    
    def clear(self):
        """
        Clear the internal (private) variables of the class.
        """
        self.filename = ''
        self.filehandler = 0
        # Station name, identification and revision year:
        self.station_name = ''
        self.rec_dev_id = ''
        self.rev_year = 0000
        # Number and type of channels:
        self.TT = 0
        self.A = 0  # Number of analog channels.
        self.D = 0  # Number of digital channels.
        # Analog channel information:
        self.An = []
        self.Ach_id = []
        self.Aph = []
        self.Accbm = []
        self.uu = []
        self.a = []
        self.b = []
        self.skew = []
        self.min = []
        self.max = []
        self.primary = []
        self.secondary = []
        self.PS = []
        # Digital channel information:
        self.Dn = []
        self.Dch_id = []
        self.Dph = []
        self.Dccbm = []
        self.y = []
        # Line frequency:
        self.lf = 0
        # Sampling rate information:
        self.nrates = 0
        self.samp = []
        self.endsamp = []
        # Date/time stamps:
        #    defined by: [dd,mm,yyyy,hh,mm,ss.ssssss]
        self.start = [00, 00, 0000, 00, 00, 0.0]
        self.trigger = [00, 00, 0000, 00, 00, 0.0]
        # Data file type:
        self.ft = ''
        # Time stamp multiplication factor:
        self.timemult = 0.0

        self.DatFileContent = ''

    def ReadComtrade(self):
        self.filehandler = open(self.filename, 'r')
        # Processing first line:
        line = self.filehandler.readline()
        templist = line.split(',')
        self.station_name = templist[0]
        self.rec_dev_id = templist[1]
        # Odd cfg file may not contain all first line fields
        # checking vector length to avoid IndexError
        if len(templist) > 2:
            self.rev_year = int(templist[2])

        # Processing second line:
        line = self.filehandler.readline().rstrip()  # Read line and remove spaces and new line characters.
        templist = line.split(',')
        self.TT = int(templist[0])
        self.A = int(templist[1].strip('A'))
        self.D = int(templist[2].strip('D'))

        # Processing analog channel lines:
        for i in range(self.A):  # @UnusedVariable
            line = self.filehandler.readline()
            templist = line.split(',')
            self.An.append(int(templist[0]))
            self.Ach_id.append(templist[1])
            self.Aph.append(templist[2])
            self.Accbm.append(templist[3])
            self.uu.append(templist[4])
            self.a.append(float(templist[5]))
            self.b.append(float(templist[6]))
            self.skew.append(float(templist[7]))
            # self.min.append(float(templist[8]))
            # self.max.append(float(templist[9]))
            # Odd cfg file may not contain all analog channel fields
            # checking vector length to avoid IndexError
            if len(templist) > 10:
                self.primary.append(float(templist[10]))
            if len(templist) > 11:
                self.secondary.append(float(templist[11]))
            if len(templist) > 12:
                self.PS.append(templist[12])

        # Processing digital channel lines:
        for i in range(self.D):  # @UnusedVariable
            line = self.filehandler.readline()
            templist = line.split(',')
            self.Dn.append(int(templist[0]))
            self.Dch_id.append(templist[1])
            self.Dph.append(templist[2])
            # Odd cfg file may not contain all digital channel fields
            # checking vector length to avoid IndexError
            if len(templist) > 3:
                self.Dccbm.append(templist[3])
            if len(templist) > 4:
                self.y.append(int(templist[4]))

        # Read line frequency:
        self.lf = int(float(self.filehandler.readline()))

        # Read sampling rates:
        self.nrates = int(self.filehandler.readline())  # nrates.
        for i in range(self.nrates):  # @UnusedVariable
            line = self.filehandler.readline()
            templist = line.split(',')
            self.samp.append(int(float(templist[0])))
            self.endsamp.append(int(float(templist[1])))

        # Read start date and time ([dd,mm,yyyy,hh,mm,ss.ssssss]):
        line = self.filehandler.readline()
        self.templistt= line
        templist = line.split('/')
        self.start[2] = int(templist[0])  # day.
        self.start[1] = int(templist[1])  # month.
        templist = templist[2].split(',')
        self.start[0] = int(templist[0][-2:])  # year.
        templist = templist[1].split(':')
        self.start[3] = int(templist[0])  # hours.
        self.start[4] = int(templist[1])  # minutes.
        self.start[5] = int( float( templist[2] ) )  # seconds.

        
        # Read trigger date and time ([dd,mm,yyyy,hh,mm,ss.ssssss]):
        line = self.filehandler.readline()
        templist = line.split('/')
        self.trigger[0] = int(templist[0])  # day.
        self.trigger[1] = int(templist[1])  # month.
        templist = templist[2].split(',')
        self.trigger[2] = int(templist[0])  # year.
        templist = templist[1].split(':')
        self.trigger[3] = int(templist[0])  # hours.
        self.trigger[4] = int(templist[1])  # minutes.
        self.trigger[5] = float(templist[2])  # seconds.

        # Read file type:
        self.ft = str(self.filehandler.readline())

        # Read time multiplication factor:
        # Odd cfg file may not have multiplication field, so checking
        # its existance before reading is a safe measure
        # If the multiplication field is not available, it will be considered as 1
        self.timemul = self.filehandler.readline()
        if self.timemul != '':
            self.timemul = float(self.timemul)
        else:
            self.timemul = 1

        # END READING .CFG FILE.
        self.filehandler.close()  # Close file.
        
#        return self.start, self.trigger
    

    def getNumberOfSamples(self):
        """
        Return the number of samples of the oscillographic record.
        Only one smapling rate is taking into account for now.
        """
        return self.endsamp[0]
    
    def getSamplingRate(self):
        """
        Return the sampling rate.

        Only one smapling rate is taking into account for now.
        """
        return self.samp[0]
    
    def getAnalogID(self, num):
        """
        Returns the COMTRADE ID of a given channel number.
        The number to be given is the same of the COMTRADE header.
        """
        listidx = self.An.index(num)  # Get the position of the channel number.
        return self.Ach_id[listidx]
    
    def getDigitalID(self, num):
        """
        Reads the COMTRADE ID of a given channel number.
        The number to be given is the same of the COMTRADE header.
        """
        listidx = self.Dn.index(num)  # Get the position of the channel number.
        return self.Dch_id[listidx]
    
    def getAnalogType(self, num):
        """
        Returns the type  of the channel 'num' based
        on its unit stored in the Comtrade header file.

        Returns 'V' for a voltage channel and 'I' for a current channel.
        """
        listidx = self.An.index(num)
        unit = self.uu[listidx]

        if unit == 'kV' or unit == 'V':
            return 'V'
        elif unit == 'A' or unit == 'kA':
            return 'I'
        else:
            print('Unknown channel type')
            return 0

    def getAnalogUnit(self, num):
        """
        Returns the COMTRADE channel unit (e.g., kV, V, kA, A)
        of a given channel number.
        The number to be given is the same of the COMTRADE header.
        """
        listidx = self.An.index(num)  # Get the position of the channel number.
        return self.uu[listidx]
    
    def ReadDataFile(self):
        """
        Reads the contents of the Comtrade .dat file and store them in a
        private variable.

        For accessing a specific channel data, see methods getAnalogData and
        getDigitalData.
        """

        if os.path.isfile(self.filename[0:-4] + '.dat'):
            filename = self.filename[0:-4] + '.dat'

        elif os.path.isfile(self.filename[0:-4] + '.DAT'):
            filename = self.filename[0:-4] + '.DAT'

        else:
            print("Data file File not found.")
            return 0
        
        if  self.ft.strip('\n') =='ASCII' :
            self.filehandler = open(filename, 'r')
            self.DatFileContent = self.filehandler.readlines()
        elif self.ft.strip('\n') == 'FLOAT32':
            self.filehandler = open(filename, 'rb')
            self.DatFileContent = self.filehandler.read()
        else:
            print("Check the comtrade format , this version only support ASCCI and FLOAT32 (check the lower and upper case)")
            return 0

        # END READING .dat FILE.
        self.filehandler.close()  # Close file.

        return 1

    def getAnalogChannel(self, ChNumber):
        """
        Main method for extract the information of the analog signals from .dat comtrade
        """
        if  self.ft.strip('\n')=='ASCII' :
            values= self.getAnalogASCCI(ChNumber)
        elif self.ft.strip('\n')== 'FLOAT32':
            values= self.getAnalogFloat32(ChNumber)
        else:
            print("Check the comtrade format , this version only support ASCCI and FLOAT32")
            return 0
        
        return values
    
    def getTimeChannel(self):
        """
        Main method for extract the information of the time signal from .dat comtrade
        """
        if  self.ft.strip('\n') =='ASCII' :
            values= self.getTimeASCCI()
        elif self.ft.strip('\n') == 'FLOAT32':
            values= self.getTimeFloat32()
        else:
            print("Check the comtrade format , this version only support ASCCI and FLOAT32")
            return 0
        
        return values
    
    
    def getDigitalChannel(self, ChNumber):
        """
        Main method for extract the information of the digital signals from .dat comtrade
        """
        if  self.ft.strip('\n') =='ASCII' :
            values= self.getDigitalASCCI(ChNumber)
        elif self.ft.strip('\n') == 'FLOAT32':
            values= self.getDigitalFloat32(ChNumber)
        else:
            print("Check the comtrade format , this version only support ASCCI and FLOAT32")
            return 0
        
        return values


    def getAnalogFloat32(self, ChNumber):
        """
        Returns an array of numbers containing the data values of the channel
        number "ChNumber".

        ChNumber is the number of the channal as in .cfg file.
        """

        if not self.DatFileContent:
            print("No data file content. Use the method ReadDataFile first")
            return 0

        if (ChNumber > self.A):
            print("Channel number greater than the total number of channels.")
            return 0

        # Structur of the data
        # structur with two integers (Sample numeber and time stamp), float for the anlog channels and digital short for digital channels
        str_struct = 'i' + 'i' + str(self.A) + 'h' + str(int(numpy.ceil((float(self.D) / float(16))))) + 'H'
        # Number of bytes per sample:
        # this ecuation is explaining in the page 25 of the comtrade format 1999
        NB = 4 + 4 + self.A * 2 + int(numpy.ceil((float(self.D) / float(16)))) * 2
        # Number of samples:
        N = self.getNumberOfSamples()

        # Empty column vector for the data:
        values = numpy.empty((N, 1))

        ch_index = self.An.index(ChNumber)

        # Reading the values from DatFileContent string:
        for i in range(N):
            data = struct.unpack(str_struct, self.DatFileContent[i * NB:(i * NB) + NB])
            values[i] = data[ChNumber + 1]  # The first two number are the sample index and timestamp

        values = values * self.a[ch_index]  # a factor
        values = values + self.b[ch_index]  # b factor
        return values

    def getTimeFloat32(self):
        """
        This method get the time from the analog channel
        """
        str_struct = 'i' + 'i' + str(self.A) + 'h' + str(int(numpy.ceil((float(self.D) / float(16))))) + 'H'
        # Number of bytes per sample:
        # this ecuation is explaining in the page 25 of the comtrade format 1999
        NB = 4 + 4 + self.A * 2 + int(numpy.ceil((float(self.D) / float(16)))) * 2

        # Number of samples:
        N = self.getNumberOfSamples()

        # Empty column vector for the time:
        Time = numpy.empty((N, 1))

        # Reading the Time from DatFileContent string:
        for i in range(N):
            data = struct.unpack(str_struct, self.DatFileContent[i * NB:(i * NB) + NB])
            Time[i] = data[1]  # The second column is the time

        Time = Time * self.timemul  # a factor

        return Time
    
    def getDigitalFloat32(self, ChNumber):
        """
        Retourn the digital value 0 or 1
        """

        if not self.DatFileContent:
            print("No data file content. Use the method ReadDataFile first")
            return 0

        if (ChNumber > self.D):
            print("Digital channel number greater than the total number of channels.")
            return 0

        # Fomating string for struct module:
        str_struct = 'i' + 'i' + str(self.A) + 'h' + str(int(numpy.ceil((float(self.D) / float(16))))) + 'H'
        # Number of bytes per sample:
        NB = 4 + 4 + self.A * 2 + int(numpy.ceil((float(self.D) / float(16)))) * 2
        # Number of samples:
        N = self.getNumberOfSamples()

        # Empty column vector:
        values = numpy.empty((N, 1))
        # Number of the 16 word where digital channal is. Every word contains
        # 16 digital channels:
        byte_number = int(numpy.ceil((ChNumber) / 16))
        # Value of the digital channel. Ex. channal 1 has value 2^0=1, channel
        # 2 has value 2^1 = 2, channel 3 => 2^2=4 and so on.
        digital_ch_value = 1 << (ChNumber - 1 - (byte_number - 1) * 16)

        # Reading the values from DatFileContent string:
        for i in range(N):
            data = struct.unpack(str_struct, self.DatFileContent[i * NB:(i * NB) + NB])

            values[i] = (digital_ch_value & data[self.A + 1 + byte_number]) * 1 / digital_ch_value

            # Return the array.
        return values


    def getAnalogASCCI(self, ChNumber):
        """
        Return the analogs channels if the format of the comtrade is ASCCI
        """

        N = self.getNumberOfSamples()
        values = numpy.empty((N, 1))
        ch_index = self.An.index(ChNumber)

        for i, line in enumerate(self.DatFileContent):
            line = line.split(',')
            values[i] = line[ChNumber + 1]  # The first two number are the sample index and timestamp

        values = values * self.a[ch_index]  # a factor
        values = values + self.b[ch_index]  # b factor
        values = values * (self.primary[ChNumber-1]/self.secondary[ChNumber-1])
        return values
    
    def getTimeASCCI(self):
        N = self.getNumberOfSamples()
        Time = numpy.empty((N, 1))
        for i, line in enumerate(self.DatFileContent):
            line = line.split(',')
            Time[i] = line[1]  # The first two number are the sample index and timestamp

        return Time
    
    def getDigitalASCCI(self, ChNumber):
        N = self.getNumberOfSamples()
        values = numpy.empty((N, 1))
        for i, line in enumerate(self.DatFileContent):
            line = line.split(',')
            values[i] = line[1 + self.A + ChNumber]  # The first two number are the sample index and timestamp

        return values
    
    def getAnalogChannelsNumber(self):
        """
        Returns the COMTRADE number of analog channels
        The number to be given is the same of the COMTRADE header.
        """
        return self.A

    def getDigitalChannelsNumber(self):
        """
        Returns the Cnumber of  Digital channels
        The number to be given is the same of the COMTRADE header.
        """
        return self.D
    
    def window_rms(self,ChNumber,cicles):
        """
        Get the rms value from signal with x cicles of length, according to the sample rate and frequency.

        Note: For 60 Hz select exact multiples, for example 3,6,9... cicles for better estimation
        """
        window_size=cicles*ceil(self.samp[0]/self.lf)
        a=self.getAnalogChannel(ChNumber)
        return numpy.sqrt(sum([a[window_size-i-1:len(a)-i]**2 for i in range(window_size-1)])/window_size).flat


