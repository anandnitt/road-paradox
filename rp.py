
#!/usr/bin/env python
import numpy as np
import cv2

cap=cv2.VideoCapture(-1)

while True:
	ret,frame=cap.read()
	
	rows,cols,ch=frame.shape
	pts1 = np.float32([[298,0],[369,0],[285,478],[428,479]])
	pts2 = np.float32([[0,0],[160,0],[0,500],[160,500]])
	
	M = cv2.getPerspectiveTransform(pts1,pts2)
	dst = cv2.warpPerspective(frame,M,(160,500))

	hsv=cv2.cvtColor(dst,cv2.COLOR_BGR2HSV)

	red_lower=np.array([0,100,160],np.uint8)
	red_upper=np.array([55,255,255],np.uint8)

	red=cv2.inRange(hsv, red_lower, red_upper)
	resr=cv2.bitwise_and(dst, dst,mask=red)	

	blur = cv2.GaussianBlur(resr,(5,5),0)
	gray = cv2.cvtColor(blur, cv2.COLOR_RGB2GRAY)	
	ret,thresh = cv2.threshold(gray,3,255,cv2.THRESH_BINARY)
	
	_,contours,h = cv2.findContours(thresh,1,2)
	c = max(contours, key = cv2.contourArea)
	approx = cv2.approxPolyDP(c,0.01*cv2.arcLength(c,True),True)

	M = cv2.moments(c)
	cx = int(M['m10']/M['m00'])
	cy = int(M['m01']/M['m00'])

	dist=(356*cy)/499
	print "Real_Dist is %d" %dist
	
	cv2.imshow('Transformed',dst)
	cv2.imshow('Real',frame)
	cv2.imshow('Threshold',resr)

	if cv2.waitKey(1) & 0xFF == ord('q'):
		break

cap.release()
cv2.destroyAllWindows()
