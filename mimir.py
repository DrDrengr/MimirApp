import torch
from PIL import Image
import cv2
import numpy as np
import os
from dataAccess import DataAccess

class MimirCore():
    def __init__(self):
        super().__init__()
        self.yolo_path = 'ultralytics/yolov5'
        self.rootPath = os.path.abspath(os.path.dirname(__file__))
        self.best_path = os.path.join(self.rootPath , "model/exp7/best.pt")

        self.imageSize = 640
        self.model = torch.hub.load(self.yolo_path, 'custom', path=self.best_path)
        self.dataAccess = DataAccess()

    def PhotoRecognition(self, imagePaths):
        newImagePaths = []
        for imagePath in imagePaths:
            imageOpened = Image.open(imagePath) 
            imagesOpened = [imageOpened]

            results = self.model(imagesOpened, self.imageSize)
            imageOpened.close()

            self.dataAccess.saveDetections(imagePath, results)
            newImagePath = self.dataAccess.getDetectionsRenderedImagePath(imagePath)
            newImagePaths.append(newImagePath)
        return newImagePaths  


    def VideoRecognition(self):
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()

            results = self.model(frame, self.imageSize)
            cv2.imshow('Mimir - Live Object Detection Demo - press q to exit', np.squeeze(results.render()))

            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
