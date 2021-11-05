import sys
from PyQt5.QtCore import pyqtSlot, Qt
from PyQt5.QtWidgets import QApplication, QLabel, QVBoxLayout, QWidget
from PyQt5.QtGui import QPixmap
from mimir import MimirCore

class ImageLabel(QLabel):
    def __init__(self):
        super().__init__()

        self.setAlignment(Qt.AlignCenter)
        self.setText('\n\n Drop Image Here! \n\n')
        self.setStyleSheet('''
            QLabel{
                border: 4 px dotted black;
            }
        ''')

    def setPixmap(self, image):
        super().setPixmap(image)


class Widget(QWidget):
    def __init__(self):
        super().__init__()
        self.resize(500, 500)
        self.setAcceptDrops(True)

        mainLayout = QVBoxLayout()
        self.photoViewer = ImageLabel()
        mainLayout.addWidget(self.photoViewer)
        self.mimirCore = MimirCore()

        self.setLayout(mainLayout)

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
            file_path = event.mimeData().urls()[0].toLocalFile()
            self.setImage(file_path)
            self.mimirCore.recognition(file_path)
            event.accept()
        else:
            event.ignore()
    
    def setImage(self, file_path):
        self.photoViewer.setPixmap(QPixmap(file_path))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = Widget()
    widget.show()
    sys.exit(app.exec_())
