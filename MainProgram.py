# -*- coding: utf-8 -*-
"""
Created on Sun Jul 29 10:52:02 2018

@author: xuanm
"""
from PyQt5 import QtCore,QtWidgets,QtGui
from PyQt5.QtWidgets import QApplication, QWidget, QLabel, QFileDialog, QGraphicsRectItem, QGraphicsScene, QMessageBox, QMainWindow
import cv2
import sys
import MainWindow
import VideoDialog
import time
import serial

class MainProgram(QWidget):
    def __init__(self): 
        app = 0
        app = QtWidgets.QApplication(sys.argv)
        super().__init__()
        MainProgram = QMainWindow()
        self.ui = MainWindow.Ui_MainWindow()
        self.ui.setupUi(MainProgram)
        
        self.camera1_flag = 0
        self.camera2_flag = 0
        self.savepath = ""
        self.filename_camera1 = ""
        self.filename_camera2 = ""
        self.timer_serial = QtCore.QTimer()
        self.action_connect()
        MainProgram.show()
        sys.exit(app.exec_())
        
    def action_connect(self):
        self.ui.Button_camera1.clicked.connect(self.Button_camera1_clicked) 
        self.ui.Button_camera2.clicked.connect(self.Button_camera2_clicked)
        self.ui.Button_filename.clicked.connect(self.Button_filename_clicked)
        self.ui.Button_savepath.clicked.connect(self.Button_savepath_clicked)
        self.ui.Button_recording.clicked.connect(self.Button_recording_clicked)
        self.ui.Button_endrecording.clicked.connect(self.Button_endrecording_clicked)
        self.ui.Button_trigger.clicked.connect(self.Button_trigger_clicked)
        self.ui.Button_canceltrigger.clicked.connect(self.Button_canceltrigger_clicked)
        self.timer_serial.timeout.connect(self.serial_timer_trigger)

    def Button_camera1_clicked(self):
        if self.camera1_flag == 0:
            self.cap1 = cv2.VideoCapture(0)
            if self.cap1.isOpened() == True:
                self.sub_ui1 = VideoDialog.Ui_VideoDialog()
                self.Dialog1 = QtWidgets.QDialog()
                
                self.sub_ui1.setupUi(self.Dialog1, 0, self.cap1)
                
                self.Dialog1.show()
                self.camera1_flag = 1
                self.Dialog1.exec_()
                if self.sub_ui1.cap.isOpened():
                   self.sub_ui1.cap.release()
                if self.sub_ui1.timer_camera.isActive():
                   self.sub_ui1.timer_camera.stop()
                   self.camera1_flag = 0
            else:
                self.cap1.release()
                QMessageBox.information(self, "Info", "Camera 1 is Null", QMessageBox.Yes | QMessageBox.No)

    def Button_camera2_clicked(self):
        if self.camera2_flag == 0:
            self.cap2 = cv2.VideoCapture(1)
            if self.cap2.isOpened() == True:
                self.sub_ui2 = VideoDialog.Ui_VideoDialog()
                self.Dialog2 = QtWidgets.QDialog()
                
                self.sub_ui2.setupUi(self.Dialog2, 1, self.cap2)
                
                self.Dialog2.show()
                self.camera2_flag = 1
                self.Dialog2.exec_()
                if self.sub_ui2.cap.isOpened():
                   self.sub_ui2.cap.release()
                if self.sub_ui2.timer_camera.isActive():
                   self.sub_ui2.timer_camera.stop()
                   self.camera2_flag = 0
            else:
                self.cap2.release()
                QMessageBox.information(self, "Info", "Camera 2 is Null", QMessageBox.Yes | QMessageBox.No)
        
    def Button_filename_clicked(self):
        base_filename = self.ui.Edit_filename.text()
        if base_filename == "":
           base_filename = "Video"
        self.filename_camera1 = ''.join((base_filename, "_camera1_"))
        self.filename_camera2 = ''.join((base_filename, "_camera2_"))
        print(self.filename_camera1)

    def Button_savepath_clicked(self):
        self.savepath = QFileDialog.getExistingDirectory(self, "Choose the path", './')
        self.savepath = ''.join((self.savepath, "/"))
        self.ui.Label_savepath.setText(self.savepath)
        self.filename_camera1 = ''.join((self.savepath, self.filename_camera1))
        self.filename_camera2 = ''.join((self.savepath, self.filename_camera2))

    def Button_recording_clicked(self):
        if self.filename_camera1 == "":
           self.filename_camera1 = ''.join(("Video", "_camera1_"))
        if self.filename_camera2 == "":
           self.filename_camera2 = ''.join(("Video", "_camera2_"))
        if self.savepath == "":
           self.savepath = "C:/"
           self.filename_camera1 = ''.join((self.savepath, self.filename_camera1))
           self.filename_camera2 = ''.join((self.savepath, self.filename_camera2))
        t=list(time.localtime()[3:7])
        t_str = [str(i) for i in t]
        t_str = ''.join(t_str)
        if hasattr(self, 'sub_ui1'):
           savename_camera1 = ''.join((self.filename_camera1, t_str, '.avi'))
           fourcc = cv2.VideoWriter_fourcc(*'XVID')
           self.sub_ui1.out = cv2.VideoWriter(savename_camera1,fourcc, 30.0, (640,480))
           self.sub_ui1.record_flag = 1
           self.ui.Label_mrecordingtime.setText("Recording")
           print(time.clock())
        if hasattr(self, 'sub_ui2'):
           savename_camera2 = ''.join((self.filename_camera2, t_str, '.avi'))
           fourcc = cv2.VideoWriter_fourcc(*'XVID')
           self.sub_ui2.out = cv2.VideoWriter(savename_camera2,fourcc, 30.0, (640,480))
           self.sub_ui2.record_flag = 1
        self.ui.Button_recording.setEnabled(False)
        print(self.filename_camera1)
        print(savename_camera1)
           
    def Button_endrecording_clicked(self):
        self.ui.Label_mrecordingtime.setText("")
        if hasattr(self, 'sub_ui1'):
           if self.sub_ui1.record_flag == 1:
              self.sub_ui1.record_flag = 0
              self.sub_ui1.out.release()
              print(time.clock())
        if hasattr(self, 'sub_ui2'):
           if self.sub_ui2.record_flag == 1:
              self.sub_ui2.record_flag = 0
              self.sub_ui2.out.release()
        self.ui.Button_recording.setEnabled(True)
        
    def Button_trigger_clicked(self):
        if self.filename_camera1 == "":
           self.filename_camera1 = ''.join(("Video", "_camera1_"))
        if self.filename_camera2 == "":
           self.filename_camera2 = ''.join(("Video", "_camera2_"))
        if self.savepath == "":
           self.savepath = "C:/"
           self.filename_camera1 = ''.join((self.savepath, self.filename_camera1))
           self.filename_camera2 = ''.join((self.savepath, self.filename_camera2))
        try:
           self.my_serial = serial.Serial('COM3', 9600, timeout=0.5)
        except:
           print('e')
        else:
           print("Waiting for triggering signal")
           self.timer_serial.start(5)
           self.ui.Button_trigger.setEnabled(False)
           
    def serial_timer_trigger(self):
        data = self.my_serial.read_all()
        if data != b'' :
           if data == b"STR":
              t=list(time.localtime()[3:7])
              t_str = [str(i) for i in t]
              t_str = ''.join(t_str)
              if hasattr(self, 'sub_ui1'):
                 savename_camera1 = ''.join((self.filename_camera1, t_str, '.avi'))
                 fourcc = cv2.VideoWriter_fourcc(*'XVID')
                 self.sub_ui1.out = cv2.VideoWriter(savename_camera1,fourcc, 30.0, (640,480))
                 self.sub_ui1.record_flag = 1
                 self.ui.Label_trecordingtime.setText("Recording")
                 print(time.clock())
              if hasattr(self, 'sub_ui2'):
                 savename_camera2 = ''.join((self.filename_camera2, t_str, '.avi'))
                 fourcc = cv2.VideoWriter_fourcc(*'XVID')
                 self.sub_ui2.out = cv2.VideoWriter(savename_camera2,fourcc, 30.0, (640,480))
                 self.sub_ui2.record_flag = 1
                 self.ui.Label_trecordingtime.setText("Recording")
              print("receive : ",data)
           if data == b"END":
              if hasattr(self, 'sub_ui1'):
                 if self.sub_ui1.record_flag == 1:
                    self.sub_ui1.record_flag = 0
                    self.sub_ui1.out.release()
                    print(time.clock())
                 self.ui.Label_trecordingtime.setText("")
              if hasattr(self, 'sub_ui2'):
                 if self.sub_ui2.record_flag == 1:
                    self.sub_ui2.record_flag = 0
                    self.sub_ui2.out.release()
                 self.ui.Label_trecordingtime.setText("")
              print("receive : ",data)
              print("***********Recording End***********")
        
    def Button_canceltrigger_clicked(self):
        if hasattr(self, 'my_serial'):
           if self.my_serial.isOpen():
              self.timer_serial.stop()
              self.my_serial.close()
              self.ui.Button_trigger.setEnabled(True)
              print("***********The serial port is closed*****************")

if __name__ == "__main__":
    MainProgram()