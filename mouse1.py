import scr
import time
from airtest.core.api import *
connect_device("android:127.0.0.1:21503")
import warnings

def tranxy(po1):
    if abs(po1[0])>=1 and abs(po1[1])>=1:
        ret=po1
    else:
        rect=scr.getrect()
        ret=(int(po1[0]*rect[1]),int(po1[1]*rect[0]))

    return ret
def op_tranxy(x1,y1,curwin=0):
    rect=scr.getrect()
    if curwin==0:
        x1=x1/(rect[2]-rect[0])
        y1=y1/(rect[3]-rect[1])
    elif curwin==2:
        x1=(x1-rect[0])/(rect[2]-rect[0])
        y1=(y1-rect[1])/(rect[3]-rect[1])
    elif curwin==1:
        x1 = (x1 - rect[0])
        y1 = (y1 - rect[1])
    ret=[x1,y1]
    return ret
def swipeTo(po1,po2,duration=0.5,steps=4):
    po1=tranxy(po1)
    po2=tranxy(po2)
    if po1[0]==po2[0]:
        po1=(po1[0]+4,po1[1])
    if po1[1]==po2[1]:
        po1=(po1[0],po1[1]+4)
    swipe(v1=po1,v2=po2,duration=duration, steps=steps)

def Tough(po1,ju=None,sleep=0.1):
    time.sleep(0.1)
    if ju==None:
        po1 = tranxy(po1)
        touch(po1)
    else:
        po1=tranxy((po1,ju))
        touch(po1)

def swipeRel(po1,rel1,pause=0.05):
    po1=tranxy(po1)
    rel1=tranxy(rel1)
    po2=(po1[0]+rel1[0],po1[1]+rel1[1])
    swipeTo(po1,po2)
    time.sleep(0.2)



def doubleClick(po1,ju_tranxy=True,sleep=0.1):
    po1=tranxy(po1)
    double_click(po1)
def initcur(full=False):
#     moveTo(0.5,0.5)
    pinch('in')
    time.sleep(0.2)
    swipeTo((0.2,0.2),(0.8,0.8))
def recover1(sleep=0.1,form=0 ):
    swipeTo((0.9,0.8),(0.91,0.81))
def muti_Swipe(po,duration=0.7,steps=6):
    otherdw(po,duration=duration,steps=steps)

if __name__=='__main__':
    p3 = [0.30638629283489096, 0.7566489361702128]

    swipeRel(p3, (0, -0.3))
    # muti_Swipe(((100,300),(223,221),(438,428),(223,221),(438,428),))
    # initcur()
    # for i in range(9):
    #     swipeRel((0.20638629283489096, 0.7566489361702128),(0,-0.3))
    # initcur()
    # recover1()
    # click((100,100))
    # pyautogui.hscroll(-1000)
    # initcur()
    # p3 = [0.20638629283489096, 0.7566489361702128]
    # moveTo(p3[0], p3[1])
    # for i in range(10):
    #     # pyautogui.hscroll(-200)
    #     pyautogui.hscroll(-200)
    #     time.sleep(1)

    # click(0.02, 0.08)




