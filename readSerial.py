# Enable pyserial extensions
import pyftdi.serialext

# Open a serial port on the FTDI device interface @ 9600 baud
port = pyftdi.serialext.serial_for_url('ftdi://ftdi:ft-x:08-15/1', baudrate=9600)

# Send bytes
#port.write(b'0')
port.write('0')

print("aaayyyyy it works")
# I just had to update the user group

# Receive bytes
#data = port.read(3)
#print(data.decode('UTF-8'))


#print('0')
# Encoding converts strings to bytes
#print('0'.encode('UTF-8'))
#print(len('0'.encode('UTF-8')))
# Decoding converts bytes to strings
#print(b'0'.decode('UTF-8'))
#print(len(b'0'.decode('UTF-8')))