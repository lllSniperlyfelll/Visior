import owncloud
import os
from time import sleep
import json

class getClouds:
    def __init__(self):
        pass
    
    def getLoc(self):
        locations = open(os.getcwd() + "/src/Services/Security/cloudlocations.json")
        locations = json.load(locations)
        cloudIps = []
        for itr in locations["clouds"]:
            cloudIps.append(itr.get("loc"))
        return cloudIps.copy()      




class cloudService:
    localPath =""
    cloudPath = "Snapshots/"
    __CloudAvaliable__ = False
    cloudClients = ["http://192.168.1.105","http://192.168.1.106"]
    counter = -1
    cloudsLocations = getClouds().getLoc()


    def getLocations(self):
        self.counter += 1
        cloudsLocation = self.cloudsLocations

        while self.counter < len(self.cloudsLocations):
            yield cloudsLocation[self.counter]
        

    def __init__(self, imagePath = "na"):
        try:
            for ips in self.getLocations():  
                cl = ips
                print("got cloud location =-> "+cl)  
                self.oc = owncloud.Client(cl)
                self.oc.login('sniperlyfe', 'sniperlyfe')
                print("Loged in")
                self.__CloudAvaliable__ = True
                if(not imagePath == "na"):
                    self.readyPush(os.path.abspath(imagePath))
                break
        except Exception as e:
            print(e)
            print("Retrying ...")
            self.__init__()

    def readyPush(self, imagePath):
        print("File to push to cloud -> "+imagePath)
        try:
            if not (imagePath  == "na"):
                self.oc.put_file(self.cloudPath, imagePath)
                print("File Flew ....")
        except Exception as e:
            self.__CloudAvaliable__ = False
            self.counter = -1
            self.__init__()
            if self.__CloudAvaliable__:
                self.readyPush(imagePath)
            print("Exception in cloud service"+e)

 
if __name__ == "__main__":
    #getClouds().getLoc()
    cloudService().getLocations()