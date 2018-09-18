import cv2
from matplotlib import pyplot as plt

import numpy as np
import cmath
from disbackground import dback
from num import finnum
def findFrame1(form=0,whetherShow=False):
    # struct choose frame
    img = cv2.imread('rf\\scr.png',0)
    img = cv2.medianBlur(img,5)
    img1=cv2.imread('rf\\scr.png')
    if 1:
        ret, th2 = cv2.threshold(img, 169, 255, cv2.THRESH_TOZERO)
        ret, th2 = cv2.threshold(th2, 170, 255, cv2.THRESH_TOZERO_INV)
        ret, th2 = cv2.threshold(th2, 80, 255, cv2.THRESH_BINARY)
        if whetherShow:
            cv2.imshow('3',th2)
            cv2.waitKey(0)
        imgx, contours, hierarchy = cv2.findContours(th2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        ex_list=[]
        for cnt in contours:
            if cv2.contourArea(cnt)>300 and cv2.contourArea(cnt)<10000:
                [x, y, w, h] = cv2.boundingRect(cnt)
                ex_list.append([x+w/2,y+h/2])
        ex_list.sort(key=lambda x:x[1])
    ret,th1 = cv2.threshold(img,175,255,cv2.THRESH_TOZERO)
    ret,th1 = cv2.threshold(th1,180,255,cv2.THRESH_TOZERO_INV)
    ret,th1 = cv2.threshold(th1,80 ,255,cv2.THRESH_BINARY)
    imgx, contours, hierarchy = cv2.findContours(th1 ,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(contours)):
        [x1, y1, w1, h1] = cv2.boundingRect(contours[i])
        if cv2.contourArea(contours[i])>30000:
            [x1, y1, w1, h1] = cv2.boundingRect(contours[i])
            th1=cv2.rectangle(th1, (x1, y1), (x1 + w1, y1 + h1), (255, 255, 255),20)
            th1= cv2.line(th1, (int(x1+w1/2), y1), (int(x1+w1/2), y1+h1), (255, 255, 255), 5)

            break
    if whetherShow:
        plt.imshow(th1)
        plt.show()
    k=None
    imgx, contours, hierarchy = cv2.findContours(th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    for i in range(len(contours)):
        if cv2.contourArea(contours[i]) > 50000:
            k=i
            break
    if k==None:
        print('not found the frame1')
        local_list=[]
    else:
        local_list=[]
        for i in range(-1,-len(hierarchy[0]),-1):
            if hierarchy[0][i][3]==k and cv2.contourArea(contours[i])>500:
                [x1, y1, w1, h1] = cv2.boundingRect(contours[i])
                # img1 = cv2.drawContours(img1,[hull], 0, (0, 0,255), 3)
                if form ==0:
                    local_list.append([x1, y1, w1, h1])
                if form==1:
                    curImg=img1[y1:y1+h1,x1:x1+w1]
                    cv2.imwrite('rf\\temc.png',curImg)
                    cv2.rectangle(img1, (x1, y1), (x1 + w1, y1 + h1), (0, 0, 255), 1)
                    curImggray=cv2.cvtColor(curImg,cv2.COLOR_BGR2GRAY)
                    th2= cv2.adaptiveThreshold(curImggray, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                                                cv2.THRESH_BINARY, 11, 2)
                    curimgx, curcontours1, curhierarchy1 = cv2.findContours(th2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    curcontours1.sort(key=lambda x:cv2.boundingRect(x)[2]*cv2.boundingRect(x)[3],reverse=True)
                    # plt.imshow(curImggray)
                    # plt.show()
                    # # for cnt in curcontours1:
                    #     curImg = cv2.drawContours(th2, [cnt], 0, (0, 0, 0), 3)
                    # for i in range(len(curcontours1)):
                    #
                    #     hull1= cv2.convexHull(curcontours1[i])
                    #     # epsilon = 0.01 * cv2.arcLength(curcontours1[i], True)
                    #     # hull1 = cv2.approxPolyDP(curcontours1[i], epsilon, True)
                    #     if cv2.contourArea(hull1)<curImg.shape[0]*curImg.shape[1]*0.8 and cv2.pointPolygonTest(curcontours1[i],(int(w1/2),int(h1/2)),True)>-20:
                    #         # curImg = cv2.drawContours(curImg,[hull1], 0, (0,0,0),3)
                    #         [x, y, w, h] = cv2.boundingRect(curcontours1[i])
                    #         # cv2.rectangle(curImg, (x, y), (x + w, y + h), (0, 0, 255), 1)
                    #         break
                    rect=(0.1,0.04,0.9,0.96)
                    fimg,ju1=dback(curImg,form=2,rect=rect,whetherShow=False,dis=[178,233,254])
                    if ju1<0.1:
                        continue
                    local_list.append([[x1, y1, w1, h1],fimg])


                # findgoods(fimg)
        if form==0:
            local_list.sort(key=lambda x:(x[1]*10+x[0]))
            # for x in local_list:
            #     if x[2] > 150 or x[3] > 150:
            #         cv2.imwrite('rf\\temc.png',img1)
            #         print('is now')
        elif form==1:
            local_list.sort(key=lambda x:(x[0][1]*10+x[0][0]))

    return local_list,ex_list

            # print(contours)
            # print('\n')
# imgx, contours, hierarchy = cv2.findContours(th1 ,cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
# for x in hierarchy:
#     for y in x:
#         print(y)
def findFrame2(form=0,whetherShow=False):
    img = cv2.imread('rf\\scr.png', 0)
    # img = cv2.medianBlur(img, 5)
    img1 = cv2.imread('rf\\scr.png')
    ret, th1 = cv2.threshold(img, 240, 255, cv2.THRESH_TOZERO)
    ret, th1 = cv2.threshold(th1, 255, 255, cv2.THRESH_TOZERO_INV)
    ret, th1 = cv2.threshold(th1, 80, 255, cv2.THRESH_BINARY_INV)
    if whetherShow:
        plt.subplot(121)
        plt.imshow(img,'gray')
        plt.subplot(122)
        plt.imshow(th1,'gray')
        plt.show()

    imgx, contours, hierarchy = cv2.findContours(th1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    curth1=[]
    for i in range(len(contours)):
        if cv2.contourArea(contours[i])>23000 and cv2.contourArea(contours[i])<70000:
            [x,y,w,h] = cv2.boundingRect(contours[i])
            curth1=th1[y+5:y+h-5,x+5:x+w-2]
            img1=img1[y+5:y+h-5,x+5:x+w-2]
            img=img[y+5:y+h-5,x+5:x+w-2]
            cv2.drawContours(img1, contours, i, [0,0,0],3)
            break
    if len(curth1)==0:
        print('not found frame2')
        ret=[],0

    else:
        if form==0:
            imgx, curcontours, curhierarchy = cv2.findContours(curth1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            for cnt in curcontours:
                if cv2.contourArea(cnt) > 100 and cv2.contourArea(cnt) < 4000:
                    [x, y, w, h] = cv2.boundingRect(cnt)
                    timeImg = img[y:y + h, 100:-100]
                    timeImg = cv2.adaptiveThreshold(timeImg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                                                    cv2.THRESH_BINARY_INV, 5, 2)
                    time= finnum(timeImg, form=1)
                    break
            goodImg_list=[]
            for cnt in curcontours:
               if cv2.contourArea(cnt)>4000:
                    [x, y, w, h] = cv2.boundingRect(cnt)
                    curgoodImg=img[y+3:y+h-3, x+2:x + w-3]
                    curgoodImg1=img1[y+3:y+h-3, x+2:x + w-3]
                    cv2.imwrite('rf\\temc.png',curgoodImg1)
                    num=finnum(curgoodImg1,whetherShow=False)
                    if num==None:
                        continue
                    num=num%10
                    curgoodth1= cv2.adaptiveThreshold(curgoodImg,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                                cv2.THRESH_BINARY_INV,5,2)

                    imgx, curgoodcontours, curgoodhierarchy = cv2.findContours(curgoodth1, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    curgoodcontours.sort(key=lambda x:cv2.contourArea(cv2.convexHull(x)),reverse=True)
                    if len(curgoodcontours)<3:
                        continue
                    [x,y,w,h] = cv2.boundingRect(curgoodcontours[0])
                    rect=(x,y,x+w,y+h)
                    dbackimg,ju1=dback(curgoodImg1,form=2,rect=rect,whetherShow=False,dis=[218,234,240])

                    goodImg_list.append([dbackimg,num])
               # goodImg_list.sort(key=lambda x:(x[0][1]*10+x[0][0]) )
            ret=goodImg_list,time
        if form==1:

            timeImg=img[int(0.8*img.shape[0]):,int(0.2*img.shape[1]):int(0.8*img.shape[1])]
            timeImg = cv2.adaptiveThreshold(timeImg, 255, cv2.ADAPTIVE_THRESH_MEAN_C, cv2.THRESH_BINARY_INV, 5, 2)
            time=finnum(timeImg,form=1,whetherShow=False)
            ret=time

    return ret

def findFrame3(form=0,whetherShow=False):
    img = cv2.imread('rf\\scr.png', 0)
    # img = cv2.medianBlur(img, 5)

    img1 = cv2.imread('rf\\scr.png')
    ret, th1 = cv2.threshold(img, 239, 255, cv2.THRESH_TOZERO)
    ret, th1 = cv2.threshold(th1, 244, 255, cv2.THRESH_TOZERO_INV)
    ret, th1 = cv2.threshold(th1, 80, 255, cv2.THRESH_BINARY)
    imgx, contours, hierarchy = cv2.findContours(th1, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    proing_list=[]
    time=None
    if whetherShow:
        plt.subplot(121)
        plt.imshow(img,'gray')
        plt.subplot(122)
        plt.imshow(th1,'gray')
        plt.show()
    for i in range(len(contours)-1,-1,-1):
        if cv2.contourArea(contours[i])>5000 and cv2.contourArea(contours[i])<42000:
            [x,y,w,h] = cv2.boundingRect(contours[i])
            # curth1=th1[y+5:y+h-5,x+5:x+w-2]
            img2=img1[y:y+h,x:x+w]
            # img=img[y+5:y+h-5,x+5:x+w-2]
            cv2.drawContours(img1, contours, i, [0,0,0],3)
            dimg,ju1=dback(img2,form=2,dis=[178,233,254],rect=[0.08,0.08,0.92,0.92],whetherShow=False)
            if whetherShow:
                cv2.imshow("12",img1)
                cv2.waitKey(0)
            if ju1<0.2:
                if form==0:
                    proing_list.append([x+w/2,y+h/2])
                continue
            else:
                proing_list.append(dimg)
                if cv2.contourArea(contours[i])>8000:
                    timeImg=img1[y-30:y,x:x+w]
                    time=finnum(timeImg,form=2,whetherShow=False)
    return proing_list,time

def findFrame4(form=0,whetherShow=False):
    #ship
    img=cv2.imread('rf\\scr.png')
    if form==0:
        lo=find_colorblocks(sample='rf\\scr.png',form=22,whetherShow=False)
        img_list=[]
        for x in lo:
            curimg=img[x[1]:x[1]+x[3],x[0]:x[0]+x[2]]
            ju1=find_colorblocks(sample=curimg,form=23,whetherShow=False)
            ju1=len(ju1)>0
            a=finnum(curimg)
            if a==None:
                continue
            dimg,ratio=dback(curimg,form=2,dis=(192,243,255),rect=[0.15,0.12,0.85,0.9])
            if ratio>0.1:
                img_list.append([[x[0]+x[2]/2,x[1]+x[3]/2],dimg,a,ju1])
            else:
                img_list.append([0,dimg,a,ju1])

            if whetherShow:
                print(a,ju1)
                cv2.imshow('1',dimg)
                cv2.waitKey(0)
        ret=img_list
    elif form==1:
        img_list=[]
        lo=find_colorblocks(sample='rf\\scr.png',form=24,whetherShow=False)
        for x in lo:
            curimg = img[x[1]:x[1] + x[3], x[0]:x[0] + x[2]]
            dimg, ratio = dback(curimg, form=2, dis=(157, 213, 244), rect=[0.13, 0.12, 0.87, 0.9])
            img_list.append(dimg)
            if whetherShow:
                cv2.imshow('1',dimg)
                cv2.waitKey(0)

        ret=img_list
    return ret

def findCropland(path='rf\\scr.png',whetherShow=False):
    frame = cv2.imread(path,-1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # img = cv2.medianBlur(img, 5)
    # ret, th1 = cv2.threshold(img, 100, 255, cv2.THRESH_TOZERO)
    # ret, th1 = cv2.threshold(th1, 120, 255, cv2.THRESH_TOZERO_INV)
    # ret, th1 = cv2.threshold(th1, 80, 255, cv2.THRESH_BINARY)
    # img1 = cv2.imread(path, 1)
    lower_blue = np.array([10, 180, 130])
    upper_blue = np.array([20 , 186, 180])
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    res = cv2.bitwise_and(frame, frame, mask=mask)
    res = cv2.cvtColor(res, cv2.COLOR_BGR2HSV)
    # plt.subplot(221)
    # plt.imshow(frame)
    # plt.subplot(222)
    # plt.imshow(hsv)
    # plt.subplot(223)
    # plt.imshow(res)
    # cv2.waitKey(0)
    # plt.show()
    imgx, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    wn=hn=None
    for cnt in contours:
        if cv2.arcLength(cnt,True)>500:
            hull = cv2.convexHull(cnt)
            hull1=hull.reshape(-1,2)
            hull1=hull1.tolist()
            hull1.sort(key=lambda x:0.5*x[0]+x[1],)
            a1=0.5*hull1[0][0]+hull1[0][1]
            a2=0.5*hull1[-1][0]+hull1[-1][1]
            hull1.sort(key=lambda x:-0.5*x[0]+x[1])
            b1 = -0.5*hull1[0][0] + hull1[0][1]
            b2 = -0.5*hull1[-1][0] + hull1[-1][1]
            p1=[int((a1-b1)),int((a1+b1)/2)]
            p2=[int((a1-b2)),int((a1+b2)/2)]
            p4=[int((a2-b1)),int((a2+b1)/2)]
            p3=[int((a2-b2)),int((a2+b2)/2)]
            if p2[0]<0:
                ret=0
            else:
                pts = np.array([p1, p2, p3, p4], np.int32)
                pts = pts.reshape((-1, 1, 2))
                cv2.polylines(frame, [pts], True, (255, 0, 0),2)
                line1=np.reshape(np.array([p2,p3],np.int32),(-1,1,2))
                line2=np.reshape(np.array([p3,p4],np.int32),(-1,1,2))
                w1=cv2.arcLength(line1,True)/2
                h1=cv2.arcLength(line2,True)/2
                a= 0.03786980393655481*frame.shape[0]
                wn=int(w1/a+0.2)
                hn=int(h1/a+0.2)
            break
    if wn==None:
        print('not founded crop')
        ret=None,None
    else:
        an1=cmath.atan(0.5).real
        block_list=[[] for x in range(wn)]
        for i in range(wn-1,-1,-1):
            for j in range(hn-1,-1,-1):
                curw=i*a
                curh=j*a
                cur_point=[int(p3[0]-(curw*cmath.cos(an1).real-curh*cmath.cos(an1).real)),int(p3[1]-(curw+curh)*cmath.sin(an1).real)]
                cur_point[1]=cur_point[1]-int(a*cmath.sin(an1).real)
                block_list[-i-1].append(cur_point)
                cv2.circle(frame,(cur_point[0],cur_point[1]),5,[0,0,0],0)
        if whetherShow:
            cv2.imshow('1', frame)
            cv2.waitKey(0)
        ret=block_list,mask
    return ret
        # if cv2.arcLength(cnt,True)>500:
        #     epsilon = 0.1 * cv2.arcLength(cnt, True)
        #     approx = cv2.approxPolyDP(cnt, epsilon, True)
        #
        #     hull=cv2.convexHull(cnt)
        #     ju=0
        #     for i in range(len(hull)):
        #         x1=hull[i][0][0]
        #         y1=hull[i][0][1]
        #         if i==len(hull)-1:
        #             x2=hull[0][0][0]
        #             y2= hull[0][0][1]
        #         else:
        #             x2 = hull[i+1][0][0]
        #             y2 = hull[i+1][0][1]
        #         if x2-x1!=0:
        #             k=(y2-y1)/(x2-x1)
        #         else:k=10
        #         if abs(abs(k)/0.5-1)<0.2:
        #             ju+=1
        #             cv2.line(img1,(x1,y1),(x2,y2), (255, 255, 255), 4)
        #     if ju>1:
        #         img1 = cv2.drawContours(img1, [cnt], 0, (0, 255, 255), 3)
        #         img1 = cv2.drawContours(img1, [hull], 0, (0, 0, 0), 3)
        #     else:
        #         continue
        #
        #     cv2.imshow('1',img1)
        #     cv2.waitKey()

def find_colorblocks(form,sample='rf\\scr.png',whetherShow=False):
    rect=cv2.imread('rf\\scr.png').shape[:2]
    S=rect[0]*rect[1]
    if type(sample)==str:
        frame = cv2.imread(sample)
    else:
        frame=sample
    # Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # define range of blue color in HSV
    if form==0:
        lower_blue = np.array([102, 68,90])
        upper_blue = np.array([103,72, 108])
        k=-0.5
        ju1=200*S/1935360
        ju2=1.2

    elif form==1:
        lower_blue = np.array([23,220,238])
        upper_blue = np.array([25,235,242])
        k=-0.45
        ju1=15*S/1935360
        ju2=0.2
    elif form==2:
        lower_blue = np.array([4,66,130])
        upper_blue = np.array([5,69,163])
        k=-0.1
        ju1=600*S/1935360
        ju2=0.5
    elif form==3:
        lower_blue = np.array([11, 150, 196])
        upper_blue = np.array([13, 160, 223])
        k=0.4
        ju1=50*S/1935360
        ju2=1
    elif form == 4:
        lower_blue = np.array([6, 64,92])
        upper_blue = np.array([8, 67, 100])
        k = -0.3
        ju1 = 300*S/1935360
        ju2 = 1
    elif form==-1:
        lower_blue = np.array([15,142,198])
        upper_blue = np.array([16, 156, 206])
        k=-0.15
        ju1=100*S/1935360
        ju2=0.3
    elif form==-2:
        hsv[0:150,:]=[0,0,0]
        hsv[630:,:]=[0,0,0]
        hsv[:,1100:]=[0,0,0]
        lower_blue = np.array([15,142,215])
        upper_blue = np.array([17, 144, 226])
        k=-0.32
        ju1=1000*S/1935360
        ju2=2
    elif form == -3:
        #truck
        lower_blue = np.array([22,60, 254])
        upper_blue = np.array([30,73, 255])
        k = -5
        ju1 = 1000*S/1935360
        ju2 = 3
    elif form == -4:
        # gray
        hsv[0:150,0:300]=[0,0,0]
        lower_blue = np.array([0, 0, 100])
        upper_blue = np.array([0, 0, 205])
        k = -5
        ju1 = 800*S/1935360
        ju2 = 3
    elif form == -11:
        # my farm
        lower_blue = np.array([0, 0, 255])
        upper_blue = np.array([0, 0, 255])
        k = -5
        ju1 = 3300*S/1935360
        ju2 = 3
    elif form==-12:
        #struct frame
        lower_blue = np.array([20,49, 239])
        upper_blue = np.array([20,49, 239])
        k = -5
        ju1 = 20000*S/1935360
        ju2 = 3

    elif form==11:
        #shopping trolley
        lower_blue = np.array([14,181,221])
        upper_blue = np.array([14,183,221])
        k=0.2
        ju1=3100*S/1935360
        ju2=1
    elif form==12:
        #money bubble
        lower_blue = np.array([92,42,230])
        upper_blue = np.array([92,70,242])
        k=0
        ju1=2000*S/1935360
        ju2=1
    elif form==13:
        # huolan
        lower_blue = np.array([15, 156, 211])
        upper_blue = np.array([15, 168, 241])
        k = 0.2
        ju1 = 4000 * S / 1935360
        ju2 = 1
    elif form == 22:
        #ship frame
        lower_blue = np.array([8, 183, 213])
        upper_blue = np.array([10, 190, 223])
        k = -0.5
        ju1 = 1100*S/1935360
        ju2 = 3
    elif form == 23:
        #ship green tick
        lower_blue = np.array([55, 230, 190])
        upper_blue = np.array([56, 255, 211])
        k = -0.5
        ju1 = 30*S/1935360
        ju2 = 3
    elif form == 24:
        #ship frame noar
        hsv[0:260,:]=[0,0,0]
        lower_blue = np.array([19, 91, 244])
        upper_blue = np.array([19, 91, 244])
        k = -0.5
        ju1 = 1000*S/1935360
        ju2 = 3
    # # Threshold the HSV image to get only blue colors
    mask = cv2.inRange(hsv, lower_blue, upper_blue)
    if form==22 or form==23  or form==11or form==12 or form==-2 or form==13 or form==-3:
        kernel = np.ones((5, 5), np.uint8)
        mask= cv2.dilate(mask, kernel, iterations=1)
    imgx, contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    lo_list=[]
    res = cv2.bitwise_and(frame, frame, mask=mask)
    res = cv2.cvtColor(res, cv2.COLOR_BGR2HSV)
    b, g, r = cv2.split(frame)
    frame = cv2.merge([r, g, b])
    if whetherShow:
        plt.subplot(221)
        plt.imshow(frame)
        plt.subplot(222)
        plt.imshow(hsv)
        plt.subplot(223)
        plt.imshow(mask)
        plt.show()
    # img = mask
    # kernel = np.ones((5, 5), np.uint8)
    # erosion = cv2.erode(img, kernel, iterations=1)
    # closing = cv2.morphologyEx(img, cv2.MORPH_CLOSE, kernel)
    # kernel = np.ones((5, 5), np.uint8)
    # dilation = cv2.dilate(erosion, kernel, iterations=2)
    # cv2.imshow('1',dilation)
    # cv2.waitKey(0)
    for cnt in contours:
        if cv2.contourArea(cnt)>ju1 :
            [vx, vy, x, y] = cv2.fitLine(cnt, cv2.DIST_L2, 0, 0.01, 0.01)
            if whetherShow:
                print(cv2.contourArea(cnt),cmath.atan(vy/vx).real,cmath.atan(k).real,vy/vx,k)

            if abs(cmath.atan(vy/vx).real-cmath.atan(k).real)>ju2:
                continue
            [x, y, w, h] = cv2.boundingRect(cnt)

            if form == -3:
                cntlist=cnt.tolist()
                cntlist .sort(key=lambda x: (-x[0][1]+x[0][0]), reverse=True)
                [x, y, w, h]=[cntlist[0][0][0],cntlist[0][0][1],10,10 ]
            lo_list.append([x,y,w,h])

    if whetherShow:
        for r in lo_list:
            [x,y,w,h]=r
            cv2.rectangle(frame, (x, y), (x + w, y + h), [0, 0, 255], 2)
            cv2.imshow('block', frame)
            cv2.waitKey(0)
    ret=lo_list
    if form == -3:
        lo_list.sort(key=lambda x: x[1], reverse=True)
        print(lo_list)
        ret=lo_list

    if form == -2:
        lo_list.sort(key=lambda x: x[0], reverse=False)
        if len(lo_list)>0:
            rect=lo_list[0]
            x0 = rect[0]
            y0=rect[1]+rect[3]
            rect = cv2.imread('rf\\scr.png').shape[:2]
            nimg=frame[y0-int(230*rect[0]/1080):y0-int(110*rect[0]/1080),x0+int(100*rect[0]/1080):x0+int(300*rect[0]/1080)]
            n=finnum(nimg,form=0,whetherShow=False)
            ret=lo_list,n
        else:
            ret=[],0
    if form == 24:
        ret=lo_list[0:3]
    return ret

    # Bitwise-AND mask and original image

def getedge():
    for i1 in range(1,19):
        for j1 in range (5):
            print(i1,j1)
            img1 = cv2.imread('iby\\plants\\plants'+str(i1)+'r'+str(j1)+'.png')
            img = cv2.imread('iby\\plants\\plants'+str(i1)+'r'+str(j1)+'.png',0)
            img = cv2.medianBlur(img,5)
            a1=img>100
            a2=img<130
            # print(a)
            b=np.where(a1==a2,True,False)
            img=np.where(b,100,img)
            # img[75:110, 65:110] = 100
            if img[0,0]!=100:
                img[0:10,:]=100
                img[-10:,:]=100

            ret,th1 = cv2.threshold(img,99,255,cv2.THRESH_TOZERO)
            ret,th1 = cv2.threshold(th1,101,255,cv2.THRESH_TOZERO_INV)
            ret,th1 = cv2.threshold(th1,80 ,255,cv2.THRESH_BINARY_INV)

            th2 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_MEAN_C,\
                        cv2.THRESH_BINARY_INV,5,2)
            th3 = cv2.adaptiveThreshold(img,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,\
                        cv2.THRESH_BINARY_INV,3,5)

            titles = ['Original Image', 'Global Thresholding (v = 127)',
                        'Adaptive Mean Thresholding', 'Adaptive Gaussian Thresholding']
            images = [img, th1, th2, th3]
            curimgx, curcontours1, curhierarchy1 = cv2.findContours(th2,  cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            curcontours1.sort(key=lambda x:cv2.arcLength(x,True),reverse=True)
            hull1 = cv2.convexHull(curcontours1[0])
            hull2 = cv2.convexHull(curcontours1[1])
            newmask1= np.zeros(img.shape[:2], np.uint8)
            # cv2.drawContours(newmask1, [hull1], 0, 255, -1)
            # cv2.drawContours(newmask1, [hull2], 0, 255, -1)


            # newmask = np.zeros(img.shape[:2], np.uint8)
            # for cnt in curcontours1:
            #     cv2.drawContours(newmask, [cnt], 0, 255,3)
            curimgx, curcontours2, curhierarchy2 = cv2.findContours(th2,  cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
            # plt.subplot(121)
            # plt.imshow( newmask)
            newmask = np.zeros(img.shape[:2], np.uint8)
            for i in range(len(curcontours2)):
                    if cv2.contourArea(curcontours2[i])>5:
                        1
                        cv2.drawContours(newmask1, curcontours2, i, 200,-1)
                        # cv2.drawContours(newmask1, curcontours2, i, 255, 1)
                    # if cv2.contourArea(curcontours2[i])>200:
                    #     cv2.drawContours(newmask, curcontours2, i, 0, 4)

            cv2.imshow('2',newmask1)
            cv2.waitKey(0)
            kernel = np.ones((5, 5), np.uint8)
            erosion = cv2.erode(img, kernel, iterations=1)
            cv2.imshow('2',erosion)
            cv2.waitKey(0)
            img2,ju1=dback(img1,form=1,whetherShow=False,newmask=newmask1)
            img1=cv2.imread('iby\\plants\\plants'+str(i1)+'r'+str(j1)+'bg.png')
            cv2.imshow('1',img1)
            cv2.imshow('2',img2)
            key=cv2.waitKey(0)
            if key!=27:
                cv2.imwrite('iby\\plants\\plants'+str(i1)+'r'+str(j1)+'bg.png',img2)
            # cv2.drawContours(img1, [hull1], 0, (0,0, 0), 2)
            # cv2.imshow('1',newmask)
            # cv2.waitKey(0)

            # help(cv2.convexHull)
            # for i in range(4):
            #     plt.subplot(2,2,i+1),plt.imshow(images[i],'gray')
            #     plt.title(titles[i])
            #     plt.xticks([]),plt.yticks([])
            # plt.show()
if __name__=="__main__":
    # product_list, ex_list = findFrame1(form=1,whetherShow=True)
    # print(len(product_list))
    # curgood = findgoods(product_list[0][1],whetherShow=True)[1]
    # for i in range(len(product_list)):
    # findFrame3(form=0,whetherShow=True)

    # findCropland(whetherShow=True)
    # lo=find_colorblocks(sample='rf\\scr.png',form=24,whetherShow=True)
    # a=findFrame4(1,whetherShow=True)
    # print(len(a[0]))
    # print(a[0][0])
    # cv2.imshow('1',a[1])
    # cv2.waitKey(0)
    rect2 = find_colorblocks(form=-4 ,sample='rf\\scr.png',whetherShow=True)
