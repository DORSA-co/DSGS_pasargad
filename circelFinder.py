import numpy as np
import cv2




DEBUG = False

def draw_contour(gray, cnts):
    img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    img = cv2.drawContours( img, cnts , -1, (0,0,255), thickness=1)
    return img


def draw_circels( gray, circels, rs=None ):
    img = cv2.cvtColor(gray, cv2.COLOR_GRAY2BGR)
    circels = circels.astype(np.int32)
    for i,circel in enumerate(circels):
        color = (np.random.randint(0,255),np.random.randint(0,255),np.random.randint(0,255))
        x,y,r = circel
        cv2.circle( img, (x,y) , r, color, thickness=3 )
        if rs is not None:
            cv2.putText( img, str( rs[i] ), (x+20,y-10) , cv2.FONT_HERSHEY_COMPLEX_SMALL, 1, (0,0,0))
    return img
    



def extract_circels( gray , min_area=100, max_area=50000 , accuracy = 0.7 ):
    gray = np.array(gray, dtype=np.uint8)
    _,mask = cv2.threshold(gray, 100, 255, cv2.THRESH_BINARY)

    if DEBUG:
        cv2.imshow('mask', mask)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    cnts,_ = cv2.findContours(mask, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
    if DEBUG:
        img = draw_contour( gray, cnts)
        cv2.imshow('all contours', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
        
    
    filter_area = lambda x: min_area< cv2.contourArea(x) < max_area
    cnts = list( filter( filter_area, cnts))
    if DEBUG:
        img = draw_contour( gray, cnts)
        cv2.imshow('area filtered contours', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

        
    def filter_acc(x):
        _,r = cv2.minEnclosingCircle(x)
        circel_area = np.pi * (r**2)
        area = cv2.contourArea(x)
        return area/circel_area > accuracy
    cnts = list( filter( filter_acc, cnts))
    if DEBUG:
        img = draw_contour( gray, cnts)
        cv2.imshow('accuraye filtered contours', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()


    def cnt2circel(pts):
        (x,y),r = cv2.minEnclosingCircle(pts)
        return [x,y,r]
    circels = cnts = list( map( cnt2circel, cnts))
    circels = np.array( circels )
    if DEBUG:
        img = draw_circels(gray, circels)
        cv2.imshow('Pellet circels', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    
    return circels









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
    fname = 'bas_c.png'
    img = cv2.imread(fname)
    cv2.imshow('img', img)
    gray = cv2.imread(fname,0)

    '''
    cap = cv2.VideoCapture(0)
    while True:
        _,img = cap.read()
        cv2.imshow('img',img)
        key = cv2.waitKey(10)
        if key!=-1:
            break

    cv2.imwrite('circels.png', img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    '''
    DEBUG = False
    import calib
    
    circels = extract_circels( gray , min_area=50, max_area=5000 , accuracy = 0.7 )
    ks = [ 4.22011156e-06, -1.09305028e-05,  3.09454825e-01]


    rs = calib.calc_radius(circels, ks )
    #rs = circels[:,-1]
    ds = rs*4
    ds = ds.astype(np.float16)
    img = draw_circels( gray, circels, ds )
    cv2.imshow('img',img)
    

    
