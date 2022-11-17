# Enable pyserial extensions
import pyftdi.serialext

# Open a serial port on the FTDI device interface @ 9600 baud
port = pyftdi.serialext.serial_for_url('ftdi://ftdi:ft-x:08-15/1', baudrate=9600)

# Send bytes
port.write('0'.encode('UTF-8'))

# Receive bytes
data1 = port.read(3)
data1 = data1.decode('UTF-8')

if data1 == 'END':
    port.write('1'.encode('UTF-8'))
    data2 = port.read(3)
    data2 = data2.decode('UTF-8')
    print(data2)

print(data1)
