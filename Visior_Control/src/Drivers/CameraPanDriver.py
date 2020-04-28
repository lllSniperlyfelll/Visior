from time import sleep
import pigpio
import os

class AngularSweep():
	
	NECK_PIN = 17
	HEAD_PIN = 27
	CURRENT_VERTICAL_ANGLE = 500
	CURRENT_HORIZONTAL_ANGLE =500
	AngularPi = ""
	
	def setPigpio(self):
		try:
			os.system("sudo pigpiod")
			print("pigpio deamon is up ...")
		except:
			pass
			
	
	def __init__(self):
		self.setPigpio()
		self.AngularPi = pigpio.pi()
		print("Angular Pi Init")
		#self.AutoReset()
		
	def AutoReset(self,optional_angle_to_reset = 1000):
		
		self.AngularPi.set_servo_pulsewidth(self.NECK_PIN,1110)
		self.AngularPi.set_servo_pulsewidth(self.HEAD_PIN,optional_angle_to_reset)
		#sleep(2)
		print("reset ")
		
	def VerticalAngleChange(self,angle = 0):
		
		if 500<=self.CURRENT_VERTICAL_ANGLE<=2300:
			print(f"Vertical Pan at {angle} degrees")
			self.AngularPi.set_servo_pulsewidth(self.HEAD_PIN,500+angle*9)
			#sleep(0.1)
			self.CURRENT_VERTICAL_ANGLE+=(500+angle+20)
			if self.CURRENT_VERTICAL_ANGLE<500:
				self.CURRENT_VERTICAL_ANGLE = 500
			elif self.CURRENT_VERTICAL_ANGLE>2300:
				self.CURRENT_VERTICAL_ANGLE = 2300
		else:
			self.CURRENT_VERTICAL_ANGLE = 1250
			self.AutoReset()
			
			
	def HorizontalAngleChange(self,horizontal_angle = 0):
		
		if 500<=self.CURRENT_VERTICAL_ANGLE<=2300:
			print(f"HorizontalPan at {horizontal_angle} degrees")
			self.AngularPi.set_servo_pulsewidth(self.NECK_PIN,500+horizontal_angle*8)
			#sleep(0.08)
			self.CURRENT_HORIZONTAL_ANGLE+=(500+horizontal_angle+20)
			if self.CURRENT_HORIZONTAL_ANGLE<500:
				self.CURRENT_HORIZONTAL_ANGLE = 500
			elif self.CURRENT_HORIZONTAL_ANGLE>2300:
				self.CURRENT_HORIZONTAL_ANGLE = 2300
		else:
			self.CURRENT_HORIZONTAL_ANGLE = 1250
			self.AutoReset()
	
	def FreeSweep(self,direction = "vertical"):
		if not direction == "vertical":
			start = 500
		else:
			start=1000
		for i in range(start,2000,1):
			if direction == "vertical":
				print("Sweeping Vertical")
				self.AngularPi.set_servo_pulsewidth(self.HEAD_PIN,i)
				sleep(0.005)
			else:
				print("Sweeping horizontal")
				self.AngularPi.set_servo_pulsewidth(self.NECK_PIN,i)
				sleep(0.005)
		for i in range(2000,start+1,-1):
			if direction == "vertical":
				self.AngularPi.set_servo_pulsewidth(self.HEAD_PIN,i)
				sleep(0.005)
			else:
				self.AngularPi.set_servo_pulsewidth(self.NECK_PIN,i)
				sleep(0.005)
		self.AutoReset()
		
				
		
		
		

class CameraPanDriver(AngularSweep):
	pi = ""
	SWEEP_VAL = 500
	VERTICAL_LOOK_ANGLE = 500
	ROT_SPEED = 20
	
	def __init__(self):
		super().__init__()
		self.pi = pigpio.pi()
		print("Rc Pi init")
		self.SWEEP_VAL = 500
		self.VERTICAL_LOOK_ANGLE = 500
		self.ResetToNormal()
		
	def ResetToNormal(self):
		self.SWEEP_VAL = 1250
		self.VERTICAL_LOOK_ANGLE = 1250
		self.pi.set_servo_pulsewidth(self.NECK_PIN,1250)
		self.pi.set_servo_pulsewidth(self.HEAD_PIN,1250)
		sleep(0.9)
		print("reset ")
		
	def PanLeft(self):
		if self.SWEEP_VAL<=2300:
			self.pi.set_servo_pulsewidth(self.NECK_PIN,self.SWEEP_VAL)
			self.SWEEP_VAL+=self.ROT_SPEED
		else:
			self.ResetToNormal()
	
	def PanRight(self):
		if self.SWEEP_VAL>=500:
			self.pi.set_servo_pulsewidth(self.NECK_PIN,self.SWEEP_VAL)
			self.SWEEP_VAL-=self.ROT_SPEED
		else:
			self.ResetToNormal()
	
	def PanUp(self):
		if self.VERTICAL_LOOK_ANGLE>=500:
			self.pi.set_servo_pulsewidth(self.HEAD_PIN,self.VERTICAL_LOOK_ANGLE)
			self.VERTICAL_LOOK_ANGLE-=self.ROT_SPEED
		else:
			self.ResetToNormal()
	
	def PanDown(self):
		if self.VERTICAL_LOOK_ANGLE<=2000:
			self.pi.set_servo_pulsewidth(self.HEAD_PIN,self.VERTICAL_LOOK_ANGLE)
			self.VERTICAL_LOOK_ANGLE+=self.ROT_SPEED
		else:
			self.ResetToNormal()


