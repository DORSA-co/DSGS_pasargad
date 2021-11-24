import cv2
import numpy as np


CHESS_G_SIZE=25
DEBUG = True
def __find_chess_coordinate(image,size):
    
    # This function returns the coordinates of chess corners
    # input : image of chess, size of chessboard
    # *** it is considered that size of each square is 2cm * 2cm
    
    coordinates = []
    gray_image  = cv2.cvtColor(image,cv2.COLOR_RGB2GRAY)

    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(8,8))
    gray_image = clahe.apply(gray_image)
    
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
        if DEBUG :
            for i in range(len(corners)):
                cv2.circle( image, tuple(corners[i]), 10, (0,0,255), thickness=-1)
                cv2.imshow('iimage', cv2.resize(image, None, fx=0.5, fy=0.5))
                print(corners[i])
                cv2.waitKey(0)
            
        coordinates = np.array([first,third,second,fourth])      
        return coordinates
 


def fit(image,chess_size=(8,12)):
    
    #This function returns the transformation matrix and scale coefficient
    #input: image of chessboard, chessboard size, orientation of the plate('h' or 'v')
    chess_size = np.array(chess_size).reshape((2,)).astype(np.int32)
    image = np.array(image,dtype=np.uint8)
    channel,h,w = image.shape
    #image = np.reshape(image,(h,w,channel))
    image = np.moveaxis(image,[0,1,2],[2,0,1])
    #image = cv2.imread('27_calib.jpg')
    
    
    chess_size = list(chess_size)
    minimum = min(chess_size)
    maximum = max(chess_size)
    chess_size[0] = minimum
    chess_size[1] = maximum

    points = __find_chess_coordinate(image,chess_size)

    realWorld_size = [(chess_size[0]-2)*CHESS_G_SIZE,(chess_size[1]-2)*CHESS_G_SIZE]
    print('realWorld_size',realWorld_size, chess_size)
    
    first_side  = __oqlidus_distance(points[0],points[1])
    second_side = __oqlidus_distance(points[1],points[3])
    third_side  = __oqlidus_distance(points[3],points[2])
    fourth_side = __oqlidus_distance(points[2],points[0])
    
    pts = np.copy( np.array([[points[0],points[1], points[3], points[2]]]) )
    pts = pts.reshape(-1,1,2).astype(np.int32)

    px_area = cv2.contourArea(pts)
    mm_area = ((chess_size[0]-2)*CHESS_G_SIZE)  *  ((chess_size[1]-2)*CHESS_G_SIZE)
    resultion_coef = np.sqrt(px_area/mm_area)
    if DEBUG:
        image = cv2.drawContours(image, [pts], 0, (255,0,0), thickness=3)
        cv2.imshow('rect', cv2.resize(image,None, fx=0.5, fy=0.5))
        print('px_area', px_area, '     mm_area:', mm_area)
        cv2.waitKey(0)
    
    offset = int(CHESS_G_SIZE*resultion_coef)
    source = np.float32(points)
#     if orientation == 'v':
#         destination = np.float32([[offset, offset], [realWorld_size[0]*resultion_coef+offset, offset], [offset, realWorld_size[1]*resultion_coef+offset],[realWorld_size[0]*resultion_coef+offset, realWorld_size[1]*resultion_coef+offset]])
#     elif orientation == 'h':
    destination = np.float32([[offset, offset], [realWorld_size[1]*resultion_coef+offset, offset], [offset, realWorld_size[0]*resultion_coef+offset],[realWorld_size[1]*resultion_coef+offset, realWorld_size[0]*resultion_coef+offset]])


    
   
    transformer_mat = cv2.getPerspectiveTransform(source,destination)

    if DEBUG :
        image = cv2.warpPerspective( image, transformer_mat, ( int(chess_size[1]*CHESS_G_SIZE * resultion_coef),
                                                               int(chess_size[0]*CHESS_G_SIZE * resultion_coef)))
        cv2.imshow('prs', cv2.resize(image,None, fx=0.5, fy=0.5))
        cv2.waitKey(0)                
    res = np.zeros((4,3), np.float32)
    res[:3,:] = transformer_mat
    res[3,:] = resultion_coef
    return res#transformer_mat.astype(np.float32)#,np.float32(resultion_coef)

        
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
    #return ( np.array(circles)[:,-1] / coef ).astype(np.float32)
    transformer_mat = np.array(transformer_mat).astype(np.float32)
    coef = np.float32(coef)
    circles = np.array(circles).astype(np.float32)
    
    first_point        = circles[:,:2].copy()
    second_point       = circles[:,:2].copy()
    centers            = circles[:,:2].copy()
    
    first_point[:,0]   = first_point[:,0]+circles[:,2]
    second_point[:,1]  = second_point[:,1]+circles[:,2]
    
    
    first_point  = np.concatenate([first_point,centers],axis=1).reshape(-1,2)
    second_point = np.concatenate([second_point,centers],axis=1).reshape(-1,2)

    
    first_distance  = __point_prediction(transformer_mat,coef,first_point).reshape(-1,1)
    second_distance = __point_prediction(transformer_mat,coef,second_point).reshape(-1,1)
    
    final_distance = np.concatenate([first_distance,second_distance],axis=1)
    
    if mode == 'mean':
        distance  = np.mean(final_distance,axis=1)
    elif mode == 'min':
        distance  = np.min(final_distance,axis=1)
    elif mode == 'max':
        distance  = np.max(final_distance,axis=1)
    else:
        raise Exception('The mode is not recognized')
        
    return distance.astype(np.float32)
        
    
def __calc_dist(points,coeficient):
    
    # This function is for calculating the oqlidusian distance with consideration of scaling coefficient
    # Input: bach of points(n*2), scaling coefficient
    
    points = points.reshape([-1,2,2])
    return np.sqrt(np.sum((points[:,0]-points[:,1])**2,1))/coeficient

 
def __oqlidus_distance(p1,p2):
    
    #This function is for computing simple oqlidus distance WITHOUT considering scaling coefficient
    dis = np.sqrt(np.sum((p1-p2)**2))                       
    return dis

'''
img_ = cv2.imread('27_calib.jpg')
img = np.moveaxis(img_,[0,1,2],[1,2,0])
a = fit(img)
print(a)
cv2.imshow('IMG', cv2.resize(img_,None, fx=0.5, fy=0.5))
'''
