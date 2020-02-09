import serial
ser = serial.Serial('/dev/ttyUSB0', timeout=1.0)  # open serial port
#ser = serial.Serial('/dev/pts/4', timeout=1.0)  # open serial port
print('Connected to', ser.name)         # check which port was really used

def write(data: bytes):
    ser.write(data)
    print('-> Wrote', data)

def read():
    print('<- Read', ser.read(255))
    
start = [
    b'\xdd\xa5\x03\x00\xff\xfdw',
    b'\xdd\xa5\x04\x00\xff\xfcw',
    b'\xdd\xa5\x05\x00\xff\xfbw'
]

for cmd in start:
    print(cmd.hex('_'))
    #write(cmd)
    #read()

ser.close()
