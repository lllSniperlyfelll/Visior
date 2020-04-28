from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import DistanceSensor
from gpiozero import MotionSensor as GroundSensor
from time import sleep
import os
from os import path

class CaughtDetection():
	UsonicSensorObject = ""
	IrSensorObject = ""

	def __init__(self):
		#if not os.path.exists("test_dir"):
			#os.system("sudo mkdir test_dir")
		os.system("sudo pigpiod")
		factory = PiGPIOFactory()
		print("factory init")		
		self.UsonicSensorObject = DistanceSensor(echo=12,trigger=16,max_distance=1000,pin_factory=factory)	
		self.IrSensorObject = GroundSensor(5)
		
	def isinThreshold(self,dis):
		if  5 <= dis <=10:
			return True
		return False

		
	def onGround(self):
		ir = self.IrSensorObject
		usonic = self.UsonicSensorObject
		
		usonic_distance = round(self.UsonicSensorObject.distance*100,4) 
		ir_state = not ir.motion_detected

		if ir_state == True and self.isinThreshold(usonic_distance) == True:
			return True
		else:
			#os.system("sudo rm -rf test_dir")
			#print("Deleted test_dir....")
			return False
			




if __name__ == "__main__":
	c = CaughtDetection()
	#while True:
	#	c.isCaught()
