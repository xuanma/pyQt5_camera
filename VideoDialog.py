# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'VideoDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets
import cv2

class Ui_VideoDialog(QtWidgets.QWidget):
    def setupUi(self, VideoDialog, No_camera, cap):
        super().__init__() 
        VideoDialog.setObjectName("VideoDialog")
        self.Lable_video = QtWidgets.QLabel(VideoDialog)
        self.Lable_video.setGeometry(QtCore.QRect(0, 0, 650, 490))
        self.Lable_video.setText("")
        self.Lable_video.setObjectName("Lable_video")
        
        self.timer_camera = QtCore.QTimer()
        self.cap = cap
        self.record_flag = 0
        
        self.open_camera(No_camera)

        self.retranslateUi(VideoDialog)
        QtCore.QMetaObject.connectSlotsByName(VideoDialog)

    def retranslateUi(self, VideoDialog):
        _translate = QtCore.QCoreApplication.translate
        VideoDialog.setWindowTitle(_translate("VideoDialog", "Camera"))
        VideoDialog.setWindowIcon(QtGui.QIcon("camera.png"))
        VideoDialog.setWindowFlags(VideoDialog.windowFlags()|
                                   QtCore.Qt.WindowMinimizeButtonHint|
                                   QtCore.Qt.WindowSystemMenuHint)
        self.timer_camera.timeout.connect(self.show_camera)

    def open_camera(self, No_camera):
        if self.timer_camera.isActive() == False:
            flag = self.cap.open(No_camera)
            if flag == False:
               QtWidgets.QMessageBox.warning(self, u"Warning", u"No Camera is detected", buttons=QtWidgets.QMessageBox.Ok, defaultButton=QtWidgets.QMessageBox.Ok)
            else:
                self.timer_camera.start(30)


# Timer function
    def show_camera(self):
        flag, self.image = self.cap.read()
        #cv2.putText(self.image,'OpenCV',(10,10), cv2.FONT_HERSHEY_PLAIN, 2,(255,255,255),1,cv2.LINE_AA)
        show = cv2.resize(self.image, (640, 480))
        show = cv2.cvtColor(show, cv2.COLOR_BGR2RGB)
        showImage = QtGui.QImage(show.data, show.shape[1], show.shape[0], QtGui.QImage.Format_RGB888)
        self.Lable_video.setPixmap(QtGui.QPixmap.fromImage(showImage))
        
        if self.record_flag == 1:
           self.out.write(self.image)