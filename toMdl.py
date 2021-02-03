import clearXML
import toPIM
import time

def startTransformation(filename):
    #mainFile = filename
    mainFile = "D:/Developer Projects/ptl2sml/Insulin_Pump_Actuator2.xml"
    clearXML.makeFiles(mainFile)

    time.sleep(3)
    
    toPIM.startPIMMaker()