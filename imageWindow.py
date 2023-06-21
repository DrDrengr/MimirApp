from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from mimir import MimirCore
from labels import ImageLabel
from buttons import ImageSwitchButton
from dataAccess import DataAccess
import os

class ImageDetectionWindow(QMainWindow):
    def __init__(self):
        super(ImageDetectionWindow, self).__init__() 
        self.customWidth = 1455
        self.customHeight = 880
        self.imageMaxHeight = 720
        self.initUI()
        self.setAcceptDrops(True)
        self.mimirCore = MimirCore()
        self.detectionImages = []
        self.displayedDetectionImageIndex = -1

    def initUI(self):
        selfcss = """
            font-size: 40px;
            background-color: #010a1c;
            color: #ac0e28;
        """
        smallLabel = """
            font-size: 15px;
        """
        self.setStyleSheet(selfcss)
        self.setObjectName("imageDetectionWindow")
        self.setWindowTitle("Mimir - Image Detection")
        self.setMinimumSize(QtCore.QSize(self.customWidth, self.customHeight))
        self.setMaximumSize(QtCore.QSize(self.customWidth, self.customHeight))
        self.rootWidget = QtWidgets.QWidget(self)
        self.rootWidget.setObjectName("rootWidget")
        self.dataAccess = DataAccess()
        self.setWindowIcon(QtGui.QIcon(os.path.join(self.dataAccess.rootPath, 'mimir.ico')))

        self.horizontalLayoutWidget = QtWidgets.QWidget(self.rootWidget)
        self.horizontalLayoutWidget.setGeometry(QtCore.QRect(10, 0, self.customWidth, self.customHeight))
        self.horizontalLayoutWidget.setObjectName("horizontalLayoutWidget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.horizontalLayoutWidget)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        self.horizontalLayout.setContentsMargins(10, 10, 10, 10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        
        self.previous = ImageSwitchButton(self.horizontalLayoutWidget, False)
        self.previous.setMinimumSize(QtCore.QSize(60, 60))
        self.previous.setMaximumSize(QtCore.QSize(60, 60))
        self.previous.setObjectName("previous")
        self.previous.setText("<")
        self.previous.clicked.connect(self.switchImageLeft)
        self.horizontalLayout.addWidget(self.previous)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSizeConstraint(QtWidgets.QLayout.SetMinAndMaxSize)
        
        self.verticalLayout.setSpacing(15)
        self.verticalLayout.setObjectName("verticalLayout")

        self.applicationNameLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)
        self.applicationNameLabel.setText("Immage Detection")
        self.applicationNameLabel.setObjectName("applicationNameLabel")
        self.applicationNameLabel.setTextFormat(QtCore.Qt.AutoText)
        self.applicationNameLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.applicationNameLabel.adjustSize()
        self.verticalLayout.addWidget(self.applicationNameLabel)

        self.infoLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)  
        self.infoLabel.setObjectName("infoLabel")
        self.infoLabel.setText("You can drop new images over the current ones.")
        self.infoLabel.setStyleSheet(smallLabel)
        self.infoLabel.setTextFormat(QtCore.Qt.AutoText)
        self.infoLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.infoLabel.adjustSize()

        self.verticalLayout.addWidget(self.infoLabel)


        self.dropdownBox = ImageLabel(self.horizontalLayoutWidget)
        self.verticalLayout.addWidget(self.dropdownBox)

        self.counterLabel = QtWidgets.QLabel(self.horizontalLayoutWidget)  
        self.counterLabel.setObjectName("counterLabel")
        self.counterLabel.setStyleSheet(smallLabel)
        self.counterLabel.setTextFormat(QtCore.Qt.AutoText)
        self.counterLabel.setAlignment(QtCore.Qt.AlignCenter)
        self.counterLabel.adjustSize()

        self.verticalLayout.addWidget(self.counterLabel)

        self.horizontalLayout.addLayout(self.verticalLayout)

        self.next = ImageSwitchButton(self.horizontalLayoutWidget, False)
        self.next.setMinimumSize(QtCore.QSize(60, 60))
        self.next.setMaximumSize(QtCore.QSize(60, 60))
        self.next.setObjectName("next")
        self.next.setText(">")
        self.next.clicked.connect(self.switchImageRight)
        self.horizontalLayout.addWidget(self.next)

        self.setCentralWidget(self.rootWidget)
        self.disableButtons()

    def handleDetections(self, filePaths):
        self.disableButtons()
        self.detectionImages = self.mimirCore.PhotoRecognition(filePaths)
        if len(self.detectionImages) > 0:
            self.setImage(self.detectionImages[0])
            self.displayedDetectionImageIndex = 0
            
            self.updateCounter()
            if len(self.detectionImages) > 1:
                self.manageButtons()

    def dragEnterEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()
    
    def dragMoveEvent(self, event):
        if event.mimeData().hasImage:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasImage:
            event.setDropAction(Qt.CopyAction)

            filePaths = []
            for url in event.mimeData().urls():
                filePaths.append(url.toLocalFile())

            self.handleDetections(filePaths)
            event.accept()
        else:
            event.ignore()

    def setImage(self, file_path):
        image = QPixmap(file_path).scaledToHeight(self.imageMaxHeight)
        self.dropdownBox.setPixmap(image)

    def switchImageRight(self):
        if len(self.detectionImages)> 0 and self.displayedDetectionImageIndex + 1 <= len(self.detectionImages) - 1:
            self.displayedDetectionImageIndex += 1
            self.setImage(self.detectionImages[self.displayedDetectionImageIndex])

            self.updateCounter()
        self.manageButtons()

    def switchImageLeft(self):
        if len(self.detectionImages) > 0 and self.displayedDetectionImageIndex - 1 >= 0:
            self.displayedDetectionImageIndex -= 1
            self.setImage(self.detectionImages[self.displayedDetectionImageIndex])

            self.updateCounter()
        self.manageButtons()

    def manageButtons(self):
        if len(self.detectionImages)> 0 and self.displayedDetectionImageIndex + 1 <= len(self.detectionImages) - 1:
            self.next.setEnabledLook()
            self.next.setEnabled(True)
        else:
            self.next.setDisabledLook()
            self.next.setEnabled(False)

        if len(self.detectionImages) > 0 and self.displayedDetectionImageIndex - 1 >= 0:
            self.previous.setEnabledLook()
            self.previous.setEnabled(True)
        else:
            self.previous.setDisabledLook()
            self.previous.setEnabled(False)

    def disableButtons(self):
        self.infoLabel.hide()
        self.counterLabel.hide() 
        self.next.setDisabledLook()
        self.next.setEnabled(False)
        self.previous.setDisabledLook()
        self.previous.setEnabled(False)
    
    def updateCounter(self):
        self.counterLabel.show()
        self.infoLabel.show()
        self.counterLabel.setText(str(self.displayedDetectionImageIndex + 1) + " of " + str(len(self.detectionImages)))