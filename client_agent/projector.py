#!/usr/bin/env python
import serial
import sys
import time
import logging

poweron =[0xBE,0xEF,0x03,0x06,0x00,0xba,0xd2,0x01,0x00,0x00,0x60,0x01,0x00]
poweroff=[0xBE,0xEF,0x03,0x06,0x00,0x2a,0xd3,0x01,0x00,0x00,0x60,0x00,0x00]
powerpoll=[0xBE,0xEF,0x03,0x06,0x00,0x19,0xd3,0x02,0x00,0x00,0x60,0x00,0x00]

def a2s(arr):
  return ''.join(chr(b) for b in arr)

def SendCommand(InputBytes):
  logging.debug("Sending command %s" % (":".join("{:02x}".format(ord(chr(c))) for c in command)))
  uart.write(a2s(command))
  time.sleep(1)
  buf=uart.inWaiting()
  if (buf > 0):
    readbytes=uart.read(buf)
    logging.debug("bufsize is %d" % buf)
    logging.debug("Response: %s" % (":".join("{:02x}".format(ord(c)) for c in readbytes)))
    if (ord(readbytes[0]) == 0x06):
      return "OK"
    elif (ord(readbytes[0]) == 0x15):
      return "ERROR"
    elif (ord(readbytes[0]) == 0x1D):
      return ":".join("{:02x}".format(ord(c)) for c in readbytes[1:])
  else:
        return False

#Main program begins here
logging.basicConfig(level=logging.DEBUG)

if len(sys.argv) < 2:
    sys.stderr.write('Usage: %s [1/0]\n' % sys.argv[0])
    sys.exit(1)

if sys.argv[1] == "pollpower":
        command=powerpoll
elif sys.argv[1] == "1":
        command=poweron
elif sys.argv[1] == "0":
        command=poweroff

uart=serial.Serial("/dev/ttyAMA0",19200)
uart.open()

j=0

while (j<=5):
        retval=SendCommand(command)
        if (retval):
                logging.debug("Response from SendCommand is %s" % retval)
                j=100
        else:
                j=j+1

uart.close()
if (j==100):
 sys.exit(0)
else:
 sys.exit(1)

