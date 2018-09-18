import cv2
import numpy as np
import time
import colorfind
import mouse1
# for i in range (1,19):
#     for j in range (5):
#         img = cv2.imread('iby\\goods\\goods'+str(i)+'r'+str(j)+'.png',0)
#         edges = cv2.Canny(img,100,200)
#
#         plt.subplot(121),plt.imshow(img,cmap = 'gray')
#         plt.title('Original Image'), plt.xticks([]), plt.yticks([])
#         plt.subplot(122),plt.imshow(edges,cmap = 'gray')
#         plt.title('Edge Image'), plt.xticks([]), plt.yticks([])
#
start=time.time()
def T(s=-1):
    ret=time.time()-start
    if s!=-1:
        s2=str(time.time()-start)
        s=str(s)
        print(s+':'+s2)
    return ret
#       plt.show()
def candySearch(form=0,whetherShow=False):
    rect=cv2.imread('rf\\scr.png').shape[:2]
    S=rect[0]*rect[1]
    frame = cv2.imread('rf\\scr.png')
    if form==0:
        frame = frame[int(0.35 * frame.shape[0]):int(0.8 * frame.shape[0]), int(0.22 *frame.shape[1]):int(0.79 * frame.shape[1])]
        # Convert BGR to HSV
        po1=colorfind.find_colorblocks(sample=frame,form=13,whetherShow=False)
        ratio=0.4
        img_list=[]
        for x in po1:
            x1=int(x[2]/5)
            if x[1]-int(0.83 *x1)>0:
                for i in range(5):
                    img=frame[x[1]-int(0.83*x1):x[1],x[0]+i*x1:x[0]+(1+i)*x1,]
                    edges = cv2.Canny(img, 110, 200)
                    ratio1 = (np.sum(np.reshape(edges, (1, -1))) / (edges.size * 255))
                    if ratio1<0.02:
                        ratio=0
                    else:
                        img_list.append(img)
                    if whetherShow:
                        cv2.imshow('2',img)
                        cv2.waitKey(0)
    elif form==1:
        frame1=frame[int(0.25*frame.shape[0]):int(0.85*frame.shape[0]),int(0.22*frame.shape[1]):int(0.56*frame.shape[1])]
        # Convert BGR to HSV
        po1=colorfind.find_colorblocks(sample=frame1,form=13)
        ratio=0.4
        img_list=[]
        for x in po1:
            x1=int(x[2]/3)
            if x[1]-int(0.85 *x1)>0:
                for i in range(3):
                    img=frame1[x[1]-int(0.85*x1):x[1],x[0]+i*x1:x[0]+(1+i)*x1,]
                    edges = cv2.Canny(img, 110, 200)
                    ratio1 = (np.sum(np.reshape(edges, (1, -1))) / (edges.size * 255))
                    if ratio1<0.02:
                        ratio=0
                    else:
                        img_list.append([img,[int(0.22*frame.shape[1])+x[0]+int((i+1/2)*x1),int(0.25*frame.shape[0])+x[1]-int(0.85*x1/2)]])

                    if whetherShow:
                        cv2.imshow('2',img)
                        cv2.waitKey(0)

    return img_list,ratio


def candySearch1(form=0,whetherShow=False):
    img2= cv2.imread('rf\\scr.png')
    if form==0:
        img1=img2[int(0.35*img2.shape[0]):int(0.8*img2.shape[0]),int(0.23*img2.shape[1]):int(0.79*img2.shape[1])]
        img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(img, 110, 200)
        lines = cv2.HoughLines(edges, 0.1, np.pi / 180,100,)
        help(cv2.HoughLines)
        cv2.imshow('3',img)
        cv2.waitKey(0)
    elif form==1:
        img1=img2[int(0.3*img2.shape[0]):int(0.85*img2.shape[0]),int(0.2*img2.shape[1]):int(0.62*img2.shape[1])]
        img = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        edges = cv2.Canny(img, 120, 200)
        lines = cv2.HoughLines(edges, 1, np.pi / 180, 100,min_theta=500)

    for i in range(len(lines)):
        for rho,theta in lines[i]:
            a = np.cos(theta)
            b = np.sin(theta)
            x0 = a*rho
            y0 = b*rho
            x1 = int(x0 + 1000*(-b))
            y1 = int(y0 + 1000*(a))
            x2 = int(x0 - 1000*(-b))
            y2 = int(y0 - 1000*(a))

            cv2.line(edges,(x1,y1),(x2,y2),(0,0,0),2)
    cv2.imshow('3',edges)
    cv2.waitKey(0)
    kernel = np.ones((5,5),np.uint8)
    edges= cv2.dilate(edges,kernel,iterations = 4)
    imgx, contours, hierarchy = cv2.findContours(edges ,cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    list1=[]
    # plt.imshow(edges)
    # plt.show()
    if form ==0:
        juimg=edges[int(0.68*img.shape[0]):,int(0.85*img.shape[1]):]
    elif form==1:
        juimg = edges[int(0.65 * img.shape[0]):, int(0.65 * img.shape[1]):]

    ratio=(np.sum(np.reshape(juimg,(1,-1)))/(juimg.size*255))
    for cnt in contours:
        [x, y, w, h] = cv2.boundingRect(cnt)
        if w*h>5000:
            list1.append([x, y, w, h])
            # if whetherShow:
            #     cv2.rectangle(img, (x, y), (x + w, y + h), [0, 0, 255], 2)
            #     cv2.imshow('12',img)
            #     cv2.waitKey(0)
    list1.sort(key=lambda x:x[3])
    i=0
    while i<len(list1):
        if list1[0][3]<0.85*list1[-1][3]:
            if list1[0][1]>20 and list1[0][1]+list1[0][3]<edges.shape[0]-20:
                list1[0][3]+=20
                list1[0][2]+=20

            else:
                list1.pop(0)
        else:break
    if whetherShow:
        for cnt in list1:
            [x, y, w, h] = cnt
            cv2.rectangle(img, (x, y), (x + w, y + h), [0, 0, 255], 2)
            cv2.imshow('12', img)
            cv2.waitKey(0)
    img_list=[]
    for x in list1:
        if form==0:
            img_list.append(img1[x[1]:x[1]+x[3],x[0]:x[0]+x[2]])
        elif form==1:
            img_list.append([img1[x[1]:x[1]+x[3],x[0]:x[0]+x[2]],[x[0]+int(0.2*img2.shape[1])+x[2]/2,x[1]+x[3]/2+int(0.3*img2.shape[0])]])
    return img_list,ratio
if __name__=="__main__":

    print(time.time())

    a=candySearch(whetherShow=True
                  ,form=1)
    print(a[1])
    print(time.time())



