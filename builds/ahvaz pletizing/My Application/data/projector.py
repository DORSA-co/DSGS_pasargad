import cv2
import numpy as np

def calib_light(img,scale=0.6, size=0.5):
    img = np.array( img, dtype= np.uint8)
    img = np.moveaxis(img,[0,1,2],[2,0,1])
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h,w = gray.shape
    h_ = int(h*size)
    w_ = int(w*size)
    offset_x = int(( w - w_)/2)
    offset_y = int(( h - h_)/2)
    roi = gray[ offset_y: offset_y + h_ , offset_x: offset_x + w_ ]
    return np.float32( roi.mean()/255 * scale)
#15

def check_light(img,thresh, size=0.5):
    img = np.array( img, dtype= np.uint8)
    img = np.moveaxis(img,[0,1,2],[2,0,1])
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    h,w = gray.shape
    h_ = int(h*size)
    w_ = int(w*size)
    offset_x = int(( w - w_)/2)
    offset_y = int(( h - h_)/2)
    roi = gray[ offset_y: offset_y + h_ , offset_x: offset_x + w_ ]
    if ( roi.mean()/255. < thresh):
        return False
    return True


        
        


        
