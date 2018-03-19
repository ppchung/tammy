#OPENCV TAMMY

import cv2
import numpy as np
import os, subprocess, signal
import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM)
GPIO.setup(4, GPIO.OUT)
GPIO.setup(17, GPIO.OUT)

GPIO.output(4, 0)
GPIO.output(17,0)

imgname = "OPENCV"
brightness = 50
n_white_pix = 0
count = 0
pixel = 200
try:
	while True:
		GPIO.output(17,1)
		#fswebcam --no-banner --set brightness=50% --set contrast=50% 2.png
		p = subprocess.Popen(['sudo', 'fswebcam', '--no-banner', '--set','brightness='+str(brightness)+'%', '--set',' contrast=40%', imgname+'noncrop.png'], stdout=subprocess.PIPE)
		out, err = p.communicate()
		print(out)

		newimage = cv2.imread(imgname+"noncrop.png")
		image = newimage[30:250, 70:280]
		cv2.imwrite(imgname+str(count)+'.png',image)
		# Convert BGR to HSV

		hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

		# define color strenght parameters in HSV

		weaker = np.array([80, 90, 90])

		stronger = np.array([130,255,255])
		# 210-255 blue
		# 40-70 light green

		# Threshold the HSV image to obtain input color

		mask = cv2.inRange(hsv, weaker, stronger)
		cv2.imwrite('MASK.png',mask)
		img = cv2.imread('MASK.png', cv2.IMREAD_GRAYSCALE)
		n_white_pix = np.sum(img == 255)
		print('######################### Number of white pixels:', n_white_pix)

		# cv2.imshow('Result',mask)
		# cv2.imshow('Initial',image)
		# p = subprocess.Popen(['sudo', 'feh', 'MASK.png', 'OPENCV.png'], stdout=subprocess.PIPE)
		# out, err = p.communicate()
		# print(out)
		os.system('sudo feh '+imgname+str(count)+'.png &')
		# os.system('sudo feh MASK.png &')
		# sleep(1)
		if n_white_pix > pixel:
			print("---------------------Target Acquired")
			GPIO.output(4, 1)         # set port/pin value to 1/HIGH/True
		else:
			print("~~~~~~~~~~~~~~~~~~~~~Target Unavailable")
			GPIO.output(4, 0)         # set port/pin value to 0/LOW/False
		if brightness == 40:
			brightness = 50
		else:
			brightness = 40
finally:
	GPIO.cleanup()
