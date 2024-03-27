#this code will contain a path to a .npy file(Lidar Scan) which will not be uploaded to github since it is confidential data of valeo.
import numpy as np
import open3d as o3d
from numpy import load

errorIntrinsics = [[0.00, 0.00, 0.00] , [0.00, 0.00, 0.00], [0.00, 0.00, 0.00]]

#lidar configureation area
path = "./../valeoData-CONFIDENTIAL/everything/Veh01_20230208_105703_076_PCD.npz"
frame_index = 0


data = load(path)
scan = data["scan_list"]
#TODO:load the scan as a geometry o3d.visualization.draw_geometries()




def pinholeGetMatrix(fx, fy, ppx, ppy):
    return [[fx, 0, ppx],[0, fy, ppy],[0, 0, 1]]

list_of_matrices = []

#this portion shall be used if and only if DroidCalibResults2.txt (of pinholeCameraModel) is tested
# config
camera_index = 0
# endconfig
list_of_matrices.append(pinholeGetMatrix(fx = 5558.10, fy = 5052.64, ppx = 1502.62, ppy = 905.80))
list_of_matrices.append(pinholeGetMatrix(1732.79, fy = 1616.02, ppx = 1142.51, ppy = 594.05))
list_of_matrices.append(pinholeGetMatrix(fx = 1597.80, fy = 1492.63, ppx = 1148.71, ppy = 604.39))
list_of_matrices.append(pinholeGetMatrix(fx = 1927.28, fy = 1489.00, ppx = 955.80, ppy = 643.10))
list_of_matrices.append(pinholeGetMatrix(fx = 2039.97, fy = 1153.31, ppx = 890.80, ppy = 571.74))
list_of_matrices.append(pinholeGetMatrix(fx = 2532.59, fy = 2216.88, ppx = 1547.08, ppy = 1000.33))
list_of_matrices.append(pinholeGetMatrix(fx = 4738.09, fy = 2033.31, ppx = 867.75, ppy = 1217.82))
cam = o3d.camera.PinholeCameraIntrinsic()
cam.intrinsic_matrix =  list_of_matrices[camera_index]

