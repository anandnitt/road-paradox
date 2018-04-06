import socket                   # Import socket module
import serial
import time

ser=serial.Serial('COM7',9600)

s = socket.socket()             # Create a socket object
port = 5078                # Reserve a port for your service.

s.connect(('192.168.43.28', port))


while True:
    print('receiving data...')
    data = s.recv(1024)
    print data[0]
    ser.write(data[0])
    
    time.sleep(1)   
    
    

s.close()
