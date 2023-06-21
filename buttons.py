from PyQt5 import QtWidgets, QtCore, QtGui
from player import Player

class ActionButton(QtWidgets.QPushButton):
    def __init__(self, parent=None, soundEnabled = True):
        super().__init__(parent)
        self.soundEnabled = soundEnabled
        self.setMinimumSize(60, 60)

        self.color1 = QtGui.QColor(172, 14, 40)
        self.color2 = QtGui.QColor(73, 0, 9)

        self._animation = QtCore.QVariantAnimation(
            self,
            valueChanged=self._animate,
            startValue=0.00001,
            endValue=0.9999,
            duration=250
        )

        self.player = Player()

    def _animate(self, value):
        qss = """
            font: 75 10pt "Microsoft YaHei UI";
            font-weight: bold;
            color: rgb(255, 255, 255);
            border-style: solid;
        """
        grad = "background-color: qlineargradient(spread:pad, x1:0, y1:0, x2:1, y2:0, stop:0 {color1}, stop:{value} {color2}, stop: 1.0 {color1});".format(
            color1=self.color1.name(), color2=self.color2.name(), value=value
        )
        qss += grad
        self.setStyleSheet(qss)

    def enterEvent(self, event):
        if self.soundEnabled == True:
            self.player.playMenuSound()
        self._animation.setDirection(QtCore.QAbstractAnimation.Forward)
        self._animation.start()
        super().enterEvent(event)

    def leaveEvent(self, event):
        self._animation.setDirection(QtCore.QAbstractAnimation.Backward)
        self._animation.start()
        super().leaveEvent(event)


class ImageSwitchButton(QtWidgets.QPushButton):
    def __init__(self, parent=None, soundEnabled = True):
        super().__init__(parent)
        self.soundEnabled = soundEnabled
        self.setMinimumSize(60, 60)

        self.player = Player()

        self.defaultStyle = """
            font-size: 80px;
            color: #ac0e28;
            background-color:transparent;  
        """

        self.hoverStyle = """
            font-size: 75px;
            color: #490009;
            background-color:transparent;  
        """

        self.disabledStyle = """
            font-size: 75px;
            color: #010a1c;
            background-color:transparent;  
        """

        self.setStyleSheet(self.disabledStyle)


    def enterEvent(self, event):
        if self.isEnabled() == True:
            self.setStyleSheet(self.hoverStyle)
            if self.soundEnabled == True:
                self.player.playMenuSound()
            super().enterEvent(event)

    def leaveEvent(self, event):
        if self.isEnabled() == True:
            self.setStyleSheet(self.defaultStyle)
            super().leaveEvent(event)

    def setDisabledLook(self):
        self.setStyleSheet(self.disabledStyle)
    
    def setEnabledLook(self):
        self.setStyleSheet(self.defaultStyle)