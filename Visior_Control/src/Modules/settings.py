import configparser as cfp
import os

class CameraSettings():
    config_file = "SystemSettings.cfg"
    settings_dict = ""

    def __init__(self):
        if os.path.exists(self.config_file):
            config = cfp.RawConfigParser()
            config.read(self.config_file)
            self.settings_dict = dict(config.items("camera_settings"))
        else:
            print("Error Setting File Not Found ")

    def getCamResolution(self):
        return self.settings_dict.get('cam_resolution')

    def getCamFrameDim(self, which_dim):
        if which_dim.lower() == "width":
            return int(self.settings_dict.get('cam_frame_dim').split("x")[0])
        elif which_dim.lower() == "height":
            return int(self.settings_dict.get('cam_frame_dim').split("x")[1])
        else:
            raise CameraSettings()


class BasicSettings(CameraSettings):
    config_file = "SystemSettings.cfg"
    settings_dict = ""

    def __init__(self):
        super().__init__()
        if os.path.exists(self.config_file):
            config = cfp.RawConfigParser()
            config.read(self.config_file)
            self.settings_dict = dict(config.items("activity_settings"))
        else:
            print("Error Setting File Not Found ")

    def getResolution(self):
        return self.settings_dict.get('resolution')

    def isOverRideAlloweded(self):
        return self.settings_dict.get('remove_default_window').lower() == "true"

    def getBgColor(self):
        return self.settings_dict.get('background_color')


class Settings(BasicSettings):
    def __init__(self):
        super().__init__()


class SensorSettings:
    config_file = "SystemSettings.cfg"
    settings_dict = ""

    FRONT_IR_PIN = ""
    BOTTOM_IR_PIN = ""

    FRONT_LEFT_MOTOR_PIN = ""
    FRONT_RIGHT_MOTOR_PIN = ""

    BACK_RIGHT_MOTOR_PIN = ""
    BACK_LEFT_MOTOR_PIN = ""
    
    VERTICAL_LOOK = ""
    HORIZONTAL_LOOK = ""

    @staticmethod
    def __getIntList__(Str):
        list_ = []
        list_ = Str.split(":")
        list_ = [int(i) for i in list_]
        return list_.copy()

    def __init__(self):
        if os.path.exists(self.config_file):
            config = cfp.RawConfigParser()
            config.read(self.config_file)
            self.settings_dict = dict(config.items("sensor_settings"))

            self.FRONT_IR_PIN = int(self.settings_dict.get("front_ir_pin"))
            self.BOTTOM_IR_PIN = int(self.settings_dict.get('bottom_ir_pin'))

            self.FRONT_LEFT_MOTOR_PIN = tuple(self.__getIntList__(self.settings_dict.get('front_left_motor_pin')))
            self.FRONT_RIGHT_MOTOR_PIN = tuple(self.__getIntList__(self.settings_dict.get('front_right_motor_pin')))
            self.BACK_LEFT_MOTOR_PIN = tuple(self.__getIntList__(self.settings_dict.get('back_left_motor_pin')))
            self.BACK_RIGHT_MOTOR_PIN = tuple(self.__getIntList__(self.settings_dict.get('back_right_motor_pin')))
            
            self.HORIZONTAL_LOOK = int(self.settings_dict.get("horizontal_camera_pan_pin"))
            self.VERTICAL_LOOK = int(self.settings_dict.get("vertical_camera_pan_pin"))
            
            # print(self.FRONT_LEFT_MOTOR_PIN,self.FRONT_RIGHT_MOTOR_PIN,self.BACK_RIGHT_MOTOR_PIN,self.BACK_LEFT_MOTOR_PIN)
        else:
            print("Error Setting File Not Found ")

    def getTestTimeOut(self):
        return int(self.settings_dict.get("test_timeout"))


if __name__ == "__main__":
    # s = Settings()
    # print(s.getResolution(), s.isOverRideAlloweded())
    SensorSettings()
