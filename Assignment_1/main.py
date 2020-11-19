import os, sys
import numpy as np
import pandas as pd
import cv2 as cv
import scipy.io as io
import copy


base_folder = './data/'
data = io.loadmat('./data/ex_1_data.mat')

X_3D = data['x_3d_w'] # shape=[25, 40, 3]
TVecs = data['translation_vecs']
RMats = data['rot_mats']
dist_params = data['distortion_params']
Kintr = data['k_mat'] # shape 3,3


#2D Image coordinates
xy_ic = [] 

#Identity matrix for Kinter
I = np.array([[1,0,0,0],
            [0,1,0,0],
            [0,0,1,0]])

#Calibration matrix, shape = (3, 4)
KI= np.matmul(Kintr,I) 

folder='./Result/Distorted/'
folder_undis= './Result/Undistorted/'
#loop for 25 images
for i in range(TVecs.shape[0]):
    #Homogeneous Matrix RI
    RI= np.array([[RMats[i][0][0],RMats[i][0][1],RMats[i][0][2],TVecs[i][0][0]],
                   [RMats[i][1][0],RMats[i][1][1],RMats[i][1][2],TVecs[i][1][0]],
                   [RMats[i][2][0],RMats[i][2][1],RMats[i][2][2],TVecs[i][2][0]],
                   [0,0,0,1]])
    
    #To save 2D image coordinates
    img_ic=[] 

    #Extracting 2D image coordinates from 3D World cordinates with distortion
    for j in range(len(X_3D[i])):
        #3D World cordinates
        X=np.array([[X_3D[i][j][0]],
                    [X_3D[i][j][1]],
                    [X_3D[i][j][2]],
                    [1]])

        #Coordinate transformation
        R= np.matmul(RI,X)

        #Creating Perspective matrix by matrix multiplication of KI and R
        P= np.matmul(KI, R)

        #Extracting 2D image coordinates from Perspective matrix
        td_x = P[0][0]/P[2][0]
        td_y = P[1][0]/P[2][0]
        img_ic.append((td_x,td_y))
                
    #2D distorted points 
    xy_ic.append(img_ic)
    
    #2D undistorted points
    kinv = np.linalg.inv(Kintr) #For normalizing the points
    
    img = cv.imread(base_folder+str(i).zfill(5)+'.jpg')
    img2 = cv.cvtColor(img, cv.COLOR_BGR2RGB)
    img_copy = copy.deepcopy(img)
    image=img
    kinv = np.linalg.inv(Kintr) #For normalizing the points
        
    for k in range(len(xy_ic[i])):
        center_coordinates= (int(xy_ic[i][k][0]),int(xy_ic[i][k][1]))
        radius=1
        color= (0,0,255)
        thickeness=2
        image= cv.circle(image, center_coordinates, radius, color, thickeness)
        
        points_img = np.matrix(np.reshape((xy_ic[i][k][0],xy_ic[i][k][1],1), (3,-1)))
        norm_pt = kinv.dot(points_img)
        xn=norm_pt[0][0]
        yn=norm_pt[1][0] 
        r2= xn**2 + yn**2
        r4 = r2**2
        factor = (1 + (dist_params[0][0]*r2) + (dist_params[1][0]*(r4)) + (dist_params[4][0]*(r2*r4)))
        temp = np.ones((3,1))
        temp[0][0] = xn*factor
        temp[1][0] = yn*factor
        undistorted_CC= Kintr.dot(np.matrix(temp)) #np.matmul(Kintr, np.matrix(temp))
        undistorted_CC = (int(undistorted_CC[0][0]),int(undistorted_CC[1][0]))
        img_un= cv.circle(img_copy, undistorted_CC, radius, (0,255,0), thickeness)

    cv.imwrite(folder_undis+str(i).zfill(5)+'.jpg',img_un)
    cv.imwrite(folder+str(i).zfill(5)+'.jpg',image)
print('success')