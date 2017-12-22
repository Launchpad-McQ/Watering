import sys
import mcp3008

# Use as: "python get_reading.py <adcnum> <device>".
adcnum = int(sys.argv[1]) #sensor number.
device = int(sys.argv[2]) #DAC "index".

def read_sensor(adcnum, device):
    return mcp3008.readadc(adcnum, device)

print(read_sensor(adcnum, device))
