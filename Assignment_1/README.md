# This Assignment is related to Camera caliberation #

The images directory contains images of a chessboard that were used for calibrating a camera
with high radial distortion. The results of the calibration (intrinsics of the camera and extrinsics
for each board) are stored in data/ex1.mat. You are asked to

Markup : 1. Write a function project_points for projecting all 3D-points defined by a chessboard
              (in the world coordinate system) to the 2D pixel coordinate system. It should optionally
              regard the radial distortion (k1, k2, k5). The function takes as input a vector of 3D
              world points, the camera’s intrinsic and extrinsic parameters and a flag for considering the
              distortion. It returns the projected 2D-points.
