import serial
import struct
SINE_WAVE = 10
ARBITRARY_WAVE = 11
DAC_COSINE_ATTEN_DB_0 = 0
DAC_COSINE_ATTEN_DB_6 = 1
DAC_COSINE_ATTEN_DB_12 = 2
DAC_COSINE_ATTEN_DB_18 = 3
MAX_FREQ = 1000000;
ARBITRARY_MAX_BUFFER_LENGTH = 2048
def clamper(x):
    if x > 1:
        return 1
    elif x < 0:
        return 0
    return x
class CircuitKing:
    def __init__(self,port,check_response=False):
        self.ser = serial.Serial(port, 115200,timeout=10)
        self.check_response = check_response
    
    def sine_wave(self,freq,attenuation):
        first_byte = struct.pack('B',SINE_WAVE)
        #frequency packed as a 32 bit integer in little endian format
        freq_bytes = struct.pack('<I',freq)
        attenuation_bytes = struct.pack('B',attenuation)
        data_packet = first_byte + freq_bytes + attenuation_bytes
        print("Sending Data")
        self.ser.write(data_packet)

        if(self.check_response):
            print("Checking for Response")
            print(self.ser.readlines())
    
    def arbitrary_wave(self,freq,waveform):
        samples =  2048
        sampling_frequency = samples*freq
        if(sampling_frequency > MAX_FREQ):
            sampling_frequency = MAX_FREQ
            samples = sampling_frequency//freq
        time_array = [i/samples for i in range(samples)]
        wave = [int((clamper(waveform(t)))*255) for t in time_array]
        buffer = bytearray(9+ARBITRARY_MAX_BUFFER_LENGTH)
        command_packet = struct.pack('B',ARBITRARY_WAVE)
        freq_buffer = struct.pack('<i',sampling_frequency)
        print(sampling_frequency)
        print(samples)
        size_buffer = struct.pack('<i',samples)
        print(wave)
        wave_buffer = bytes(wave)
        print(wave_buffer)
        data_packet = command_packet + freq_buffer + size_buffer + wave_buffer
        buffer[:len(data_packet)] = data_packet
        # print(len(buffer))
        print("Sending Data")
        self.ser.write(buffer)
        if(self.check_response):
            print("Checking for Response")
            print(self.ser.readlines())
        
        
        

