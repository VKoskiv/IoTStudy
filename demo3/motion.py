import RPi.GPIO as GPIO
import time
import picamera

GPIO.setmode(GPIO.BCM)
pin = 21
camera = picamera.PiCamera()
GPIO.setup(pin, GPIO.IN)

end = time.time() + 10

while time.time() < end:
	if GPIO.input(pin) is 1:
		camera.capture('image.jpg')
		print('picture taken!')
		break
	time.sleep(1)

GPIO.cleanup()
