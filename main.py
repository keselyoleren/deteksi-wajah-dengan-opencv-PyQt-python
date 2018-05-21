import cv2
import os
import sys
from os import path
import numpy as np
import subprocess
try:
    from PyQt5.QtCore import pyqtSlot
    from PyQt5 import QtCore
    from PyQt5.QtGui import *
    from PyQt5.QtCore import *
    from PyQt5.QtWidgets import *
    from PyQt5.uic import loadUi
    from PyQt5 import QtGui, uic
except ImportError:
    if sys.version_info.major >= 3:
        import sip
        sip.setapi('QVariant', 2)
    from PyQt4.QtGui import *
    from PyQt4.QtCore import *

class Detect(QMainWindow):
    face_cascade = cv2.CascadeClassifier(os.path.join('haarcascade_frontalface_alt.xml'))
    def __init__(self):
        super(Detect, self).__init__()
        loadUi(os.path.join('ui/main.ui'), self)
        self.image = None
        self.processedImage = None
        self.loadButton.clicked.connect(self.openFile)
        self.detectButton.clicked.connect(self.detectClicked)

    def detectClicked(self):
        gray = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY) if len(self.image.shape) >= 3 else self.image
        faces = self.face_cascade.detectMultiScale(gray,1.3,5)
        for (x,y,w,h) in faces:
            if self.chkFace.isChecked():
                cv2.rectangle(self.image, (x,y), (x+w, y+h),(255,0,0), 2 )
            else:
                self.image = self.image.copy()
            
            roy_gray = gray[y:y+h, x:x+w]
            roi_color = self.image[y:y+h, x:x+w]
        else:
            self.image[y:y+h, x:x+w] = self.image[y:y+h,  x:x+w].copy()

        self.displayImage(2)

    def openFile(self):
        frame, filter = QFileDialog.getOpenFileName(self, 'open FIle', "*.jpg")
        if frame :
            self.loadImage(frame)
        else:
            print("invalid Image")
    
    def loadImage(self, frame):
        self.image = cv2.imread(frame)
        self.displayImage(1)

    
    def displayImage(self, window = 1):
        height, width, channels = self.image.shape
        bytesPerLine = channels * width
        qImg = QImage(self.image.data, width, height, bytesPerLine, QtGui.QImage.Format_RGB888)
        pixmap01 = QPixmap.fromImage(qImg)
        pixmap_image = QPixmap(pixmap01)
        if window == 1:
            
            self.imgLabel.setPixmap(pixmap_image)
            self.imgLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.imgLabel.setScaledContents(True)
            self.imgLabel.setMinimumSize(1,1)

        if window == 2:

            self.detectLabel.setPixmap(pixmap_image)
            self.detectLabel.setAlignment(QtCore.Qt.AlignCenter)
            self.detectLabel.setScaledContents(True)
            self.detectLabel.setMinimumSize(1,1)
            



app = QApplication(sys.argv)
window = Detect()
window.setWindowTitle("detect Face")
window.setWindowIcon(QIcon(os.path.join('icons/logo.png')))
window.show()
sys.exit(app.exec_())
