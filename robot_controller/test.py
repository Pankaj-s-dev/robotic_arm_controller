import serial
import time
#Serial takes two parameters: serial device and baudrate
ser = serial.Serial('/dev/ttyUSB0', 115200)
print(ser.is_open) 

write_b = "hellow boy"

while True:
   ser.write(bytes(write_b, 'utf-8'))
   data = str(ser.readline(), 'UTF-8')
   print(data)
   time.sleep(1)

 