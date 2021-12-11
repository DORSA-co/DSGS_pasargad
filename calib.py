import numpy as np
import cv2



DEBUG = False


def draw_contour(gray, cnts):
    img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    img = cv2.drawContours( img, cnts , -1, (0,0,255), thickness=3)
    return img


def draw_rect(gray, cnts, areas):
    img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    for i,cnt in enumerate(cnts):
        x,y,w,h = cv2.boundingRect(cnt)
        color = (np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255))
        cv2.putText( img, str(areas[i]) , (x,y) , cv2.FONT_HERSHEY_DUPLEX, 1, color )
        img = cv2.drawContours( img, [cnt] , 0, color, thickness=3)
    return img



def imshow(name, img):
    cv2.imshow(name, cv2.resize(img, None, fx=0.5, fy=0.5))




    

def extract_info( gray, areas_mm , min_area=2000, max_area=50000 , accuracy = 0.9 ):
    nrects = len(areas_mm)
    areas_mm = list(areas_mm)
    gray = np.array(gray, dtype=np.uint8)
    _,mask = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    if DEBUG:
        imshow('mask', mask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    cnts,_ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    if DEBUG:
        img = draw_contour( gray, cnts)
        imshow('all contours', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    
    filter_area = lambda x: min_area< cv2.contourArea(x) < max_area
    cnts = list( filter( filter_area, cnts))
    if DEBUG:
        img = draw_contour( gray, cnts)
        imshow('area filtered contours', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        
    def filter_acc(x):
        _,(w,h),_ = cv2.minAreaRect(x)
        rect_area = w*h
        area = cv2.contourArea(x)
        return area/rect_area > accuracy
    cnts = list( filter( filter_acc, cnts))
    if DEBUG:
        img = draw_contour( gray, cnts)
        imshow('accuraye filtered contours', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    cnts.sort(key = lambda x:cv2.contourArea(x), reverse=True)
    rects = cnts[:nrects]
    areas_mm.sort(reverse=True)
    if DEBUG:
        img = draw_rect( gray, rects, areas_mm)
        imshow('Final Rectangles', img)
        cv2.waitKey(0)
        #cv2.destroyAllWindows()

    infoes = []
    for i in range(len(rects)):
        (x,y),_,_ = cv2.minAreaRect(rects[i])
        area_px = cv2.contourArea(rects[i])
        area_mm = areas_mm[i]
        px2mm = np.sqrt( area_mm/ area_px )
        infoes.append([x,y , px2mm])
    infoes = np.array(infoes)
    infoes = np.mean(infoes, axis=0)
    return infoes





    for i in range(2):
        _,(w,h),_ = cv2.minAreaRect(rects[i])
        print(w*infoes[i][-1] , h*infoes[i][-1])









def solve_equation( inputs ):
    inputs = np.array(inputs)
    inputs = np.insert(inputs, -1, 1, axis=1)

    d = np.copy( inputs[:,:3] )
    
    dx = np.copy( d )
    dx[:,0] = inputs[:,-1]
    
    dy = np.copy( d )
    dy[:,1] = inputs[:,-1]
    
    dz = np.copy( d )
    dz[:,2] = inputs[:,-1]

    d = np.linalg.det(d)
    dx = np.linalg.det(dx)
    dy = np.linalg.det(dy)
    dz = np.linalg.det(dz)

    kx = dx/d
    ky = dy/d
    kz = dz/d
    return np.array([kx,ky,kz])

    print(dz.shape, dy.shape, dx.shape, d.shape)




def calc_radius(circels, coef ):
    kx,ky,c = coef
    px2mms = circels[:,0]*kx + circels[:,1]*ky + c
    radiuses_mm = circels[:,-1] * px2mms
    return radiuses_mm
    

    
 

if __name__ == '__main__':
    gray = cv2.imread('bas.png',0)
    info = extract_info(gray, [1500,1800], min_area=2000, max_area=50000, accuracy=0.9)
