import sys
from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QApplication, QMainWindow
from buttons import ActionButton
from mimir import MimirCore
from imageWindow import ImageDetectionWindow
from dataAccess import DataAccess
import os

class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__() 
        self.initUI()

        self.newWindow = None

    def initUI(self):
        selfcss = """
            background-color: #010a1c;
            color: #ac0e28;
            font-size: 75px;
        """
        smallLabel = """
            font-size: 25px;
        """
        self.setStyleSheet(selfcss)
        self.setObjectName("MainWindow")
        self.setWindowTitle("Mimir - YOLOv5 Object Detection program")
        self.resize(500, 400)
        self.setMinimumSize(QtCore.QSize(500, 400))
        self.setMaximumSize(QtCore.QSize(500, 400))
        self.rootWidget = QtWidgets.QWidget(self)
        self.rootWidget.setObjectName("rootWidget")
        self.dataAccess = DataAccess()
        self.setWindowIcon(QtGui.QIcon(os.path.join(self.dataAccess.rootPath, 'mimir.ico')))

        self.verticalLayoutWidget = QtWidgets.QWidget(self.rootWidget)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(30, 30, 441, 341))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName("verticalLayout")

        self.applicationNameLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.applicationNameLabel.setText("Mimir")
        self.applicationNameLabel.setObjectName("applicationNameLabel")
        self.applicationNameLabel.setTextFormat(QtCore.Qt.AutoText)
        self.applicationNameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.applicationNameLabel.adjustSize()

        self.verticalLayout.addWidget(self.applicationNameLabel)

        self.applicationSubtitleLabel = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.applicationSubtitleLabel.setText("YOLOv5 Object detection program")
        self.applicationSubtitleLabel.setObjectName("applicationSubtitleLabel")
        self.applicationSubtitleLabel.setStyleSheet(smallLabel)
        self.applicationSubtitleLabel.setTextFormat(QtCore.Qt.AutoText)
        self.applicationSubtitleLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.applicationSubtitleLabel.adjustSize()

        self.verticalLayout.addWidget(self.applicationSubtitleLabel)

        self.imageDetectionButton = ActionButton(self.verticalLayoutWidget)
        self.imageDetectionButton.setText("Image Detection")      
        self.imageDetectionButton.setObjectName("imageDetectionButton")
        self.imageDetectionButton.setMinimumSize(QtCore.QSize(0, 50))
        self.imageDetectionButton.setMaximumSize(QtCore.QSize(16777215, 50))
        self.imageDetectionButton.clicked.connect(self.imageDetection)

        self.verticalLayout.addWidget(self.imageDetectionButton)

        self.videoDetectionButton = ActionButton(self.verticalLayoutWidget)
        self.videoDetectionButton.setText("Live Object Detection")      
        self.videoDetectionButton.setObjectName("videoDetectionButton")
        self.videoDetectionButton.setMinimumSize(QtCore.QSize(0, 50))
        self.videoDetectionButton.setMaximumSize(QtCore.QSize(16777215, 50))
        self.videoDetectionButton.clicked.connect(self.vodeoDetection)

        self.verticalLayout.addWidget(self.videoDetectionButton)

        self.setCentralWidget(self.rootWidget)
    
    def vodeoDetection(self):
        self.mimirCore = MimirCore()
        self.mimirCore.VideoRecognition()

    def imageDetection(self):
        self.imageDetectionWindow = ImageDetectionWindow()
        self.imageDetectionWindow.show()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    ui = MainWindow()
    ui.show()
    sys.exit(app.exec_())