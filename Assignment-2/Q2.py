# @Author: Kaustav Vats 
# @Roll-Number: 2016048 

# In[]
from __future__ import division
import numpy as np
import cv2
import matplotlib.pyplot as plt

# In[]
criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)

Points_3d = np.zeros((6*7, 3), dtype=np.float32)
Points_3d[:, :2] = np.mgrid[0:7,0:6].T.reshape(-1, 2)

Points_3d_all = []
Points_2d_all = []

for i in range(1, 10):
    Image = cv2.imread("q2_img/Left"+str(i)+".bmp", 0)
    # print(Image.shape)
    ret, corners = cv2.findChessboardCorners(Image, (7, 6), None)
    if ret:
        Points_3d_all.append(Points_3d)
        cv2.cornerSubPix(Image, corners, (11, 11), (-1, -1), criteria)
        Points_2d_all.append(corners)

        cv2.drawChessboardCorners(Image, (7, 6), corners, ret)
        cv2.imwrite("q2_img/Corners_Left"+str(i)+".png", Image)
    # print(Image.shape[::-1])
print("----All Corners Detected----")

# In[]
# Calibrate Camera
# In[]
ret, cMatrix, dMatrix, rVector, tVector = cv2.calibrateCamera(Points_3d_all, Points_2d_all, (640, 480), None, None)

Image = cv2.imread("q2_img/Left2.bmp", 0)
heigth, width = Image.shape[:2]
NewCamMatrix, roi = cv2.getOptimalNewCameraMatrix(cMatrix, dMatrix, (width, heigth), 1, (width, heigth))

dMatrix = cv2.undistort(Image, cMatrix, dMatrix, None, NewCamMatrix)
x, y, w, h = roi
dMatrix = dMatrix[y:y+h, x:x+w]
cv2.imwrite('q2_img/cc_result.png',dMatrix)
print("----Camear Calibration done----")

# In[]
# Reprojection Error
# In[]
Total_error = 0
for i in range(len(Points_3d_all)):
    Img_points, _ = cv2.projectPoints(Points_3d_all[i], rVector[i], tVector[i], cMatrix, dMatrix)
    error = cv2.norm(Points_2d_all[i], Img_points, cv2.NORM_L2)/len(Img_points)
    Total_error += error

print("Error:", Total_error/len(Points_3d_all))
