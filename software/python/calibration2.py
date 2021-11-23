import cv2
import numpy as np


CHESS_G_SIZE=25
DEBUG = False
def __find_chess_coordinate(image,size):
    
    # This function returns the coordinates of chess corners
    # input : image of chess, size of chessboard
    # *** it is considered that size of each square is 2cm * 2cm
    
    coordinates = []
    gray_image  = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gray_image = clahe.apply(gray_image)

    if DEBUG:
        cv2.imshow('gray_calhe',cv2.resize(gray_image, None, fx=0.5,fy=0.5))
        cv2.waitKey(0)
    corners     = cv2.findChessboardCorners(gray_image,(size[0]-1,size[1]-1))
    if corners[0] == False:
        raise Exception ('The chessboard is not found')
    else:
        corners = corners[1].reshape([-1,2])
#         corners = corners[1].reshape(-1,2)
#         max_x   = np.argmax(corners[:,0],axis=0)
#         max_y   = np.argmax(corners[:,1],axis=0)
#         min_x   = np.argmin(corners[:,0],axis=0)
#         min_y   = np.argmin(corners[:,1],axis=0)
 
#         coordinates.append(corners[min_y].reshape(1,-1))
#         coordinates.append(corners[max_x].reshape(1,-1))
#         coordinates.append(corners[min_x].reshape(1,-1))
#         coordinates.append(corners[max_y].reshape(1,-1))

        first  = corners[0]
        second = corners[size[0]-2]
        third  = (corners[((size[0]-1)*(size[1]-1))-(size[0]-1)])
        fourth = corners[(size[0]-1)*(size[1]-1)-1]
            
        coordinates = np.array([first,third,second,fourth])

        if DEBUG:
            for pt in coordinates:
                cv2.circle(image, tuple(pt.astype(np.int32)), 10, (255,0,0), thickness=-1)
                cv2.imshow('image',cv2.resize(image,None, fx=0.5, fy=0.5))
                cv2.waitKey(0)
        
        return coordinates
 


def fit(image,chess_size=(8,12)):
    
    #This function returns the transformation matrix and scale coefficient
    #input: image of chessboard, chessboard size, orientation of the plate('h' or 'v')
    chess_size = np.array(chess_size).reshape((2,)).astype(np.int32)
    image = np.array(image,dtype=np.uint8)
    channel,h,w = image.shape
    #image = np.reshape(image,(h,w,channel))
    image = np.moveaxis(image,[0,1,2],[2,0,1])
    #cv2.imshow('imageee',image)
    
#     print(image.shape)
    
    
    
    chess_size = list(chess_size)
    minimum = min(chess_size)
    maximum = max(chess_size)
    chess_size[0] = minimum
    chess_size[1] = maximum
    
    points = __find_chess_coordinate(image,chess_size)
    realWorld_size = [(chess_size[0]-2)*CHESS_G_SIZE * (chess_size[1]-2)*CHESS_G_SIZE]
    w1  = __oqlidus_distance(points[0],points[1])
    h1 = __oqlidus_distance(points[1],points[3])
    w2  = __oqlidus_distance(points[3],points[2])
    h2 = __oqlidus_distance(points[2],points[0])

    h_px = (h1 + h2)/2
    w_px = (w1 + w2)/2

    area_px = h_px * w_px
    px_size = (realWorld_size/ area_px)**0.5
        
    res = np.zeros((4,3), np.float32)
    res[3,:] = px_size
    return res

        
def __point_prediction(transformer_mat,coef,points):
    points = np.array(points).T
    ones   = np.array([1]*points.shape[1]).reshape([-1,1]).T
    points = np.concatenate([points, ones], 0)
    points = (transformer_mat @ points).T
    points = np.diag(1/(points[:,2].reshape(-1))) @ points[:,:2]
    dists  = __calc_dist(points,coef)
    return dists

def predict(transformer_mat,coef,circles,mode='mean'):
    
    # This function predicts real distance
    # Inputs: transformation matrix, scaling coefficient, matrix of circles(n*3 --> x,y,center),
    #         mode('mean','max','min') 

    result = np.copy( circles[:,-1] )
    result = result * coef* 2
    return result
        
    
def __calc_dist(points,coeficient):
    
    # This function is for calculating the oqlidusian distance with consideration of scaling coefficient
    # Input: bach of points(n*2), scaling coefficient
    
    points = points.reshape([-1,2,2])
    return np.sqrt(np.sum((points[:,0]-points[:,1])**2,1))/coeficient

 
def __oqlidus_distance(p1,p2):
    
    #This function is for computing simple oqlidus distance WITHOUT considering scaling coefficient
    dis = np.sqrt(np.sum((p1-p2)**2))                       
    return dis






img = cv2.imread('29_calib.jpg')
img = np.moveaxis(img,[0,1,2],[1,2,0])
a = fit(img)

