import cv2
from scr import getsc,getrect
import numpy as np,sys
import pickle
import mouse1
from siftmatch import detect,Staticpt
from matplotlib import pyplot as plt
import colorfind
def finblock(truck):
    origin=truck.getOrigin()
    getsc(1)
    spt = Staticpt(cv2.imread('rf\\scr.png'))
    for i in range(6,len(truck.struct_list)):
        x=truck.struct_list[i]
        lo=detect(test=x.img,several=True,static=True,whetherShow=False,staticpt1=spt)

        # if len(lo)==0:
        #     lo=[detectinpano(x.img) ]
        #     print(lo,x.path)
        for z in lo:
            # if z[0]<200:
            #     continue
            x.relLocation.append([z[0]-origin[0],z[1]-origin[1]])
            for j in range(len(x.relLocation)-1):
                x2=x.relLocation[j]
                clo=[z[0]-origin[0],z[1]-origin[1]]
                if abs(clo[0]-x2[0])<50 and abs(clo[1]-x2[1])<50:
                    x.relLocation.pop(-1)
                    break
    for i in range(1,len(truck.public_list)-1):
        x = truck.public_list[i]
        lo = detect(test=x.img, several=True, static=True, whetherShow=False, staticpt1=spt)

        # if len(lo)==0:
        #     lo=[detectinpano(x.img) ]
        #     print(lo,x.path)
        for z in lo:
            # if z[0] < 200:
            #     continue
            x.relLocation.append([z[0] - origin[0], z[1] - origin[1]])
            for j in range(len(x.relLocation) - 1):
                x2 = x.relLocation[j]
                clo = [z[0] - origin[0], z[1] - origin[1]]
                if abs(clo[0] - x2[0]) < 50 and abs(clo[1] - x2[1]) < 50:
                    x.relLocation.pop(-1)
                    break
        truck.public_list[4].relLocation=[[-75*getrect()[1]/1792,750*getrect()[0]/1080]]
        truck.public_list[0].relLocation=[[0,0]]

    for i in range(5):
        curlist=colorfind.find_colorblocks(form=i,whetherShow=False)
        for x in curlist:
            clo=[x[0]+x[2]-origin[0],x[1]+x[3]+40-origin[1]]
            truck.struct_list[i+1].relLocation.append([clo[0],clo[1]])
            for i1 in range(len(truck.struct_list[i+1].relLocation)-1):
                x1=truck.struct_list[i+1].relLocation[i1]
                if abs(clo[0]-x1[0])<50 and abs(clo[1]-x1[1])<50:
                    truck.struct_list[i + 1].relLocation.pop(-1)
                    break
        truck.struct_list[i + 1].relLocation.sort(key=lambda x:x[0]+x[1])
    if len(truck.struct_list[0].relLocation)==0:
        block_list=colorfind.findCropland()[0]
        if block_list!=None:
            for i in range(len(block_list)):
                for j in range(len(block_list[0])):
                    block_list[i][j][0]= block_list[i][j][0]-origin[0]
                    block_list[i][j][1]= block_list[i][j][1]-origin[1]
            # truck.struct_list[0].relLocation=[[block_list[0][0][0]-origin[0],block_list[0][0][1]-origin[1]]]
            truck.struct_list[0].relLocation =block_list
    return origin

def getpanorama(truck,whetherShow=False):
    def dbimg():
        img=cv2.imread('rf\\scr.png')
        img = np.where(truck.scrmask == 1, img, 255)
        return img
    for x in truck.struct_list:
        x.relLocation=[]
    for x in  truck.public_list:
        x.relLocation=[]
    stitcher = cv2.createStitcher(False)

    mouse1.recover1()
    mouse1.initcur()
    origin=finblock(truck)
    img1=dbimg()
    origin1=origin
    # img1.reshape(int(img1.shape[0]*0.5),int(img1.shape[1]*0.5))
    # getsc(1)
    # img11=dbimg()
    # img1 = stitcher.stitch((img1,img11))[1]
    mouse1.swipeTo((0.5,0.5),(0.15,0.205))
    finblock(truck)
    img2=dbimg()
    # cv2.imshow('1',img2)
    # cv2.waitKey(0)
    # #
    curimg = stitcher.stitch((img1,img2))[1]
    #
    # mouse1.swipeTo((0.5,0.5),(0.15,0.205))
    # getsc(1)
    # img3=dbimg()
    # finblock(truck)

    # finblock()
    # img3.reshape(int(img1.shape[0]*0.5),int(img1.shape[1]*0.5))
    # panoimg = stitcher.stitch((img3,curimg))[1]
    # if whetherShow:
    panoimg=curimg
    truck.panoimg=panoimg.copy()
    for i in range(len(truck.struct_list)):
        x = truck.struct_list[i]
    origin = origin1
    panoimg = cv2.circle(panoimg, (origin[0], origin[1]), 5, (0, 255, 0), 3)
    for i in range(6, len(truck.struct_list)):
        y1 = truck.struct_list[i].relLocation
        truck.struct_list[i].num=len(y1)
        for y in y1:
            panoimg = cv2.circle(panoimg, (y[0] + origin[0], y[1] + origin[1]), 18, (0, 255, 0), 3)
    for i in range(1, len(truck.public_list)-1):
        y1 = truck.public_list[i].relLocation
        truck.public_list[i].num=len(y1)
        for y in y1:
            panoimg = cv2.circle(panoimg, (y[0] + origin[0], y[1] + origin[1]), 18, (0, 255, 0), 3)
    for i in range(1, 6):
        y1 = truck.struct_list[i].relLocation
        truck.struct_list[i].num=len(y1)
        for y in y1:
            panoimg = cv2.circle(panoimg, (y[0] + origin[0], y[1] + origin[1]), 18, (0, 0, 255), 3)
    for x in truck.struct_list[0].relLocation:
        for y in x:
            panoimg = cv2.circle(panoimg, (y[0]+origin[0],y[1]+origin[1]), 2,(255, 255, 255), 2)
    b, g, r = cv2.split(panoimg)
    panoimg1 = cv2.merge([r, g, b])
    if whetherShow:
        plt.imshow(panoimg1)
        plt.show()
        for x in truck.public_list:
            print(x.relLocation)
        for x in truck.struct_list:
            print(x.relLocation)
    cv2.imwrite('rf\\panorama.png',panoimg)
    return panoimg, origin1

def showStruct(panoimg,lo,origin):
    panoimg=panoimg.copy()
    if len(np.array(lo).shape)==3:
        for x in lo:
            for y in x:

                panoimg = cv2.circle(panoimg, (y[0] + int(origin[0]), y[1] + int(origin[1])), 2, (255, 255, 255), 2)

    else:

        for i in range(len(lo)):
            panoimg = cv2.circle(panoimg, (lo[i][0] + int(origin[0]), lo[i][1] + int(origin[1])), 18, (0, 255, 0), 3)
    return panoimg
if __name__=="__main__":
    f = open('rf\\goods.txt', 'rb')
    list1 = pickle.load(f)
    # truck.struct_list=list1[1]
    # truck.goods_list=list1[0]
    # truck.public_list=list1[2]
    # for x in truck.struct_list:
    #     x.relLocation=[]
    # panoimg=cv2.imread('rf\\panorama.png')
    # panoimg,origin1=getpanorama(whetherShow=True)
    # f = open('rf\\goods.txt', 'wb')
    # pickle.dump([truck.goods_list, truck.struct_list,truck.public_list], f, 0)
    # f.close()
    for x in list1[1]:
        print(x.relLocation)

