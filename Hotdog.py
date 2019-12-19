import RPi.GPIO as GPIO

import time

import picamera

import datetime

import smtplib, os, pickle

import cv2

from email.mime.text import MIMEText

from email.mime.multipart import MIMEMultipart

from email.mime.base import MIMEBase

from email import encoders

from email.message import EmailMessage

from email.header import Header

 

#raspberry 

GPIO.setmode(GPIO.BOARD)

soundpin = 7

GPIO.setup(soundpin,GPIO.IN)

 

#model

classNames = {0: 'background',

              1: 'person', 2: 'bicycle', 3: 'car', 4: 'motorcycle', 5: 'airplane', 6: 'bus',

              7: 'train', 8: 'truck', 9: 'boat', 10: 'traffic light', 11: 'fire hydrant',

              13: 'stop sign', 14: 'parking meter', 15: 'bench', 16: 'bird', 17: 'cat',

              18: 'dog', 19: 'horse', 20: 'sheep', 21: 'cow', 22: 'elephant', 23: 'bear',

              24: 'zebra', 25: 'giraffe', 27: 'backpack', 28: 'umbrella', 31: 'handbag',

              32: 'tie', 33: 'suitcase', 34: 'frisbee', 35: 'skis', 36: 'snowboard',

              37: 'sports ball', 38: 'kite', 39: 'baseball bat', 40: 'baseball glove',

              41: 'skateboard', 42: 'surfboard', 43: 'tennis racket', 44: 'bottle',

              46: 'wine glass', 47: 'cup', 48: 'fork', 49: 'knife', 50: 'spoon',

              51: 'bowl', 52: 'banana', 53: 'apple', 54: 'sandwich', 55: 'orange',

              56: 'broccoli', 57: 'carrot', 58: 'hot dog', 59: 'pizza', 60: 'donut',

              61: 'cake', 62: 'chair', 63: 'couch', 64: 'potted plant', 65: 'bed',

              67: 'dining table', 70: 'toilet', 72: 'tv', 73: 'laptop', 74: 'mouse',

              75: 'remote', 76: 'keyboard', 77: 'cell phone', 78: 'microwave', 79: 'oven',

              80: 'toaster', 81: 'sink', 82: 'refrigerator', 84: 'book', 85: 'clock',

              86: 'vase', 87: 'scissors', 88: 'teddy bear', 89: 'hair drier', 90: 'toothbrush'}

 

 

def id_class_name(class_id, classes):

    for key, value in classes.items():

        if class_id == key:

            return value

 

 

model = cv2.dnn.readNetFromTensorflow('ExploreOpencvDnn/models/frozen_inference_graph.pb',

                                      'ExploreOpencvDnn/models/ssd_mobilenet_v2_coco_2018_03_29.pbtxt')

 

 

 

while True:

	soundlevel=GPIO.input(soundpin)

	print("sound",soundlevel)

	if soundlevel==0:

		print("1111")

		

		time.sleep(0.5)

	else:

		print("camera on")

		with picamera.PiCamera() as camera:

			camera.resolution = (300,300)

			now = datetime.datetime.now()

			filename = now.strftime('/home/pi/Videos/%Y-%m-%d-%H:%M:%S')

			camera.start_recording(output = filename + '.h264')

			camera.wait_recording(10)

			camera.stop_recording()

			camera.start_preview() # tkwls

			time.sleep(1)

			camera.stop_preview()

			camera.capture(filename+ '.jpg') 

			print("camera off")

 

		image = cv2.imread(filename+'.jpg')

		image_height, image_width, _ = image.shape

		model.setInput(cv2.dnn.blobFromImage(image, size=(300, 300), swapRB=True))

		output = model.forward()

		# print(output[0,0,:,:].shape)

 

		print("aaaa")

		for detection in output[0, 0, :, :]:

		    confidence = detection[2]

		    if confidence > .5:

		        class_id = detection[1]

		        class_name=id_class_name(class_id,classNames)

		        print(str(str(class_id) + " " + str(detection[2])  + " " + class_name))

		        box_x = detection[3] * image_width

		        box_y = detection[4] * image_height

		        box_width = detection[5] * image_width

		        box_height = detection[6] * image_height

		        cv2.rectangle(image, (int(box_x), int(box_y)), (int(box_width), int(box_height)), (23, 230, 210), thickness=1)

		        cv2.putText(image,class_name ,(int(box_x), int(box_y+.05*image_height)), cv2.FONT_HERSHEY_SIMPLEX,(.005*image_width),(0, 0, 255))

	        

		cv2.imwrite(filename+"_detection.jpg",image)

 

 

 

 

 

 

		#stmp

		s = smtplib.SMTP('smtp.gmail.com',587)

		s.ehlo()

		s.starttls()

		s.login('yongwhan11@gmail.com','wjd!615069')

	

		msg= MIMEMultipart()

		msg['subject']="현재 신호를 감지하여 영상을 보냅니다."

		#msg.set_content("test")

		msg['From']='yongwhan11@gmail.com'

		msg['To']='yongwhan11@gmail.com'

 

		file= filename+".h264"

		fp = open(file,'rb')

		file_data = MIMEBase('application','octet-stream')

		file_data.set_payload((fp).read())

		encoders.encode_base64(file_data)

		file_data.add_header('Content-Disposition',"attachment; filename="+file)

		msg.attach(file_data)

		

 

		fileimage= filename+"_detection.jpg"

		fp = open(fileimage,'rb')

		file_data = MIMEBase('application','octet-stream')

		file_data.set_payload((fp).read())

		encoders.encode_base64(file_data)

		file_data.add_header('Content-Disposition',"attachment; filename="+fileimage)

		msg.attach(file_data)

		

		s.send_message(msg)

		s.quit()

 

 

 