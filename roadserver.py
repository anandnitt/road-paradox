import socket
import time 
port=5078
s=socket.socket()
s.bind(('192.168.43.52',port))
s.listen(5)
global data

print 'server started'

if __name__=="__main__":
    while 1:

        conn,addr=s.accept()
        #print 'got'
        for i in xrange(0,100000):
            if i%2:
                            conn.send('a')
            else:
                            conn.send('b')
            time.sleep(1)
            print 'value sent'

        conn.close()
