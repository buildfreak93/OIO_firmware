import RPi.GPIO as GPIO
import sys


GPIO.setmode(GPIO.BOARD)
GPIO.setwarnings(False)

#while(1):
GPIO.cleanup()
i = int(sys.argv[1])
key1 = (i & 0b0001) != 0
key2 = (i & 0b0010) != 0
key3 = (i & 0b0100) != 0
GPIO.cleanup()
GPIO.setmode(GPIO.BOARD)
GPIO.setup(11,GPIO.OUT)
GPIO.setup(13,GPIO.OUT)
GPIO.setup(15,GPIO.OUT)
GPIO.output(11,key1)
GPIO.output(13,key2)
GPIO.output(15,key3)

