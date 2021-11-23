import cv2
import numpy as np
import os
#______________________________________________________________________________________________________________________________________
#
#______________________________________________________________________________________________________________________________________


def __checkCnt__(img,cnt):
    area = cv2.contourArea(cnt)
    if area>100:
        res = np.copy(img)
        cv2.drawContours(res,[cnt],0,(255,0,0), thickness=3)
        print(area)
        cv2.imshow('res DEBUG2', cv2.resize(res,None, fx=0.4,fy=0.4))
        cv2.waitKey(0)

DEBUG = False
DEBUG2 = False
def get_circels(img,accuracy=0.5, min_area=100,max_area = 2000, bias=20):

    #-----------------------------------------------------------------------------------------
    #Labview to python
    img = np.array(img,dtype=np.uint8)
    #img = np.reshape(img,(h,w,channel))
    img = np.moveaxis(img,[0,1,2],[2,0,1])
    if DEBUG:
        cv2.imshow('img', cv2.resize(img,None, fx=0.4,fy=0.4))
        cv2.waitKey(0)
    #-----------------------------------------------------------------------------------------
    #Pre Processing ( Color to Gray And Adaptive Equlize Hisogram)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(17,17))
    gray = clahe.apply(gray)
    if DEBUG:
        cv2.imshow('gray', cv2.resize(gray,None, fx=0.4,fy=0.4))
        cv2.waitKey(0)

    #-----------------------------------------------------------------------------------------
    #Edge Detection By Combination Blur and Adaptive
    #res = cv2.blur(gray, (51,51))
    gray = cv2.blur(gray, (7,7))
    #gray = cv2.absdiff( res,gray)
    #gray = cv2.bilateralFilter(gray,11,75,75)
    if DEBUG:
        cv2.imshow('blur', cv2.resize(gray,None, fx=0.4,fy=0.4))
        cv2.waitKey(0)
        
    edge = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 71, 5)
    if DEBUG:
        cv2.imshow('adaptive theresh', cv2.resize(edge,None, fx=0.4,fy=0.4))
        cv2.waitKey(0)
    #-----------------------------------------------------------------------------------------
    #ّFilter1 For Bad Contours
    bad_area1 = 500
    bad_area2 = 2000
    
    cnts,h= cv2.findContours(edge, cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts)==0:
        return np.array([[-1,-1,-1]], dtype=np.float64).reshape((1,3))
    h = h[0]
    cnts_h = list(zip(cnts,h))

    filter_bad_func1 = lambda x: True if ( bad_area1<(cv2.contourArea(x[0]) )) else False
    bad_cnts_h = list(filter(filter_bad_func1,cnts_h))
    bad_cnts = list(map(lambda x:x[0],bad_cnts_h))
    cv2.drawContours(edge, bad_cnts, -1, 255, thickness=-1)
    if DEBUG:
        cv2.imshow('bad filter1', cv2.resize(edge,None, fx=0.4,fy=0.4))
        cv2.waitKey(0)

    #-----------------------------------------------------------------------------------------
    #Function For Detec Pellet Contour
    height,width = gray.shape
    def filter_pellet(cnt):
        SIZE=3
        mean_ind = 250
        area = cv2.contourArea(cnt)
        if min_area<area<max_area:
            (x,y),r = cv2.minEnclosingCircle(cnt)
            if area/(np.pi * r*r) > accuracy :
                
                cnt_ = np.copy(cnt)
                cnt_ = cnt_.reshape((-1,2))
                x1,y1 = cnt_.min(axis=0)
                x2,y2 = cnt_.max(axis=0)
                roi = res[y1:y2,x1:x2]
                mask = np.zeros_like(roi)
                cnt_[:,0] = cnt_[:,0] - x1
                cnt_[:,1] = cnt_[:,1] - y1
                cnt_ = cnt_.reshape((-1,1,2))
                cv2.drawContours(mask, [cnt_], 0, 255, thickness=-1)            
                if cv2.mean( roi, mask)[0]>mean_ind:
                    return True
        else:
            return False

    #-----------------------------------------------------------------------------------------
    #Function For Conver Contour to Circel
    def cnt2circel(cnt):
        global _iter_
        biases = [10,10,15,20]
        (x,y),r = cv2.minEnclosingCircle(cnt)
        #return [x,y, (r + 10  )*1.5]
        return [x,y, (r + biases[0])]
    #-----------------------------------------------------------------------------------------
    #iteration For Detec Pellet With Diffrent Sizes

    res = np.copy(edge)
    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    gondle = []
    circels = []
    for _iter_ in range(4):
        #-----------------------------------
        cnts,h= cv2.findContours(res, cv2.RETR_LIST  , cv2.CHAIN_APPROX_SIMPLE)

        if DEBUG2:
            for cnt in cnts:
                __checkCnt__(img,cnt)
        gondle_ = list( filter(filter_pellet, cnts))
        circels_ = list( map(cnt2circel, gondle_))
        gondle = gondle + gondle_
        circels = circels + circels_

        cv2.drawContours( res, gondle, -1, 0, -1)
        if DEBUG:
            img_ = np.copy(img)
            for (x,y,r) in circels_:
                cv2.circle(img_, (int(x),int(y)), int(r), (0,255,0), thickness=2)
                
            cv2.imshow('extract', cv2.resize(res,None, fx=0.4,fy=0.4))
            cv2.imshow('img_', cv2.resize(img_,None, fx=0.4,fy=0.4))
            
            cv2.waitKey(0)

        res = cv2.erode(res, kernel)
        if DEBUG:
            cv2.imshow('erode', cv2.resize(res,None, fx=0.4,fy=0.4))
            cv2.waitKey(0)
            
          
        
    if len(circels)==0:
        return np.array([[-1,-1,-1]], dtype=np.float64).reshape((1,3))
    return np.array( circels, dtype=np.float64)              

#-----------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------
def draw_cicles(img,circles,thickness=2, boundaries=[25,30]):
    img = np.array(img,dtype=np.uint8)
    channel,h,w = img.shape
    img = np.moveaxis(img,[0,1,2],[2,0,1])
    res = np.copy(img)
    for (x,y,r) in circles :
        if int(r)<boundaries[0]:
            cv2.circle(res, (int(x),int(y)), int(r), (0,0,255), thickness=thickness)
            
        elif r<boundaries[1]:
            cv2.circle(res, (int(x),int(y)), int(r), (0,255,0), thickness=thickness)

        else:
            cv2.circle(res, (int(x),int(y)), int(r), (255, 0,0), thickness=thickness)

    res = np.moveaxis(res,[0,1,2],[1,2,0])
    return res
    
#-----------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------
def draw_center(img,circles, boundaries=[25,30]):
    img = np.array(img,dtype=np.uint8)
    channel,h,w = img.shape
    img = np.moveaxis(img,[0,1,2],[2,0,1])
    res = np.copy(img)
    for (x,y,r) in circles :
        if int(r)<boundaries[0]:
            cv2.circle(res, (int(x),int(y)), int(5), (0,0,255), thickness=-1)
            
        elif r<boundaries[1]:
            cv2.circle(res, (int(x),int(y)), int(5), (0,255,0), thickness=-1)

        else:
            cv2.circle(res, (int(x),int(y)), int(5), (255, 0,0), thickness=-1)

    res = np.moveaxis(res,[0,1,2],[1,2,0])
    return res


#-----------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------
def increas_contrast(img,landa=0.5):
    iimg = np.array(img,dtype=np.uint8)
    channel,h,w = img.shape
    img = np.moveaxis(img,[0,1,2],[2,0,1])
    res = np.copy(img)
    #-----------------
    lookUpTable = np.empty((1,256), np.uint8)
    for i in range(256):
        lookUpTable[0,i] = np.clip(pow(i / 255.0, landa) * 255.0, 0, 255)
    res = cv2.LUT(res, lookUpTable)

    #-----------------
    res = np.moveaxis(res,[0,1,2],[1,2,0])
    return res




'''
import time
img = cv2.imread('2.bmp')

img = np.zeros((500,500),dtype = np.uint8)
cnt1 = np.array([[100,100],[400,100],[400,400],[100,400]])
#cv2.drawContours(img,[cnt1],0,255,-1)
cv2.imshow('img', img)
cnt2 = np.array([[200,200],[300,200],[300,300],[200,300]])
cv2.drawContours(img,[cnt2],0,255,-1)
cv2.imshow('img', img)


img = np.moveaxis(img,[0,1,2],[1,2,0])
t = time.time()
circ = get_circels(img)
t = time.time() - t 
print('num:',len(circ),'t:',t)
img = increas_contrast(img)
res = draw_cicles(img,circ)
res2 = draw_center(img, circ)
res = np.moveaxis(res,[0,1,2],[2,0,1])
res2 = np.moveaxis(res2,[0,1,2],[2,0,1])
cv2.imshow('res', cv2.resize(res,None, fx=0.5,fy=0.5))
cv2.imshow('res2', cv2.resize(res2,None, fx=0.5,fy=0.5))

'''
    


