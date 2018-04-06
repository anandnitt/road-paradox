#!/usr/bin/env python

import numpy as np
import cv2
import socket
import time 
import datetime
port=5091
s=socket.socket()
s.bind(('192.168.43.18',port))
s.listen(5)
global data

print 'server started'

i=0

cap=cv2.VideoCapture(1)
#fourcc=cv2.VideoWriter_fourcc(*'XVID')
#out=cv2.VideoWriter('output.avi',fourcc,20.0,(640,480))
hhh=0
f1=open("speed.txt","w+")
f2=open("dist.txt","w+")
f3=open("time.txt","w+")
while True:
	ret,frame=cap.read()
	#cv2.imshow('dd',frame)
	#cv2.waitKey(10000)
	frame=cv2.flip(frame,-1)
	if hhh==0:
		##conn,addr=s.accept()
		hhh+=1
		print 'got'
	
	rows,cols,ch=frame.shape
	pts1 = np.float32([[289,25],[371,17],[316,475],[467,477]])
	pts2 = np.float32([[0,0],[160,0],[0,500],[160,500]])
	
	M = cv2.getPerspectiveTransform(pts1,pts2)
	dst = cv2.warpPerspective(frame,M,(160,500))

	hsv=cv2.cvtColor(dst,cv2.COLOR_BGR2HSV)

	red_lower=np.array([0,100,160],np.uint8)
	red_upper=np.array([55,255,255],np.uint8)

	red=cv2.inRange(hsv, red_lower, red_upper)

	_,contours,h = cv2.findContours(red,1,2)
	c = max(contours, key = cv2.contourArea)
	approx = cv2.approxPolyDP(c,0.01*cv2.arcLength(c,True),True)

	M = cv2.moments(c)
	cx = int(M['m10']/M['m00'])
	cy = int(M['m01']/M['m00'])

	x=2  ##signal time
	t=0 ##signal covered time
	dist=(356*cy)/499
###signal time=1s
	speed=(int)((dist/(x-t))*0.314);
	if speed>80:
		speed=(int)((dist/((x-t)+x))*0.314)
	if speed<30:
		speed=30
	f1.write((str)(speed))
	f1.write("\n")
	f2.write((str)(dist))	
	f2.write("\n")
	f3.write((str)(time.time()))
	f3.write("\n")
	print "Distance from signal",dist
	print "Predicted Speed is ",(speed)
	time.sleep(100)
	#print "Current time is:",time.time()-1508188550
	#conn.send((chr)(speed))
	#conn.send((chr)(speed))
	#conn.send((chr)(speed))
	#conn.send((chr)(speed))
	cv2.imshow('Transformed',dst)
	cv2.imshow('Real',frame)

	
	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
