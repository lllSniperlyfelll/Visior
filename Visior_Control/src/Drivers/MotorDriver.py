import RPi.GPIO as gpio
from time import sleep

pwm = ""
pwm_l = ""
def InitilaizePins():
	global pwm
	global pwm_l
	gpio.setmode(gpio.BCM)
	gpio.setwarnings(False)
	gpio.setup([2,3],gpio.OUT)   
	gpio.setup(26,gpio.OUT)        
	gpio.setup(19,gpio.OUT)
	gpio.setup(6,gpio.OUT)        
	gpio.setup(13,gpio.OUT)

	ResetMotorPins()
	pwm = gpio.PWM(2,100)
	pwm_l = gpio.PWM(3,100)

	pwm.start(0)
	pwm_l.start(0)
	gpio.output(6,True)
	gpio.output(26,True)

def ResetMotorPins():
	gpio.output(26,False)
	gpio.output(19,False)
	gpio.output(6,False)
	gpio.output(13,False)
	

def StopMotor():
	global pwm
	global pwm_l
	pwm.ChangeDutyCycle(0)
	pwm_l.ChangeDutyCycle(0)

def MoveBackward():
	global pwm
	global pwm_l
	print("Called MoveBackwards ###############")
	#ResetMotorPins()
	gpio.output(6,False)
	gpio.output(13,True)
	gpio.output(19,False)
	gpio.output(26,True)
	#pwm.ChangeDutyCycle(60)
	#pwm.ChangeDutyCycle(60)
	
	pwm.ChangeDutyCycle(60)
	pwm_l.ChangeDutyCycle(60)
	
	
def MoveLeft():
	global pwm
	global pwm_l
	print("Called MoveLeft ###############")
	#ResetMotorPins()
	gpio.output(6,True)
	gpio.output(13,False)
	gpio.output(19,False)
	gpio.output(26,True)
	
	pwm.ChangeDutyCycle(60)
	pwm.ChangeDutyCycle(60)
	
	pwm.ChangeDutyCycle(100)
	pwm_l.ChangeDutyCycle(100)
	

def MoveRight():
	global pwm
	global pwm_l
	print("Called MoveRight ###############")
	#ResetMotorPins()
	gpio.output(6,False)
	gpio.output(13,True)
	gpio.output(19,True)
	gpio.output(26,False)
	pwm.ChangeDutyCycle(60)
	pwm.ChangeDutyCycle(60)
	
	pwm.ChangeDutyCycle(100)
	pwm_l.ChangeDutyCycle(100)
	

def MoveForward():
	global pwm
	global pwm_l
	print("Called MoveFroward ###############")
	gpio.output(6,True)
	gpio.output(13,False)
	gpio.output(19,True)
	gpio.output(26,False)
	#pwm.ChangeDutyCycle(60)
	#pwm.ChangeDutyCycle(60)
	
	pwm.ChangeDutyCycle(30)
	pwm_l.ChangeDutyCycle(30)


if __name__ == "__main__":
	#InitilaizePins()
	#MoveForward()
	#MoveBackward()
	#MoveRight()
	#MoveLeft()
	#sleep(10)
	ResetMotorPins()
