from gpiozero.pins.pigpio import PiGPIOFactory
from gpiozero import DistanceSensor
from .CameraPanDriver import AngularSweep 
from time import sleep

class UltraSonicControl(AngularSweep):
	ECHO_PIN = 23
	TRIGGER_PIN = 24
	SensorObject  = ""
	min_distance = 70
	
	def __init__(self):
		super().__init__()
		factory = PiGPIOFactory()
		self.SensorObject =DistanceSensor(echo=self.ECHO_PIN,trigger=self.TRIGGER_PIN,max_distance=1000,pin_factory=factory)
		print("UltrasonicSensor Up ..")
	

	def checkArea(self,min_distance = 70):
		sensor_dis = self.SensorObject.distance
		AlertDistance = min_distance/100 
		if sensor_dis <= AlertDistance:
			return (False,round(sensor_dis*100,3))
		else:
			return (True,round(sensor_dis*100,3))

	
	def CheckLeft(self,angle_left = 180):
		self.HorizontalAngleChange(angle_left)
		sleep(1)
		area_data_left = self.checkArea(self.min_distance)
		print(area_data_left)
		return area_data_left


	def CheckRight(self,angle_right = 0):
		self.HorizontalAngleChange(angle_right)
		sleep(1)
		area_data_right = self.checkArea(self.min_distance)
		print(area_data_right)
		return area_data_right

	
	def CheckFront(self):
		self.AutoReset()
		area_data_front = self.checkArea(self.min_distance)
		print(area_data_front)
		return area_data_front


		
		
if  __name__ =="__main__":
	s = UltraSonicControl()
	while True:
		s.CheckRight()
	
