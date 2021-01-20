#Robot Parameter입력하는 GUI
import sys
import numpy as np
import math
from PyQt5.QtWidgets import *
from PyQt5 import uic
from PyQt5.QtCore import QCoreApplication
import pyrealsense2 as rs
import Robot_Matrix as RoM
import cv2
import time
global X
global Y
global Z
global RX
global RY
global RZ
    
def Calibration_Input():
    #UI파일 연결
    #단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
    form_class = uic.loadUiType("Calibration_Input.ui")[0]

    #화면을 띄우는데 사용되는 Class 선언
    class WindowClass(QMainWindow, form_class) :
        def __init__(self) :
            global X
            global Y
            global Z
            global RX
            global RY
            global RZ
            global B
            global color_image
            
            super().__init__()
            self.setupUi(self)

            self.Send.clicked.connect(self.send)
            self.Camera.clicked.connect(self.Realsense)

            self.Send.clicked.connect(QCoreApplication.instance().quit)

        def send(self, text):
            i = time.time()

            global X
            global Y
            global Z
            global RX
            global RY
            global RZ
            global B
            global color_image

            X = float(self.lineEdit.text())
            Y = float(self.lineEdit_2.text())
            Z = float(self.lineEdit_3.text())
            RX = float(self.lineEdit_4.text())
            RY = float(self.lineEdit_5.text())
            RZ = float(self.lineEdit_6.text())

            if self.Degree.isChecked():
                RX = RX
                RY = RY
                RZ = RZ

            else:
                RX = math.degrees(RX)
                RY = math.degrees(RY)
                RZ = math.degrees(RZ)
                
            B = RoM.robot_Mat(X, Y, Z, RX, RY, RZ)
            
            cv2.imwrite('./calibration_data/{0}.jpg'.format(i), color_image)
            np.save('./calibration_data/{0}'.format(i), B)
            
            return
             
        def Realsense(self):
            #Realsense
            global color_image
            
            pipeline = rs.pipeline()    # 이미지 가져옴
            config = rs.config()        # 설정 파일 생성
            config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)  #크기 , 포맷, 프레임 설정
            config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

            profile = pipeline.start(config)   #설정을 적용하여 이미지 취득 시작, 프로파일 얻음

            depth_sensor = profile.get_device().first_depth_sensor()    # 깊이 센서를 얻음
            depth_scale = depth_sensor.get_depth_scale()                # 깊이 센서의 깊이 스케일 얻음
            #print("Depth Scale is: ", depth_scale)

            clipping_distance_in_meters = 1    # 1 meter, 클리핑할 영역을 1m로 설정
            clipping_distance = clipping_distance_in_meters / depth_scale   #스케일에 따른 클리핑 거리

            align_to = rs.stream.color      #depth 이미지를 맞추기 위한 이미지, 컬러 이미지
            align = rs.align(align_to)      #depth 이미지와 맞추기 위해 align 생성

        #try:
            while True:
                frames = pipeline.wait_for_frames() #color와 depth의 프레임셋을 기다림
                #frames.get_depth_frame() 은 640x360 depth 이미지이다.

                aligned_frames= align.process(frames)   #모든(depth 포함) 프레임을 컬러 프레임에 맞추어 반환

                aligned_depth_frame = aligned_frames.get_depth_frame()  #  aligned depth 프레임은 640x480 의 depth 이미지이다
                color_frame = aligned_frames.get_color_frame()      #컬러 프레임을 얻음

                if not aligned_depth_frame or not color_frame:      #프레임이 없으면, 건너 뜀
                    continue

                depth_image = np.asanyarray(aligned_depth_frame.get_data())     #depth이미지를 배열로, 
                color_image = np.asanyarray(color_frame.get_data())             #color 이미지를 배열로
                
                #글자 표시
                color = (0, 255, 255)
                thickness = 2
                location = (250, 30)
                font = cv2.FONT_HERSHEY_COMPLEX
                fontScale = 1.0
                
                cv2.putText(color_image, 'q : Quit', location, font, fontScale, color, thickness)

                cv2.namedWindow('Align Example', cv2.WINDOW_AUTOSIZE)   #이미지 윈도우 정의
                cv2.imshow('Align Example', color_image)         #이미지를 넣어 윈도우에 보임

                key = cv2.waitKey(1)
                #if key & 0xFF == ord('s'):
                #   cv2.imwrite('./calibration_data/{0}.jpg'.format(i), color_image)
                #   cv2.destroyAllWindows()
                #q를 누르면, 나간다.
                if key & 0xFF == ord('q') or key == 27:
                #윈도우 제거
                    cv2.destroyAllWindows()
                    break
                    
       #finally:
            #pipeline.stop()
        
    #if __name__ == "__main__" :
    #QApplication : 프로그램을 실행시켜주는 클래스
    app = QApplication(sys.argv) 

    #WindowClass의 인스턴스 생성
    myWindow = WindowClass() 

    #프로그램 화면을 보여주는 코드
    myWindow.show()

    #프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
    
    return 

if __name__ == "__main__" :
    Calibration_Input()