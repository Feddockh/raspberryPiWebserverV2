# Enable pyserial extensions
import pyftdi.serialext

# Open a serial port on the FTDI device interface @ 9600 baud
port = pyftdi.serialext.serial_for_url('ftdi://ftdi:ft-x:08-15/1', baudrate=9600)

# Send b'2' in order to begin the clock
port.write('2'.encode('UTF-8'))
