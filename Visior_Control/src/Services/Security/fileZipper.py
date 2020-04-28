from zipfile import *
import os
import pyAesCrypt
import hashlib
from time import sleep


def cleanUp(args):
   for itr in args:
     if os.path.exists (itr):
       os.remove(itr)


def getFullPath(fileName):
  fullPathas = os.path.abspath(fileName) 
  return fullPathas

#os.system("rm "+getFullPath("../../../Snapshots/")+ "*.jpg.encry ")


class keyValidator:

  def validateKey(self, inputKey):
    keyy = getCode().getKey()
    print(keyy)
    if(inputKey == keyy):
      return zipIt().openZip(inputKey) == True
    else:
      return False #("Error in unlocking")


class getCode:

  def getKey(self, filePaths = "./"):
    allFiles = os.listdir(filePaths)
    print("Got file path as -> "+filePaths)
    print(allFiles)
    raw_key = ""
    for itr in allFiles:
      if(".py" in itr):
        file = open(filePaths+itr,"r")
        raw_key += file.read()
    final_key = (hashlib.sha256(raw_key.encode()).hexdigest())
    print(final_key)
    return(final_key)


    
class zipIt:
  
  def __init__(self, singleImage = "na"):
    allImages = os.listdir(getFullPath("Snapshots/"))
    self.pushInZip(allImages, singleImage)

  def clearAllData(self):
    mmData = os.listdir(getFullPath("Snapshots"))
    currentPath = getFullPath(os.getcwd())
    fullPath = getFullPath('Snapshots/')
    os.chdir(fullPath)
    for itr in mmData:
      os.system("rm ./"+itr)
    os.chdir(currentPath)
  
  
  def pushInZip(self, allImages,singleImage = "na"):
    #cleanUp([getFullPath("Snapshots.zip")])
    if( singleImage == "na"):
      for images in allImages:
        if(".encry" not in images):
          pyAesCrypt.encryptFile(getFullPath("Snapshots/") + images, getFullPath("Snapshots/") + images + ".encry", getCode().getKey(), 64*1024)
          os.system("rm "+getFullPath("Snapshots/")+ images)
    else:
      print("Single Image")
      pyAesCrypt.encryptFile(getFullPath(singleImage), getFullPath(singleImage) + ".encry", getCode().getKey(), 64*1024)
      os.system("rm "+getFullPath(singleImage))
    #zipFileName = ZipFile(getFullPath("Snapshots.zip"),"a")
    #zipFileName.setpassword(b"12345")
    #with zipFileName as zipper:
      #for images in allImages:cls

        #zipper.write(getFullPath("Snapshots/") + images)
    #pyAesCrypt.encryptFile(getFullPath("Snapshots.zip"), getFullPath("SnapshotsZip.zip.encryp"), getCode().getKey(), 64*1024)
    #cleanUp([getFullPath("Snapshots.zip")])
    #self.clearAllData()
    #print("Deleting dir")
    #os.chdir(getFullPath("../"))
    #print(os.getcwd())
    #os.system("rmdir "+getFullPath("./Snapshots"))
  

  def openZip(self, code):
    try:
        for images in os.listdir(getFullPath("Snapshots/")):
          if(".jpg" in images):
            pyAesCrypt.decryptFile(getFullPath("Snapshots/") + images, getFullPath("Snapshots/") + images.replace(".encry","") , getCode().getKey(), 64*1024)
            os.system("rm "+getFullPath("Snapshots/")+ images)

      #pyAesCrypt.decryptFile(getFullPath("../../../SnapshotsZip.zip.encryp"), getFullPath("../../../")+"Snapshots.zip", code, 64*1024)
      #cleanUp([getFullPath("../../../SnapshotsZip.zip.encryp")])

        print("Files Unlocked")
        return True
    except:
      return False

# Only for testing 
def pseudoOpen():
  try:
    #pyAesCrypt.decryptFile(getFullPath("../../../SnapshotsZip.zip.encryp"), getFullPath("../../../")+"Snapshots.zip", getCode().getKey(getFullPath("../../../")), 64*1024)
    #cleanUp([getFullPath("../../../SnapshotsZip.zip.encryp")])
    #print("Files Unlocked")
    print('51119318aeecb5a629e3966bcf1ec2dec929527434666f458a7e5ec575fb182e' in os.listdir(getFullPath("../../../Snapshots/")))
    for images in os.listdir(getFullPath("../../../Snapshots/")):
      print(images)
      if(".jpg" in images):
        pyAesCrypt.decryptFile(getFullPath("../../../Snapshots/") + images, getFullPath("../../../Snapshots/") + images.replace(".encry","") , getCode().getKey(getFullPath("../../../")), 64*1024)
        os.system("rm "+getFullPath("../../../Snapshots/")+ images)

      #pyAesCrypt.decryptFile(getFullPath("../../../SnapshotsZip.zip.encryp"), getFullPath("../../../")+"Snapshots.zip", code, 64*1024)
      #cleanUp([getFullPath("../../../SnapshotsZip.zip.encryp")])
      print("Files Unlocked")
  except Exception as e:
    print(e)
      

    





















if __name__ == "__main__":
  #zipIt()
  pseudoOpen()
  #getCode().getKey()
