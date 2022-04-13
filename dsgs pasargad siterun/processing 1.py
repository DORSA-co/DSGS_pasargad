import cv2
import numpy as np
#import calibration as calib

def __checkCnt__(img,cnt):
    area = cv2.contourArea(cnt)
    if area>100:
        res = np.copy(img)
        cv2.drawContours(res,[cnt],0,(255,0,0), thickness=3)
        print(area)
        cv2.imshow('res DEBUG2', cv2.resize(res,None, fx=0.4,fy=0.4))
        cv2.waitKey(0)

DEBUG = False
TIME = 0
DEBUG2 = False
def get_circels(img, bias=14,accuracy=0.5, min_area=100,max_area = 2000):
    try:
        #-----------------------------------------------------------------------------------------
        #Labview to python
        gray = np.array(img,dtype=np.uint8)
        img = cv2.merge((gray,gray,gray))
        #img = np.reshape(img,(h,w,channel))
        #img = np.moveaxis(img,[0,1,2],[2,0,1])
        if DEBUG:
            cv2.imshow('img', cv2.resize(gray,None, fx=0.4,fy=0.4))
            cv2.waitKey(TIME)
        #-----------------------------------------------------------------------------------------
        #Pre Processing ( Color to Gray And Adaptive Equlize Hisogram)
        #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(17,17))
        gray = clahe.apply(gray)
        if DEBUG:
            cv2.imshow('gray', cv2.resize(gray,None, fx=0.4,fy=0.4))
            cv2.waitKey(TIME)

        #-----------------------------------------------------------------------------------------
        #Edge Detection By Combination Blur and Adaptive
        #res = cv2.blur(gray, (51,51))
        gray = cv2.blur(gray, (7,7))
        #gray = cv2.absdiff( res,gray)
        #gray = cv2.bilateralFilter(gray,11,75,75)
        if DEBUG:
            cv2.imshow('blur', cv2.resize(gray,None, fx=0.4,fy=0.4))
            cv2.waitKey(TIME)
            
        edge = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY, 31, 3)
        if DEBUG:
            cv2.imshow('adaptive theresh', cv2.resize(edge,None, fx=0.4,fy=0.4))
            cv2.waitKey(TIME)
        #-----------------------------------------------------------------------------------------
        #ّFilter1 For Bad Contours
        bad_area1 = 500
        bad_area2 = 2000
        
        cnts,h= cv2.findContours(edge, cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)
        if len(cnts)==0:
            return np.array([[-1,-1,-1]], dtype=np.float64).reshape((1,3))
        h = h[0]
        cnts_h = list(zip(cnts,h))

        #filter_bad_func = lambda x: True if ( (cv2.contourArea(x[0]) < bad_area1 )or ( bad_area1< cv2.contourArea(x[0]) <bad_area2  and cv2.contourArea(x[0])/(np.pi * cv2.minEnclosingCircle(x[0])[1]**2) < 0.6)) else False
        #filter_bad_func = lambda x,y: True if ( (cv2.contourArea(x) < bad_area1 )or ( bad_area1< cv2.contourArea(x) <bad_area2  and y[-2]==-1 < accuracy)) else False
        filter_bad_func1 = lambda x: True if ( bad_area1<(cv2.contourArea(x[0]) )) else False
        bad_cnts_h = list(filter(filter_bad_func1,cnts_h))
        bad_cnts = list(map(lambda x:x[0],bad_cnts_h))
        cv2.drawContours(edge, bad_cnts, -1, 255, thickness=-1)
        if DEBUG:
            cv2.imshow('bad filter1', cv2.resize(edge,None, fx=0.4,fy=0.4))
            cv2.waitKey(TIME)
        #-----------------------------------------------------------------------------------------
        #ّFilter2 For Bad Contours
        '''
        cnts,h= cv2.findContours(edge, cv2.RETR_TREE , cv2.CHAIN_APPROX_SIMPLE)
        
        if len(cnts)==0:
            return np.array([[-1,-1,-1]], dtype=np.float64).reshape((1,3))
        h = h[0]
        cnts_h = list(zip(cnts,h))

        filter_bad_func2 = lambda x: True if ( bad_area2<(cv2.contourArea(x[0]) )) else False
        bad_cnts_h = list(filter(filter_bad_func2,cnts_h))
        bad_cnts = list(map(lambda x:x[0],bad_cnts_h))
        cv2.drawContours(edge, bad_cnts, -1, 255, thickness=-1)
        if DEBUG:
            cv2.imshow('bad filter2', cv2.resize(edge,None, fx=0.4,fy=0.4))
            cv2.waitKey(0)
        '''

        #-----------------------------------------------------------------------------------------
        #Function For Detec Pellet Contour
        height,width = gray.shape
        def filter_pellet(cnt):
            SIZE=3
            mean_ind = 240
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
        def cnt2circel(i):
            def _cnt2circel_(cnt):
                global _iter_
                biases = [12,12,12,12] #[13,12,16,18]
                (x,y),r = cv2.minEnclosingCircle(cnt)
                #return [x,y, (r + 10  )*1.5]
                return [x,y, (r + bias)]
                
            return _cnt2circel_
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
            circels_ = list( map(cnt2circel(_iter_), gondle_))
            gondle = gondle + gondle_
            circels = circels + circels_

            cv2.drawContours( res, gondle, -1, 0, -1)
            if DEBUG:
                img_ = np.copy(img)
                for (x,y,r) in circels_:
                    cv2.circle(img_, (int(x),int(y)), int(r), (0,255,0), thickness=2)
                    
                cv2.imshow('extract', cv2.resize(res,None, fx=0.4,fy=0.4))
                cv2.imshow('img_', cv2.resize(img_,None, fx=0.4,fy=0.4))
                
                cv2.waitKey(TIME)

            res = cv2.erode(res, kernel)
            if DEBUG:
                cv2.imshow('erode', cv2.resize(res,None, fx=0.4,fy=0.4))
                cv2.waitKey(TIME)
                
              
            
        if len(circels)==0:
            return np.array([[-1,-1,-1]], dtype=np.float64).reshape((1,3))
        return np.array( circels, dtype=np.float64)

    except:
        return np.array([[-1,-1,-1]], dtype=np.float64).reshape((1,3))

        

#-----------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------------------

#-----------------------------------------------------------------------------------------------------------------------------
def draw_cicles(img,circles,thickness=1, boundaries=[25,30]):
    img = np.array(img,dtype=np.uint8)
    channel,h,w = img.shape
    #img = np.moveaxis(img,[0,1,2],[2,0,1])
    res = np.copy(img)
    for (x,y,r) in circles :
        if int(r)<boundaries[0]:
            cv2.circle(res, (int(x),int(y)), int(r), (0,0,255), thickness=thickness)
            
        elif r<boundaries[1]:
            cv2.circle(res, (int(x),int(y)), int(r), (0,255,0), thickness=thickness)

        else:
            cv2.circle(res, (int(x),int(y)), int(r), (255, 0,0), thickness=thickness)

    #res = np.moveaxis(res,[0,1,2],[1,2,0])
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


if __name__ == '__main__' and False:
    path ='disc03 pics'
    #path = 'tests'
    import os
    for fname in os.listdir(path):
        img = cv2.imread( os.path.join( path, fname),0)
        cv2.imshow('img',cv2.resize(img,None,fx=0.5,fy=0.5))
        
        circ = get_circels(img)
        img_ = cv2.merge( (img, img, img)) 
        res = draw_cicles(img_, circ)
        cv2.imshow('res',cv2.resize(res,None,fx=0.5,fy=0.5))
        cv2.waitKey(0) 

'''
mtx = np.array([[-0.972168, -0.0637452, 594.339],
                [-0.0351841, 0.992448, -13.0618],
                [0.0000987100,-0.000164460,1.]])#28

coef = 4.78
#coef = 0.20845968

cal_img = cv2.imread('28_calib.jpg')
cal_img = np.moveaxis(cal_img, [0,1,2],[1,2,0])
m = calib.fit(cal_img)
coef = m[3,0]
mtx = m[0:3,:]


img = cv2.imread('28.bmp')
img_ = np.moveaxis(img,[0,1,2],[1,2,0])

circ = get_circels(img_)
#---------------------------------
thresh = np.array([[0,6.3],[6.3,8],[8,10],[10,12.5],[12.5,14],[14,16],[16,100]])
rs = calib.predict(mtx,coef, circ, mode='mean')
rs_ = circ[:,-1] / coef
#---------------------------------
hist = np.array([0,0,0,0,0,0,0,0])

thresh  = thresh**3
for r in rs:
    v = (r*2)**3
    for i,th in enumerate(thresh):
        if th[0]<= v <th[1]:
            hist[i]+=v

hist =hist/ hist.sum()
print(hist)
    


res = draw_cicles(img_, circ)
res = np.moveaxis( res,[0,1,2],[2,0,1])
cv2.imshow('rs',cv2.resize(res,None,fx=0.29,fy=0.29))
cv2.waitKey(0)
'''

