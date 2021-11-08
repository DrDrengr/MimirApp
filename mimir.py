import torch
from PIL import Image
from pathlib import Path
import cv2
import numpy as np

class MimirCore():
    def __init__(self):
        super().__init__()

        self.best_path = 'C:\\Users\\Daniel\\Desktop\\Mimir\\MimirApp\\model\\custom\\v1\\exp7\\weights\\best.pt'
        self.yolo_path = 'ultralytics/yolov5'

        self.model = torch.hub.load(self.yolo_path, 'custom', path=self.best_path)
        

    def recognition(self, file_path):
        print(file_path)

        image = Image.open(file_path) 
        images = [image]
        size = 640

        results = self.model(images, size)

        results.print()
        results.show()
        variable = results.pandas().xyxy[0]
        print(variable)

    def VideoRecognition(self):
        cap = cv2.VideoCapture(0)
        while cap.isOpened():
            ret, frame = cap.read()

            results = self.model(frame)
            cv2.imshow('Yolo', np.squeeze(results.render()))
            if cv2.waitKey(10) & 0xFF == ord('q'):
                break
        cap.release()
        cv2.destroyAllWindows()
