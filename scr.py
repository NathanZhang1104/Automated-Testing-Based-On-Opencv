
from airtest.core.api import *
import time
import cv2
connect_device('Android:127.0.0.1:21503')
def getsc(form=0,sleep=0.3):
    time.sleep(sleep)
    # snapshot('rf\\scrpart.jpg')
    # ret=cv2.imread('rf\\scrpart.jpg')
    # ret.resize((720,1080,3))
    # os.system('cd D:\\文件\\python\\lib\\site-packages\\airtest\\core\\android\\static\\adb\\windows')
    # os.system('d:')
    if form==0:
        img=snapshot('rf\\scr.png')

        # touch((487,1700))
        rect=img.shape[:2]
        ret = img[:, 0:int(rect[0] * 1.66)]
        cv2.imwrite('rf\\scr.png',ret)
    if form==1:
        os.system(
            'D:\\python3.6\\lib\\site-packages\\airtest\\core\\android\\static\\adb\\windows\\adb shell screencap -p /sdcard/screen.png')
        os.system(
            'D:\\python3.6\\lib\\site-packages\\airtest\\core\\android\\static\\adb\\windows\\adb pull /sdcard/screen.png C:\\Users\\dell\\PycharmProjects\\untitled11\\rf\\scr.png')
        img=cv2.imread('rf\\scr.png')
        rect=img.shape[:2]
        ret = img[:, 0:int(rect[0] * 1.66)]
        cv2.imwrite('rf\\scr.png',ret)
    return ret
def scrpart(x1,x2):
    scrimg=cv2.imread('rf\\scr.png')
    rect=getrect()
    scrpartimg=scrimg[int(x2[0]*rect[0]):int(x2[1]*rect[0]),int(x1[0]*rect[1]):int(x1[1]*rect[1])]
    cv2.imwrite('rf\\scrpart.png',scrpartimg)
    return scrpartimg

def getrect():
    # im=getsc()
    ret=cv2.imread('rf\\scr.png').shape[:2]

    return ret
def template_pos(img,sample=None):
    time.sleep(0.1)
    if type(img)!=str:
        cv2.imwrite('rf\\temc.png',img)
        try:
            po=loop_find(Template('rf\\temc.png'),sample, timeout=1)
            return po
        except:
            return None
    else:
        try:
            po=loop_find(Template(img,sample), timeout=1)
            return po
        except:
            return None


if __name__=='__main__':
    # print(pyautogui.size())
    # img = np.where(manage.scrmask == 1, img, 255)
    # cv2.imshow('2', img)
    # cv2.waitKey()
    print(time.time())
    img = getsc()

    print(time.time())
    img = scrpart((0.45, 0.54), (0.01, 0.1))

    # img =scrpart((0.223, 0.296), (0.27, 0.39))
    cv2.imshow('1',img)

    cv2.waitKey(0)
        # print(getrect())
    # scrpart((0.43,0.6),(0.58,0.7675))
    # print('a',time.time())
    # po=loop_find(Template('rf\\scrpart.png'), timeout=1)e
    # template_pos(cv2.imread('rf\\'))
    # print(a.record_pos)
    # po2=template_pos(cv2.imread('rf\\shenmi.png'),sample='rf\\scr.png')
    po=template_pos('rf\\lian.png')
    # print(po,po2)
    # print(po[0]-po2[0],po[1]-po2[1])
    # img = scrpart((0.42, 0.53), (0.3, 0.35))
    # # print(ST.FIND_TIMEOUT)
    # # img1=cv2.rectangle(img,po,(po[0]+10,po[1]+10),color=0)
    # print('b',time.time())
    # print(po)
    # print(828/1792,653/1080)
    touch(po)



# -514 375


