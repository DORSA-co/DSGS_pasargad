import cv2
import numpy as np
import os
#from matplotlib import pyplot as plt
#import keras
#import tensorflow as tf
#______________________________________________________________________________________________________________________________________
#
#______________________________________________________________________________________________________________________________________
#img = cv2.imread('1.bmp')

#return [x,y,r]
path = 'imgs_final/'
DEBUG = False
DEBUG2 = False
def get_circels(img,accuracy=0.4, min_area=120,max_area = 2000, bias=20):

    img = np.array(img,dtype=np.uint8)
    if len(img.shape)==3 :
   
        img = np.moveaxis(img,[0,1,2],[2,0,1])
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    elif len(img.shape)==2 :
        gray = np.copy(img)
    #-----------------------------------

    if DEBUG:
        cv2.imshow('img', cv2.resize(img,None, fx=0.4,fy=0.4))
        cv2.waitKey(0)

    #
    
    clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(17,17))
    gray = clahe.apply(gray)
    if DEBUG:
        cv2.imshow('gray', cv2.resize(gray,None, fx=0.4,fy=0.4))
        cv2.waitKey(0)

    #gray = cv2.medianBlur(gray, 17)
    res = cv2.blur(gray, (51,51))
    #res = cv2.bilateralFilter(res,9,75,75)
    gray = cv2.blur(gray, (5,5))
    gray = cv2.bilateralFilter(gray,11,75,75)
    

    #gray = cv2.blur(gray, (15,15))

    edge = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 71, 5)

    if DEBUG:
        cv2.imshow('adaptive theresh', cv2.resize(edge,None, fx=0.4,fy=0.4))
        cv2.waitKey(0)


    bad_area1 = 1000
    bad_area2 = 5000
    
    cnts,h= cv2.findContours(edge, cv2.RETR_LIST , cv2.CHAIN_APPROX_SIMPLE)

    filter_bad_func = lambda x: True if ( (cv2.contourArea(x) < bad_area1 )or ( bad_area1< cv2.contourArea(x) <bad_area2  and cv2.contourArea(x)/(np.pi * cv2.minEnclosingCircle(x)[1]**2) < 0.6)) else False
    bad_cnts = list(filter(filter_bad_func,cnts))
    cv2.drawContours(edge, bad_cnts, -1, 255, thickness=-1)
    if DEBUG:
        cv2.imshow('threhs_draw', cv2.resize(edge,None, fx=0.4,fy=0.4))
        cv2.waitKey(0)
    '''
    for cnt in cnts:
        area = cv2.contourArea(cnt)
        (x,y),r = cv2.minEnclosingCircle(cnt)
        len_ = cv2.arcLength(cnt, True)
        if area < bad_area1 or ( bad_area1< area <bad_area2  and area/(np.pi * r*r) < 0.6):
            edge = cv2.drawContours(edge, [cnt], 0, 255, thickness=-1)
        #elif  ( bad_area1< area <bad_area2  and min(len_,(np.pi * 2 *r)) / max(len_,(np.pi * 2 *r)) < 0.5)  :
        #    edge = cv2.drawContours(edge, [cnt], 0, 255, thickness=-1)
    if DEBUG:
        cv2.imshow('threhs_draw', cv2.resize(edge,None, fx=0.4,fy=0.4))
        cv2.waitKey(0)
    '''


    res = np.copy(edge)

    kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(5,5))
    res = cv2.erode(res, kernel, iterations=4)

    if DEBUG:
        cv2.imshow('erode', cv2.resize(res,None, fx=0.4,fy=0.4))
        cv2.waitKey(0)
        

    #res = cv2.dilate(res, np.ones((5,5)), iterations=2)
    if DEBUG:
        cv2.imshow('dilate', cv2.resize(res,None, fx=0.4,fy=0.4))
        cv2.waitKey(0)
    
    #-----------------------------------
    cnts,h= cv2.findContours(res, cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)
    #cnts.sorted(key=lambda x:cv2.contourArea(x), reverse=True)
    h = h[0]
    gondle = []
    circels = []
    bad_parrents =[]
    #bias = int(MaxPool/2)
    mean_ind = 200

    def filter_pellet(cnt):
        area = cv2.contourArea(cnt)
        if min_area<area<max_area:
            (x,y),r = cv2.minEnclosingCircle(cnt)
            if area/(np.pi * r*r) > accuracy :
                roi = res[int(y)-2:int(y)+3, int(x)-2:int(x)+3]
                if roi.mean()>mean_ind:
                    return True
        return False

    def cnt2circel(cnt):
        (x,y),r = cv2.minEnclosingCircle(cnt)
        #return [x,y, (r + 10  )*1.5]
        return [x,y, (r + bias)]


    gondle = list( filter(filter_pellet, cnts))
    circels = list( map(cnt2circel, gondle))


    '''
    for i,cnt in enumerate(cnts):
        if DEBUG2:
            print(i)
            (x,y),r = cv2.minEnclosingCircle(cnt)
            temp_cnt = np.copy(img)
            print('cnt_area:', cv2.contourArea(cnt), 'h cond:',(h[i,-1]==-1 or h[i,-1] in bad_parrents),'acc:',cv2.contourArea(cnt)/(np.pi * r*r), 'ind:',mean_indensity )
            cv2.imshow('temp_cnt', cv2.resize(temp_cnt,None, fx=0.4,fy=0.4))
            cv2.waitKey(0)
        area = cv2.contourArea(cnt)
        if min_area<area<max_area:
            (x,y),r = cv2.minEnclosingCircle(cnt)
            if area/(np.pi * r*r) > accuracy :
                if h[i,-1]==-1 or h[i,-1] in bad_parrents:
                    roi = res[int(y)-2:int(y)+3, int(x)-2:int(x)+3]
                    if roi.mean()>mean_ind:
                        gondle.append(cnt)
                        circels.append([x,y,r+bias])
                else:
                    cnt_p = cnts[h[i,-1]]
                    area_p = cv2.contourArea(cnt_p)
                    (x_p,y_p),r_p = cv2.minEnclosingCircle(cnt_p)
                    if area_p/(np.pi * r_p * r_p) > 0.6:
                        gondle.append(cnt_p)
                        circels.append([x_p,y_p,r_p+bias])
                    else:
                        gondle.append(cnt)
                        circels.append([x,y,r+bias])
                        bad_parrents.append(h[i,-1])
                    
        elif h[i,-2]!=-1:
            bad_parrents.append(i)
            
    '''
    return np.array( circels, dtype=np.float64)                   




#-----------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------
def draw_cicles(img,circles,thickness=2, boundaries=[35,45]):
    img = np.array(img,dtype=np.uint8)
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
def draw_center(img,circles, boundaries=[35,45]):
    img = np.array(img,dtype=np.uint8)
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
    img = np.array(img,dtype=np.uint8)
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





if __name__ == '__main__':

    #path = 'shiraz pics/'
    path = 'shiraz pics/'
    print(os.listdir(path))
    for img_name in os.listdir(path):
        full_path = os.path.join(path,img_name)
        img = cv2.imread(full_path)

        #---------------for labview------------------\
        img = np.moveaxis(img,[0,1,2],[1,2,0])
        circels = get_circels(img)
        print(len(circels))
        res = draw_cicles( img, circels )
        res = np.moveaxis(res,[0,1,2],[2,0,1])

        circels[:,-1] = circels[:,-1] * 0.25#mm
        
        
        ranges= np.array([0,6,8,10,12.5,14,16,18,50])
        count1 = np.array([0]*8)
        count2 = np.array([0]*8)

        percentage1 = np.array([0]*8)
        percentage2 = np.array([0]*8)
        
        bias = 0.5
        for circel in circels:
            for i in range(0,len(ranges)-1):

                if ranges[i] <circel[-1]< ranges[i+1]:
                    count1[i]+=1
                    percentage1[i]+= circel[-1]**3
                    
                if ranges[i] + bias <circel[-1]< ranges[i+1] - bias:
                    count2[i]+=1
                    percentage2[i]+= circel[-1]**3
            
            
        percentage1 = percentage1 / percentage1.sum() * 100
        percentage2 = percentage2 / percentage2.sum() * 100
        print(count1, percentage1)
        print(count2, percentage2)
        print('-'*100)


        
        cv2.imshow('res', cv2.resize(res, None, fx=0.5, fy=0.5) )
        cv2.waitKey(0)
