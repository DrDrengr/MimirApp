import torch
from PIL import Image
from pathlib import Path

class MimirCore():
    def __init__(self):
        super().__init__()
        

    def recognition(self, file_path):
        best_path = 'C:\\Users\\Daniel\\Desktop\\Mimir\\MimirApp\\model\\custom\\v1\\exp7\\weights\\best.pt'
        yolo_path = 'ultralytics/yolov5'

        print(file_path)

        image = Image.open(file_path) 
        images = [image]
        size = 640

        model = torch.hub.load(yolo_path, 'custom', path=best_path)
        results = model(images, size)

        results.print()
        results.show()
        variable = results.pandas().xyxy[0]
        print(variable)