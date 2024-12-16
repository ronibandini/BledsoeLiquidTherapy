# Liquido Terapia Bledsoe
# Roni Bandini, December, 2024
# http://bandini.medium.com
# MIT License
# Versión sin Telegram ni script de carga de target

import face_recognition
import gpiod
import time
import timeit
import datetime
import os
from picamera2 import Picamera2, Preview
from telethon.sync import TelegramClient, events

def writeLog(myLine):
    now = datetime.datetime.now()
    dtFormatted = now.strftime("%Y-%m-%d %H:%M:%S")
    with open('log.txt', 'a') as f:
        myLine=str(dtFormatted)+","+myLine
        f.write(myLine+"\n")

picam2 = Picamera2()

config = picam2.create_still_configuration(
    main={"size": (480, 270)},            
    raw={'size': (2304, 1296)},
    buffer_count=2,
    controls={'FrameRate': 50},
)
picam2.controls.ExposureTime = 10000
picam2.controls.AwbMode = False
picam2.start()

# Settings
relayPin = 18
api_id      = ""
api_hash    = ""
telegramUser = ""
sendTelegram =1
sprayTime=3

chip = gpiod.Chip('gpiochip4')
relayLine = chip.get_line(relayPin)
relayLine.request(consumer="LED", type=gpiod.LINE_REQ_DIR_OUT)


# dataset
known_image = face_recognition.load_image_file("/home/YOURFOLDER/dataset/intruder.jpg")
target_encoding = face_recognition.face_encodings(known_image)[0]

client = TelegramClient('Bledsoe Liquid Therapy', api_id, api_hash)
client.start()

writeLog("Bledsoe Liquid Therapy iniciado")
os.system('clear')
print("Bledsoe Liquid Therapy 1.0 iniciado")
print("")

if sendTelegram==1:
	# no incluido en esta versión
	print("Enviando notificación...")

time.sleep(3)

while True:

	print("Sacando foto...")
	start = timeit.timeit()	
	picam2.capture_file("/home/YOURFOLDER/dataset/take.jpg")
	unknown_image = face_recognition.load_image_file("/home/YOURFOLDER/dataset/take.jpg")
	
	try:
		print("Aplicando IA...")
		unknown_encoding = face_recognition.face_encodings(unknown_image)[0]
		results = face_recognition.compare_faces([target_encoding], unknown_encoding)
		end = timeit.timeit()
		print("Tiempo de inferencia: "+str(round(end - start, 4))+" segundos...")
		print(results)

		if str(results)=="[True]":
			writeLog("Objetivo localizado")
			print("Objetivo localizado...")
			# disparando spray
			print("Disparando spray...")
			relayLine.set_value(1)
			time.sleep(sprayTime)
			relayLine.set_value(0)
			picam2.capture_file("/home/YOURFOLDER/dataset/take2.jpg")

			if sendTelegram==1:
				# no incluido en esta versión
				print("Enviando notificacion...")
			# notificando

		else:
			print("No identificado...")
			if sendTelegram==1:
				# no incluido en esta versión
				print("Enviando notificación...")
				
	except IndexError:
		print("No hay personas")
		pass

cam.release()
