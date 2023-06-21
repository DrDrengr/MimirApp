from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import Qt, QSize

class ImageLabel(QLabel):
    def __init__(self, parent):
        super(ImageLabel, self).__init__()

        self.parent = parent
        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop Images Here! \n\n')
        self.setStyleSheet('''
            border: 5px dashed #ac0e28;
            font-size: 70px;
        ''')
        self.resize(1280, 720)
        self.setMinimumSize(QSize(1280, 720))
        self.setMaximumSize(QSize(1280, 720))

    def setPixmap(self, image):
        super().setPixmap(image)