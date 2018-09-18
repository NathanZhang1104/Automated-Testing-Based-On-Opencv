import time
import cv2
import pickle
import numpy as np
import classmethodINthere
import matplotlib.pyplot as plt
import scr
import mouse1
import os
import panorama
import cmath
import num

class Goods:
    def __init__(self,path,num):
        self.num = num
        self.path=path
        self.img=cv2.imread(path)
        self.dbimg=cv2.imread(path[:-4]+'bg.png')
        self.cang=0
        self.N0=0
        self.N1=0
        self.K0=1
    def demand(self,form=0):
        list1=[x[1] for  x in self.product_struct.product_list]
        l=list1.index(self)
        k1=1-l/(2*len(self.product_struct.product_list))
        if form==0:

            ret=k1*(1/cmath.e)**(self.K0*(self.num+self.proing_num-self.N0-self.N1+1))
        elif form==1:
            ret=(1/cmath.e)**(self.K0*(self.num+self.proing_num-self.N0-self.N1+1))
        return ret
    def adK0(self,a,b):
        self.K0=(self.K0+b*a)/(1+b)
    def jupro(self):
        ret=[]
        for x in self.need_list:
            if x[0].num<x[1]:
                ret.append([x[0],x[1]-x[0].num])
        return ret
    def get_information(self,product_struct,need_list,product_time,product_num=1,):
        self.product_struct=product_struct
        self.product_time=product_time
        self.product_num=product_num
        self.need_list=need_list
        self.proing_num=0

    def show(self):
        print('num=',self.num)
        cv2.imshow('1',self.dbimg)
class Struct:
    def __init__(self,num,path):
        # self.name=name
        self.num=num
        self.path=path
        self.img=cv2.imread(path)
        self.relLocation=[]
        self.product_list=[]
        self.tobeComplete=[]
        self.proing_list=[]
        self.temimg_list=[]
    def findlo(self,i=0,j=-1):
        ret=classmethodINthere.findlo_Struct(self,i,j)
        return ret

    def get_information(self,product_list):
        self.product_list.extend(product_list)
    # def __init__(self,preout):
    # #     # self.need_list.append(preneed)
    #     self.output_list.append(preout)
    def product(self,pro_list,li=0):
        ret=classmethodINthere.product_Struct(self,pro_list,li)
        return ret
    def getProinglist(self,proing_list=None):
        if proing_list!=None:
            self.proing_list=proing_list
            self.stotime=time.time()
        i1=k1=0
        while i1<len(proing_list):
            x=proing_list[i1]
            if x[1]+k1>time.time()-self.stotime:
                x[1]=x[1]-(time.time()-self.stotime)
                break
            else:
                k1+=x[1]
                proing_list.pop(i1)
                i1-=1
            i1+=1
        ret=proing_list
        return ret
    def show(self):
        print('num=',self.num)
        cv2.imshow(self.img)
class Truck(Struct):
    if 1:
        scrrect = scr.getsc().shape
        scrmask = np.ones(scrrect)
        scrrect = [scrrect[1], scrrect[0]]
        scrmask[0:int(0.148 * scrrect[1]), 0:int(0.28 * scrrect[0])] = 0
        scrmask[int(0.82 * scrrect[1]):, 0:int(0.1 * scrrect[0])] = 0
        scrmask[0:int(0.09 * scrrect[1]), int(0.388 * scrrect[0]):] = 0
        scrmask[int(0.248 * scrrect[1]):int(0.48 * scrrect[1]), int(0.92 * scrrect[0]):] = 0
        scrmask[int(0.82 * scrrect[1]):, int(0.80 * scrrect[0]):] = 0
        initorigin = [0.46205357142857145,0.6046296296296296]
    def __init__(self):
        path = 'rf\\scrpart.png'
        num=1
        Struct.__init__(self, num, path)
        retval = os.getcwd()
        os.chdir(retval)
        self.relLocation=[[0,0]]
        self.start = time.time()
        self.scrrect=scr.getsc().shape
        self.scrmask=self.get_scrmark()
        self.initorigin = [0.46205357142857145,40.6046296296296296]
        self.goods_list=[]
        self.struct_list=[]
        self.public_list=[self,]
        self.password=0
        self.grade=0
        self.panoimg=0
        self.WHETHER_crop = 1
        self.WHETHER_farm = 1
        self.WHETHER_struct = 1
        self.WHETHER_sale =1
        self.WHETHER_ship = 1
    @classmethod
    def getOrigin(cls,form=0,inital=False):
        if inital:
            mouse1.initcur(full=True)
        for i in range(3):
            ori_po=scr.template_pos(cv2.imread('rf\\truck1.png'))
            # if ori_po==None:
            #     ori_po = scr.template_pos(cv2.imread('rf\\truck1.png'),sample='rf\\scr.png')
            # if ori_po==None:
            #     ori_po2 = scr.template_pos(cv2.imread('rf\\shenmi.png'),sample='rf\\scr.png')
            #     if ori_po2!=None:
            #         ori_po=[ori_po2[0]-int(514*scr.getrect()[0]/1080),ori_po2[0]+int(375*scr.getrect()[0]/1080)]

            if ori_po!=None:
                ret=ori_po
                return ret
            else:
                if form == 1:
                    break
                if i == 0:
                    mouse1.recover1()
                else:
                    mouse1.initcur()
    def get_scrmark(self):
        scrrect = self.scrrect
        scrmask = np.ones(scrrect)
        scrrect = [scrrect[1], scrrect[0]]
        scrmask[0:int(0.148 * scrrect[1]), 0:int(0.28 * scrrect[0])] = 0
        scrmask[int(0.82 * scrrect[1]):, 0:int(0.1 * scrrect[0])] = 0
        scrmask[0:int(0.09 * scrrect[1]), int(0.388 * scrrect[0]):] = 0
        scrmask[int(0.248 * scrrect[1]):int(0.48 * scrrect[1]), int(0.92 * scrrect[0]):] = 0
        scrmask[int(0.82 * scrrect[1]):, int(0.80 * scrrect[0]):] = 0
        return scrmask
    def getGrade(self):
        mouse1.recover1()
        scr.getsc()
        img = scr.scrpart((0.45, 0.54), (0.01, 0.1))
        self.grade=num.finnum(img)
        print(self.grade)
        time.sleep(3)
    def save(self,filename='rf\\Class.txt'):
        f = open(filename, 'wb')
        pickle.dump([self.goods_list, self.struct_list, self.public_list, self.password,self.panoimg,self.temimg_list], f, 0)
        f.close()
        print('saved')
       
    def reload(self,filename='rf\\Class.txt'):
        f = open(filename, 'rb')
        list1 = pickle.load(f)
        f.close()
        self.goods_list = list1[0]
        self.struct_list = list1[1]
        self.public_list = list1[2]
        self.password=list1[3]
        self.panoimg=list1[4]
        self.temimg_list=list1[5]#1:truck_pos 2:
        print('reloaded')
    def T(self,s=-1):
        ret = time.time() - self.start
        if s != -1:
            s2 = str(time.time() - self.start)
            s =str(s)
            print(s + ':' + s2)
        return ret
    def getpanorama(self):
        # if 1:
        #     scrrect = scr.getsc().shape
        #     scrmask = np.ones(scrrect)
        #     scrrect = [scrrect[1], scrrect[0]]
        #     scrmask[0:int(0.175 * scrrect[1]), 0:int(0.28 * scrrect[0])] = 0
        #     scrmask[int(0.82 * scrrect[1]):, 0:int(0.1 * scrrect[0])] = 0
        #     scrmask[0:int(0.12 * scrrect[1]), int(0.42 * scrrect[0]):] = 0
        #     scrmask[0:int(0.04 * scrrect[1]), :] = 0
        #     scrmask[int(0.276 * scrrect[1]):int(0.5 * scrrect[1]), int(0.925 * scrrect[0]):] = 0
        #     scrmask[int(0.84 * scrrect[1]):, int(0.82 * scrrect[0]):] = 0
        #     self.scrrect=scrrect
        #     self.scrmask=scrmask
        panoimg, origin1 = panorama.getpanorama(self, whetherShow=False)
        f = open('rf\\goods.txt', 'wb')
        pickle.dump([self.goods_list, self.struct_list, self.public_list], f, 0)
        f.close()
        b, g, r = cv2.split(panoimg)
        panoimg = cv2.merge([r, g, b])
        plt.imshow(panoimg)
        plt.show()
    def savepanorama(self):
        f = open('rf\\goods.txt', 'rb')
        list1 = pickle.load(f)
        f.close()
        self.goods_list = list1[0]
        self.struct_list = list1[1]
        self.public_list = list1[2]
        self.save()

    def main(self):
        if 1:

            def SALE(whetherShow=False):
                liangsum = self.public_list[2].getSum(self)
                huosum = self.public_list[1].getSum(self)
                demand_list = list(filter(lambda x: x.product_struct != 0, self.goods_list))
                demand_list = sorted(demand_list, key=lambda x: x.demand(form=1), reverse=False)
                sale_list = []
                if liangsum / self.public_list[2].capacity > 0.85:
                    # sale_list1 = list(filter(lambda x: x.cang == 1, demand_list))
                    # sale_list1 = sale_list1[0:2]
                    # sale_list1 = [[x,0] for x in sale_list1]
                    # sale_list.extend(sale_list1)
                    sale_list1 = sorted(demand_list, key=lambda x: x.num - (x.N0 + x.N1), reverse=True)
                    sale_list1 = [[x, 0] for x in sale_list1]
                    sale_list1 = sale_list1[0:4]
                    sale_list.extend(sale_list1)

                if huosum / self.public_list[1].capacity > 0.9:
                    sale_list1 = list(filter(lambda x: x.cang == 0, demand_list))
                    sale_list1.sort(key=lambda x: x.num - x.N0 - x.N1, reverse=True)
                    sale_list1 = [[x, 0] for x in sale_list1]
                    sale_list.extend(sale_list1[:4])
                if huosum / self.public_list[1].capacity > 0.85:
                    sale_list1 = list(filter(lambda x: x.cang == 0, demand_list))
                    sale_list1 = list(filter(lambda x: x.num + x.proing_num - x.N1 - x.N0 > 0, sale_list1))
                    sale_list1.sort(key=lambda x: x.K0, reverse=True)
                    #
                    # if len(sale_list)>6:
                    sale_list2 = []
                    ju1 = i = 0
                    while i < len(sale_list1):
                        if sale_list1[i].num != 0:
                            if abs(sale_list1[i].K0 - sale_list1[0].K0) < 0.0001:
                                sale_list2.append([sale_list1[i], sale_list1[i].num])
                            else:
                                if ju1 == 0:
                                    sale_list2.sort(key=lambda x: x[0].num, reverse=True)
                                    # for x in sale_list2:
                                    ju1 = 1
                                else:
                                    sale_list2.append([sale_list1[i], 0])
                        i += 1
                    sale_list.extend(sale_list2[0:3])

                sale_list = list(filter(lambda x: x[0].num != 0, sale_list))
                if whetherShow:
                    for i1 in range(len(sale_list)):
                        x = sale_list[i1][0]
                        plt.subplot(len(sale_list), 2, 2 * i1 + 1)
                        t = "num=%s,proingnum=%s,K0=%s" % (x.num, x.proing_num, x.K0,)
                        t2 = "demand=%s" % (x.demand(form=1))
                        plt.text(150, 30, t, ha='left', fontsize=10, rotation=0, wrap=True)
                        plt.text(150, 60, t2, ha='left', fontsize=10, rotation=0, wrap=True)
                        img1 = cv2.cvtColor(x.img, cv2.COLOR_BGR2RGB)
                        plt.imshow(img1)
                    plt.show()
                if len(sale_list) > 0:
                    self.public_list[3].sale(self, sale_list)

            def PRODUCT_STUCT(i, whethershow=False):
                for j in range(self.struct_list[i].num):
                    x1 = self.struct_list[i]
                    st_p = sorted(x1.product_list, key=lambda x1: x1[1].demand(), reverse=True)
                    st_p = [[x[1], 1] for x in st_p]
                    st_pr = []
                    ad_list = []
                    for x in st_p:
                        ju1 = x[0].jupro()
                        if len(ju1) == 0:
                            st_pr = [x]
                            for y in x[0].need_list:
                                ad_list.append(y[0])
                                # y[0].adK0(a=2, b=1)
                            break
                        else:
                            for y in ju1:
                                # if type(y[0].product_struct) != type(self.struct_list[1]):
                                #     ad_list.append(y[0])
                                y[0].adK0(a=0.1, b=1)

                                # y[0].adK0(a=0.1, b=1)
                                # else:
                                #     ad_list.append(y[0].need_list[0][0])
                                # y[0].need_list[0][0].adK0(a=2, b=1)
                    if whethershow:
                        list1 = sorted(self.struct_list[i].product_list, key=lambda x: x[1].demand(), reverse=True)
                        for i1 in range(len(self.struct_list[i].product_list)):
                            x = list1[i1]
                            plt.subplot(len(self.struct_list[i].product_list), 2, 2 * i1 + 1)
                            t = "num=%s,proingnum=%s,K0=%s" % (x[1].num, x[1].proing_num, x[1].K0,)
                            t2 = "N0=%s N1=%s demand=%s" % (x[1].N0, x[1].N1, x[1].demand())
                            plt.text(150, 30, t, ha='left', fontsize=10, rotation=0, wrap=True)
                            plt.text(150, 60, t2, ha='left', fontsize=10, rotation=0, wrap=True)
                            img1 = cv2.cvtColor(x[1].img, cv2.COLOR_BGR2RGB)
                            plt.imshow(img1)
                        plt.show()
                    ju1 = x1.product(st_pr, j)
                    if ju1 == 1:
                        for x in ad_list:
                            x.adK0(a=0.1, b=1)

            def PRODUCT_CROP(whethershow=False):
                # crop_pl = self.struct_list[0].product_list.copy()
                # crop_pl.sort(key=lambda x: x[1].demand(), reverse=True)
                # # crop_pl = list(filter(lambda x: (x[1].K0>0.22 or x[1].num+x[1].proing_num-x[1].K0<3), crop_pl))
                # # crop_pl = list(filter(lambda x: x[1].num!=0, crop_pl))
                # crop_pl = [[x[1], len(self.struct_list[0].relLocation[0])] for x in crop_pl]
                self.struct_list[0].findlo()
                for i in range(len(self.struct_list[0].relLocation)):
                    crop_pl = self.struct_list[0].product_list.copy()
                    crop_pl.sort(key=lambda x: x[1].demand(), reverse=True)
                    # crop_pl = list(filter(lambda x: (x[1].K0>0.22 or x[1].num+x[1].proing_num-x[1].K0<3), crop_pl))
                    # crop_pl = list(filter(lambda x: x[1].num!=0, crop_pl))
                    crop_pl = [[x[1], len(self.struct_list[0].relLocation[0])] for x in crop_pl]
                    if whethershow:
                        for i1 in range(len(crop_pl)):
                            x = crop_pl[i1][0]
                            plt.subplot(len(crop_pl), 2, 2 * i1 + 1)
                            t = "num=%s,proingnum=%s,K0=%s,N0+N1=%s" % (x.num, x.proing_num, x.K0, x.N0 + x.N1)
                            t2 = "demand=%s" % (x.demand())
                            plt.text(150, 30, t, ha='left', fontsize=10, rotation=0, wrap=True)
                            plt.text(150, 60, t2, ha='left', fontsize=10, rotation=0, wrap=True)
                            img1 = cv2.cvtColor(x.img, cv2.COLOR_BGR2RGB)
                            plt.imshow(img1)
                        plt.show()
                    self.struct_list[0].product(crop_pl, i)

            class Whether():
                def __init__(self):
                    self.whether = 1

                def changewhether(self, k):
                    self.whether = k

        self.reload()
        scr.getsc()
        mouse1.initcur()
        # self.public_list[4].relLocation=[(-40,510)]
        # PRODUCT_STUCT(11,whethershow=True)
        # self.public_list[4].findlo()
        # print(len(self.struct_list[15].relLocation))
        # PRODUCT_STUCT(8,whethershow=False)
        # print(self.struct_list[0].proing_list)
        # PRODUCT_CROP(whethershow=True)
        # print(self.struct_list[15])
        # SALE(whetherShow=True)
        # self.struct_list[0].findlo()
        # self.public_list[4].coorder()
        # ju1 = self.struct_list[2].product(li=1)
        # self.public_list[4].coorder()

        self.getGrade()
        self.public_list[1].getStatic(self, whetherGetcapacity=True)
        self.public_list[2].getStatic(self, whetherGetcapacity=True)
        while self.T(0) < 50000:
            if self.WHETHER_ship:
                self.public_list[4].coorder(self)
            if self.WHETHER_crop:
                PRODUCT_CROP()
                self.save()
            if self.WHETHER_sale:
                SALE(whetherShow=False)
            if self.WHETHER_struct:
                PRODUCT_STUCT(7,whethershow=False)
            for i in range(1, 6):
                a = self.struct_list[i].product_list[0][1].need_list[0][0].num
                print(a)
            if self.WHETHER_farm:
                for i in range(1,6):
                    a=self.struct_list[i].product_list[0][1].need_list[0][0].num
                    print(a)
                for i in range(1, 6):
                    for j in range(self.struct_list[i].num):
                        ju1 = self.struct_list[i].product(li=j)
                        if ju1 == 1:
                            self.struct_list[i].product_list[0][1].need_list[0][0].adK0(a=0.1, b=1)

            self.public_list[1].getStatic(self)
            self.public_list[2].getStatic(self)
            if self.WHETHER_sale:
                SALE()
            if self.WHETHER_struct:
                for i in range(6, len(self.struct_list)):
                    PRODUCT_STUCT(i)
            for x in self.goods_list:
                x.adK0(a=1, b=0.2)
            if self.WHETHER_sale:
                SALE()
            self.save()
            print('done')
            time.sleep(300 - 2 * self.grade)
        self.save()
class Cropland(Struct):
    def __init__(self,num):
        path='rf\\scrpart.png'
        Struct.__init__(self, num,path)
        self.temimg_list=[]

    def product(self,pro_list,i):
        classmethodINthere.product_Cropland(self,pro_list,i)
class Farm(Struct):
    def __init__(self, num):
        path = 'rf\\scrpart.png'
        Struct.__init__(self, num, path)
    def product(self,pro_list=0,li=0):
        ret=classmethodINthere.product_Farm(self,li)
        return ret
class Cang(Struct):
    def __init__(self,path,capacity):
        num = 1
        Struct.__init__(self, num, path)
        self.capacity=capacity
    def getStatic(self, truck,whetherGetcapacity=False):
        classmethodINthere.getstatis_Cang(truck=truck,struct=self,whetherGetcapacity=whetherGetcapacity)
    def getSum(self,truck):
        sum=0
        if self==truck.public_list[1]:
            for x in truck.goods_list:
                if x.cang==0:
                    if x.num==None:
                        x.num=0
                    sum+=x.num
        elif self==truck.public_list[2]:
            for x in truck.goods_list:
                if x.cang==1:
                    if x.num == None:
                        x.num = 0
                    sum+=x.num
        return sum
class Sale(Struct):
    def __init__(self):
        num = 1
        Struct.__init__(self, num, 'iby\\struct\\0s1_shouwulan.jpg')
    def sale(self,truck,sale_list):
        classmethodINthere.salegoods(self,truck,sale_list)
class Ship(Struct):
    def __init__(self,):
        num = 1
        path='rf\\scr.png'
        Struct.__init__(self, num, path)
        self.relLocation=[[-30,400]]
    def coorder(self,truck):
        classmethodINthere.coorder_Ship(self,truck)
if __name__ == "__main__":

    # x1 = Truck()
    # x1.reload()
    # # f = open('rf\\x1.txt', 'rb')
    # x1 = pickle.load(f)
    # print(x1.struct   _list[0].num)
    Truck.getOrigin()