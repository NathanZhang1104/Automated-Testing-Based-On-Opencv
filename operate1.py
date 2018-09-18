import time
import os
import cv2
import numpy as np
import pickle
import manage
from scr import getsc,scrpart
from mouse1 import dragTo,moveTo,click,mouseUp,mouseDown,position,initcur,recover1
from siftmatch import detect
from coloredage import findFrame1,findFrame2,findFrame3,findCropland,find_colorblocks
from num import finnum
from findgoods import findgoods
from panorama import getpanorama
from disbackground import dback

def first_learn():

    def learn_struct():
        # manage.struct_list[0].product_list = []
        block_list, mask = findCropland()
        cropland = manage.Cropland(num=np.array(block_list).size)
        manage.truck.struct_list.append(cropland)
        lolist = find_colorblocks(form=0)
        farmji = manage.Farm(num=len(lolist))
        manage.truck.struct_list.append(farmji)
        lolist = find_colorblocks(form=1)
        farmniu = manage.Farm(num=len(lolist))
        manage.truck.struct_list.append(farmniu)
        lolist = find_colorblocks(form=2)
        farmzhu = manage.Farm(num=len(lolist))
        manage.truck.struct_list.append(farmzhu)

        lolist = find_colorblocks(form=3)
        farmyang = manage.Farm(num=len(lolist))
        manage.truck.struct_list.append(farmyang)

        lolist = find_colorblocks(form=4)
        farmshan = manage.Farm(num=len(lolist))
        manage.truck.struct_list.append(farmshan)

        huocang = manage.Cang(path='iby\\struct\\0s2_huocang.jpg', capacity=325)
        liangcang = manage.Cang(path='iby\\struct\\0s3_liangcang.jpg', capacity=325)
        sale=manage.Sale()
        manage.truck.public_list.append(huocang)
        manage.truck.public_list.append(liangcang)
        manage.truck.public_list.append(sale)
        for i in range(1, 5):
            for j in range(4):
                if i == 4 and j == 2:
                    break
                structscur = manage.Struct(num=1, path='iby\\struct\\struct' + str(i) + 'r' + str(j) + '.png')
                manage.truck.struct_list.append(structscur)
    def learn_goods():
        rootdir = 'iby\\goods'
        list1= os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
        list1.sort(key=lambda x: int(x[6].isdigit()) * 10 + int(x[5]))
        for x in list1:
            if x[-4:]=='.png' and x[-6:-4]!='bg':
                curgood=manage.Goods('iby\\goods\\'+x,0)
                manage.truck.goods_list.append(curgood)
        manage.public_list[1].getStatic()
        rootdir = 'iby\\plants'
        list2 = os.listdir(rootdir)  # 列出文件夹下所有的目录与文件
        list2.sort(key=lambda x: int(x[7].isdigit()) * 10 + int(x[6]))
        for x in list2:
            if x[-4:]=='.png' and x[-6:-4]!='bg':
                curgood=manage.Goods('iby\\plants\\'+x,0)
                manage.goods_list.append(curgood)
        manage.truck.public_list[2].getStatic()

    recover1(form=1)
    initcur()
    getsc()
    learn_struct()
    getpanorama(whetherShow=False)
    f=open('rf\\Class.txt','wb')
    pickle.dump([manage.truck.goods_list,manage.truck.struct_list,manage.truck.public_list],f,0)
    f.close()
    learn_goods()
    # learn_plants()
def second_learn():
    # recover1()
    # initcur()
    getsc()
    def getInformation(product_list,struct,proing_list):
        for i in range(len(product_list)):
            curgood=findgoods(product_list[i][1],whetherShow=False)[1]
            product_list[i][1]=curgood
            moveTo(int(product_list[i][0][0]+product_list[i][0][2]/2),int(product_list[i][0][1]+product_list[i][0][3]/2))
            mouseDown()
            getsc()
            product_list[i][0]=10*int(len(struct.product_list)/6)+i
            need_list,time1=findFrame2()
            if need_list==2:
                need_list, time1 = findFrame2()
            product_list[i].append(time1)
            for i in range(len(need_list)):
                need_list[i][0]=findgoods(need_list[i][0],whetherShow=False)[1]
            if manage.truck.struct_list.index(struct)==7:
                product_num=3
            else:
                product_num=1
            curgood.get_information(struct,need_list,time1,product_num)
            mouseUp()
        struct.get_information(product_list)
        # proing_list, proingtime = findFrame3()p
        # if len(proing_list) > 0:
        for i in range(len(proing_list)):
            if len(proing_list[i])==2:
                continue
            proing_list[i] = [findgoods(proing_list[i])[1]]
            proing_list[i].append(proing_list[i][0].product_time)
            struct.proing_list.append(proing_list[i])
        print(proing_list)


    for i in range(6,len(manage.truck.struct_list)):
        # if manage.struct_list[i].path!='iby\\struct\\struct2r1.png':
        #     continue
        manage.truck.struct_list[i].proing_list=[]
        manage.truck.struct_list[i].product_list=[]
        recover1()
        product_list, ex_list,proing_list=manage.truck.struct_list[i].findlo()
        # if po1==None:
        #     print(manage.struct_list[i].path)
        #     continue
        product_list, ex_list=findFrame1(form=1)
        getInformation(product_list,manage.truck.struct_list[i],proing_list)
        for y in ex_list:
            moveTo(y[0],y[1])
            click()
            getsc(sleep=0.5)
            product_list, ex_list1 = findFrame1(form=1)
            getInformation(product_list,manage.truck.struct_list[i],proing_list)

def third_learn():
    if 1:
        manage.truck.struct_list[1].product_list=[[0,manage.truck.goods_list[18],5.0]]
        manage.truck.goods_list[18].get_information(manage.truck.struct_list[1],[[manage.truck.goods_list[24],1]],5.0,product_num=1,)
        manage.truck.struct_list[2].product_list=[[0,manage.truck.goods_list[66],20.0]]
        manage.truck.goods_list[66].get_information(manage.truck.struct_list[2],[[manage.truck.goods_list[65],1]],20.0,product_num=1,)
        manage.truck.struct_list[3].product_list=[[0,manage.truck.goods_list[21],60.0]]
        manage.truck.goods_list[21].get_information(manage.truck.struct_list[3],[[manage.truck.goods_list[20],1]],60.0,product_num=1,)
        manage.truck.struct_list[4].product_list=[[0,manage.truck.goods_list[33],360.0]]
        manage.truck.goods_list[33].get_information(manage.truck.struct_list[4],[[manage.truck.goods_list[12],1]],360.0,product_num=1,)
        manage.truck.struct_list[5].product_list=[[0,manage.truck.goods_list[14],480.0]]
        manage.truck.goods_list[14].get_information(manage.truck.struct_list[5],[[manage.truck.goods_list[60],1]],480.0,product_num=1,)

    recover1()
    manage.truck.struct_list[0].findlo()
    getsc()
    block_list,mask=findCropland()
    manage.truck.struct_list[0].product_list=[]
    manage.truck.struct_list[0].proing_list=[[]for x in range(len(block_list))]
    def getInformation(product_list,struct=manage.truck.struct_list[0]):
        for i in range(len(product_list)):
            curgood=findgoods(product_list[i][1],whetherShow=False)[1]
            product_list[i][1]=curgood
            moveTo(int(product_list[i][0][0]+product_list[i][0][2]/2),int(product_list[i][0][1]+product_list[i][0][3]/2))
            mouseDown()
            getsc(sleep=0.5)
            product_list[i][0]=10*int(len(struct.product_list)/6)+i
            time1=findFrame2(form=1)
            product_list[i].append(time1)
            need_list=[[curgood,1]]
            curgood.get_information(struct,need_list,time1,product_num=2)
            mouseUp()
        struct.get_information(product_list)

    for x in block_list:
        for y in x:
            curmask= mask[y[1]-5:y[1]+5,y[0]-5:y[0]+5]
            juc=(np.sum(np.reshape(curmask,(1,-1)))/(curmask.size*255))
            if juc>0.8:
                moveTo(y[0],y[1])
                click()
                moveTo(0.1,0.1)
                getsc()
                product_list,ex_list=findFrame1(form=1)
                getInformation(product_list)
                for y in ex_list:
                    moveTo(y[0], y[1])
                    click()
                    getsc(sleep=0.5)
                    product_list, ex_list1 = findFrame1(form=1)
                    getInformation(product_list)
                break
        if juc>0.8:
            break
            # break





if __name__=="__main__":
    f = open('rf\\Class.txt', 'rb')
    list1 = pickle.load(f)
    f.close()
    # # # manage.struct_list=[]
    manage.truck.goods_list=list1[0]
    manage.truck.struct_list=list1[1]
    manage.truck.public_list=list1[2]
    # print(len(list1[2]))
    # sale = manage.Sale()
    # manage.truck.public_list.append(sale)
    ship=manage.Ship()
    manage.truck.public_list.append(ship)
    # list1[1][7].product([[list1[1][7].product_list[0][1],1]])
    # manage.struct_list[0].proing_list=[[]for x in range(len(manage.truck.struct_list[0].relLocation))]
    # prol=[[list1[1][6].product_list[1],2],[list1[1][6].product_list[0],2]]
    # print(type(list1[1][0]),type(1))
    # print(type(list1[1][0]) == manage.Cropland)
    #    list1[1][0].product(pro_list=[[list1[1][0].product_list[5],10],[list1[1][0].product_list[1],10],[list1[1][0].product_list[9],6]])
    # # list1[1][6].product(prol)
    # first_learn()
    # # # # #
    # # # # # # # print(manage.truck.struct_list[0].relLocation)
    # # f=open('rf\\Class.txt','wb')
    # # pickle.dump([manage.truck.goods_list,manage.truck.struct_list,manage.truck.public_list],f,0)
    # # f.close()
    # f = open('rf\\Class.txt', 'wb')
    # pickle.dump([manage.truck.goods_list, manage.truck.struct_list], f, 0)
    # f.close()
    # # # 1
    # # # f
    # second_learn()
    f=open('rf\\Class.txt','wb')
    pickle.dump([manage.truck.goods_list,manage.truck.struct_list,manage.truck.public_list],f,0)
    f.close()
    # second_learn()
    # f=open('rf\\goods.txt','wb')
    # pickle.dump([manage.truck.goods_list,manage.truck.struct_list,manage.truck.public_list],f,0)
    # f.close()
    # # print(position())
    # moveTo(0.10954616588419405, 0.3978638184245661)
    # mouseDown()
    # getsc()
    # mouseUp()


