import numpy
import os
from pathlib import Path 

class DataAccess():
    def __init__(self):
        self.rootPath = os.path.abspath(os.path.dirname(__file__))
        self.detectionsLearnPath = self.makeDirs(os.path.join(self.rootPath, "detections", "learn"))
        self.detectionsTagPath = self.makeDirs(os.path.join(self.rootPath, "detections", "tag"))
        self.detectionsRenderedImagePath = self.makeDirs(os.path.join(self.rootPath, "detections", "renderedimage"))

    def saveDetections(self, filePath, results):
        fileName = self.getFileNameFromPath(filePath)

        data = results.pandas().xyxy[0]
        print(fileName)
        print(data)

        #learn mode
        columnNames = ["class", "xmin", "ymin", "xmax", "ymax"]
        data = self.fixDataSet(data, columnNames)

        detectionFilePath = os.path.join(self.detectionsLearnPath, fileName + ".csv")
        data.to_csv(detectionFilePath, header=None, index=False)
        
        #detectionInfo
        columnNames = ["class", "xmin", "ymin", "xmax", "ymax", "name", "confidence"]
        data = self.fixDataSet(data, columnNames)

        detectionFilePath = os.path.join(self.detectionsTagPath , fileName + ".csv")
        data.to_csv(detectionFilePath, index=False)
        
        #save image
        results.save(self.detectionsRenderedImagePath)

    def fixDataSet(self, data, columnNames):   
        return data.reindex(columns = columnNames)

    def makeDirs(self, path):
        exists = os.path.exists(path)
        if not exists:
            os.makedirs(path)
        return path
    
    def getFileNameFromPath(self, filePath):
        return self.getFileNammeWithExtensionFromPath(filePath).split('.')[0]

    def getFileNammeWithExtensionFromPath(self, filePath):
        return Path(filePath).name
    
    def getDetectionsRenderedImagePath(self, imagePath):
        fileNameWithExtenstion = self.getFileNammeWithExtensionFromPath(imagePath)
        return os.path.join(self.detectionsRenderedImagePath, fileNameWithExtenstion)