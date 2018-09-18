import time
import cv2

import manage
from scr import getsc ,scrpart,template_pos
from mouse1 import swipeTo,Tough,initcur,recover1,swipeRel,muti_Swipe
from siftmatch import detect
from colorfind import findFrame1,findFrame2,findFrame3,findFrame4,find_colorblocks
from num import finnum
from findgoods import findgoods
from canndyedge import candySearch
import random
def findlo_Struct(struct,i1=0,j1=-1):
    originlo=manage.Truck.getOrigin()
    try:
        if type(struct)==manage.Cropland:
            # recover1()
            # getsc(sleep=0.3)
            # originlo = manage.Truck.getOrigin()
            if j1==-1:
                    rello=struct.relLocation[int(len(struct.relLocation)/2)][int(len(struct.relLocation[0])/2)]
                    selfLo = [originlo[0] + rello[0], originlo[1] + rello[1]]
                    raise  IndexError
            else:
                rello=struct.relLocation[i1][j1]
                # print(struct.relLocation[i1])
                # print(rello,originlo)
                selfLo = [originlo[0] + rello[0], originlo[1] + rello[1]]
        else:
            rello=struct.relLocation[i1]
            selfLo=[originlo[0]+rello[0],originlo[1]+rello[1]]

        if manage.Truck.scrmask[selfLo[1]][selfLo[0]][0]!=1 or selfLo[0]>0.73*manage.Truck.scrrect[0] or selfLo[0]<0 or selfLo[1]<0.2*manage.Truck.scrrect[0]  :
            raise IndexError
    except IndexError:
        po1 = (0.5, 0.5)
        relmo=[0.5 * manage.Truck.scrrect[0] - selfLo[0], 0.5 * manage.Truck.scrrect[1] - selfLo[1]]
        # if abs(relmo[0])>manage.Truck.scrrect[0]/2  or abs(relmo[1])>manage.Truck.scrrect[1]/2:
        #     k=max(int(abs(relmo[0])/(manage.Truck.scrrect[0]/2))+1,int(abs(relmo[1])/(manage.Truck.scrrect[1]/2))+1)
        #     for i in range(k):
        #         po2=(relmo[0]/k,relmo[1]/k)
        # else:
        po2=(relmo[0],relmo[1])
        swipeRel(po1, po2)
        originlo=[originlo[0]+relmo[0],originlo[1]+relmo[1]]
        print(originlo[1],manage.Truck.initorigin[1]*manage.Truck.scrrect[1])

        if originlo[0]>manage.Truck.initorigin[0]*manage.Truck.scrrect[0]:
            originlo[0]=manage.Truck.initorigin[0]*manage.Truck.scrrect[0]
        if originlo[1]>manage.Truck.initorigin[1]*manage.Truck.scrrect[1]:
            originlo[1] = manage.Truck.initorigin[1] * manage.Truck.scrrect[1]
        if originlo[1]<-82*int(720/manage.Truck.scrrect[1]):
            originlo[1] = -82*int(720/manage.Truck.scrrect[1])
        selfLo=[originlo[0]+rello[0],originlo[1]+rello[1]]
    ret=[selfLo[0],selfLo[1]]
    if type(struct)==manage.Struct:
        Tough(selfLo[0],selfLo[1])
        getsc(sleep=0.1)
        local_list, ex_list=findFrame1(form=0)
        for i in range(7):
            if len(local_list)==0:
                local_list, ex_list, proing_list=findlo_Struct(struct,i1)
            proing_list,time1=findFrame3()
            ret=local_list, ex_list,proing_list
    elif type(struct)==manage.Farm:
        Tough(selfLo[0],selfLo[1])
        getsc(sleep=0.3)
        # try:
        rect2,n=find_colorblocks(form=-2,whetherShow=False)
        if len(rect2)==0:
            return 0,0,0,0
        else:
            rect2=rect2[0]
            lo1=[rect2[0]+50,rect2[1]+rect2[3]-50]
            lo2=[rect2[0]+120,rect2[1]+rect2[3]-120]
            originlo = manage.Truck.getOrigin(form=1)
        if originlo==None:
            recover1()
            originlo = manage.Truck.getOrigin(form=1)
            selfLo = [originlo[0] + struct.relLocation[i1][0], originlo[1] + struct.relLocation[i1][1]]
            Tough(selfLo[0], selfLo[1], )
        selfLo = [originlo[0] + struct.relLocation[i1][0], originlo[1] + struct.relLocation[i1][1]]
        ret=selfLo,lo1,lo2,n
    elif type(struct)==manage.Cropland:
        if j1==-1:
            ret=selfLo
        else:
            Tough(selfLo[0], selfLo[1])
            time.sleep(0.3)
            lian_pos= template_pos('rf\\lian1.png')
            if lian_pos!=None:
                ret =lian_pos,selfLo
            else:
                lo_list,ex_list=findFrame1(form=0)
                if len(lo_list)>0:
                    originlo=manage.Truck.getOrigin(form=1)
                    if originlo==None:
                        recover1()
                        originlo=manage.Truck.getOrigin(form=1)
                        selfLo=[originlo[0]+struct.relLocation[i1][j1][0],originlo[1]+struct.relLocation[i1][j1][1]]
                        Tough(selfLo[0], selfLo[1])

                    lo1=[originlo[0]+struct.relLocation[i1][0][0],originlo[1]+struct.relLocation[i1][0][1]]
                    lo2=[originlo[0]+struct.relLocation[i1][-1][0],originlo[1]+struct.relLocation[i1][-1][1]]
                    ret=lo_list,ex_list,lo1,lo2
                else:
                    ret=0
    elif type(struct) == manage.Cang:
        ret=selfLo
        Tough(selfLo[0], selfLo[1])
    elif type(struct) == manage.Sale:
        Tough(selfLo[0], selfLo[1])
    elif type(struct) == manage.Ship:
        Tough(selfLo[0], selfLo[1])
    return ret
    # if selfLo[0]>0.8*manage.scrimgrect[0]
def product_Struct(struct,pro_list,lj):
    lo_list,ex_list,proing_list1=struct.findlo(lj)
    wher1=0
    try:
        ret=1
        if len(struct.relLocation)==1:
            fw1 = [len(x) for x in proing_list1].index(2)
            l1=len(struct.proing_list)-fw1
            for i in range(0,l1):
                struct.proing_list[i][0].num+= struct.proing_list[i][0].product_num
            # pro_list=pro_list[-fw1:]
            if fw1>=2:
                raise ValueError
    except ValueError:
        ret=0
    for x in pro_list:
        try:
            fw1=[len(x) for x in proing_list1].index(2)
            print(fw1,'1adsadw')
            if fw1>=2:
                raise ValueError
            list1=[x[1]for x in struct.product_list]
            loc = list1.index(x[0])
        except ValueError:
            # print('dont have this production',x[0])
            # cv2.imshow('1',x[0].img)
            # cv2.waitKey(0)
            break
        if loc>5 and loc<12 and wher1!=1:
            Tough(ex_list[0][0],ex_list[0][1])
            wher1=1
        elif loc >11and wher1!=2:
            Tough(ex_list[1][0],ex_list[1][1])
            wher1=2
        elif loc<6 and wher1!=0:
            Tough(ex_list[0][0], ex_list[0][1]-80)
            wher1=0
        loc= (loc + 1) % 6-1
        ju=1
        for i in range(x[1]):
            po1=(lo_list[loc][0]+int(lo_list[loc][2]/2),lo_list[loc][1]+int(lo_list[loc][3]/2))
            po2=(proing_list1[fw1][0],proing_list1[fw1][1])
            print('KKKKK')
            swipeTo(po1,po2)
            getsc()
            proing_list1,time1=findFrame3()
            if(len(proing_list1))==0:
                recover1()
                lo_list, ex_list,proing_list1=struct.findlo()
                break
            else:
                try:
                    fw2 = [len(x) for x in proing_list1].index(2)
                except ValueError:
                    ju=0
                    break
                if fw2-fw1==1:
                    if len(struct.relLocation)==1:
                        struct.proing_list.append([x[0],x[0].product_num])
                        struct.proing_list=struct.proing_list[-fw2:]
                    for y in x[0].need_list:
                        y[0].num-=y[1]
                    fw1=fw2
                    continue
                else:
                    break
        if ju==0:
            break
    # if len(struct.relLocation)==1:
    #     for x in struct.product_list:
    #         x[1].proing_num=0
    #     for x in struct.proing_list:
    #         x[0].proing_num+=x[0].product_num
    # if len(struct.relLocation)>1:
    for x in struct.product_list:
        x[1].proing_num=0
    goods_list1=[x[1]for x in struct.product_list]
    local_list1, ex_list1=findFrame1(form=1)
    if len(struct.relLocation)>1:
        for x in local_list1:
            curgood=findgoods(x[1],goods_list1)[1]
            num1=finnum(x[1])
            if num1!=None:
                curgood.num=num1
            else:
               pass

    ing_list=[]
    for x in proing_list1:
        if len(x) > 10:
            ing_list.append(x)
    for i in range(len(struct.relLocation)) :
        if i!=lj:
            lo_list, ex_list, proing_list1 = struct.findlo(i)
            for x in proing_list1:
                if len(x)>10:
                    ing_list.append(x)
    for  x in ing_list:
        curgood=findgoods(x,goods_list1)[1]
        curgood.proing_num+=curgood.product_num
    recover1()
    return ret
def product_Farm(struct,li):
    if type(struct)!=manage.Farm:
        raise TypeError
        print('it is not Farm')
    ret = 0
    if struct.product_list[0][1].need_list[0][0].num >=1:
        selflo,lo1,lo2,n=struct.findlo(li)
        # print(n)
        julo = find_colorblocks(form=-4)
        if len(julo) >=2:
            ret=0
        else:
            if n==0 or n==None:
                1
            else:
                po_list=[]
                po_list.append(lo1)
                x1=selflo[0]
                xr=100
                for j in range(1):
                    y1 = selflo[1] - 10-10*random.random()
                    for i in range(13):
                        po_list.append((x1+xr,y1))
                        y1+=int(4+4*random.random())
                        xr=-xr
                muti_Swipe(po_list,duration=0.6,steps=4)
                Tough(selflo[0],selflo[1])
                getsc()
                julo2=find_colorblocks(form=-4)
                if len(julo2)>1:
                    if abs(julo2[-1][1]-selflo[1])>100:
                        ret=0
                po_list=[]
                po_list.append(lo2)
                for j in range(1):
                    y1 = selflo[1] - 10-10*random.random()
                    for i in range(13):
                        po_list.append((x1+xr,y1))
                        y1+=int(4+4*random.random())
                        xr=-xr
                muti_Swipe(po_list,duration=0.6,steps=4)
            struct.proing_list=[[struct.product_list[0][1],5]]
            struct.product_list[0][1].proing_num=5
            ret=1
        recover1()
    return ret
def product_Cropland(struct,pro_list,wni):
    if type(struct)!=manage.Cropland:
        raise TypeError
        print('it is not Cropland')
    else:
        if len(struct.proing_list)!=len(struct.relLocation):
            struct.proing_list=[[]for x in range(len(struct.relLocation))]

    # for x in pro_list:

    # struct.findlo()
    re=struct.findlo(wni,0)

    if re==0:
        1
    elif len(re)==2:
        po_list=[]
        po_list.append(re[0])
        # moveTo(re[0][0], re[0][1])
        # mouseDown()
        for i in range(2):
            x1 = struct.relLocation[wni][0][0]-struct.relLocation[wni][0][0]+re[1][0]
            y1 = struct.relLocation[wni][0][1]-struct.relLocation[wni][0][1]+re[1][1]
            po_list.append((x1,y1))
            x2 = struct.relLocation[wni][-1][0] - struct.relLocation[wni][0][0] + re[1][0]
            y2 = struct.relLocation[wni][-1][1] - struct.relLocation[wni][0][1] + re[1][1]
            po_list.append((x2,y2))
        muti_Swipe(po_list)
        product_Cropland(struct, pro_list, wni)
    elif len(re)==4:
            if len(struct.proing_list[wni])==2:
                struct.proing_list[wni][0].num+=struct.proing_list[wni][1]
            if pro_list[0][0].num==0:
                for i in range(len(pro_list)):
                    if pro_list[i][0].num!=0:
                        t=pro_list[i][0]
                        pro_list[i][0]=pro_list[0][0]
                        pro_list[0][0]=t
                        break
            list1=[x[1]for x in struct.product_list]
            loc = list1.index(pro_list[0][0])
            lo_list=re[0]
            ex_list=re[1]
            if loc > 5 and loc < 12 :
                Tough(ex_list[0][0], ex_list[0][1])
            elif loc > 11:
                Tough(ex_list[1][0], ex_list[1][1])
            # elif loc < 6:
            #     Tough(ex_list[0][0], ex_list[0][1] - 80)
            loc = (loc + 1) % 6 - 1
            po1=(lo_list[loc][0] + int(lo_list[loc][2] / 2), lo_list[loc][1] + int(lo_list[loc][3] / 2))
            po2=(re[2][0],re[2][1])
            po3=(re[3][0],re[3][1])
            # dragTo(proing_list1[fw1][0], proing_list1[fw1][1])
            # print(po1,po2,po3)
            muti_Swipe([po1,po2,po3,po2,po3])

            pro_list[0][1]=pro_list[0][1]-len(struct.relLocation[0])
            if pro_list[0][0].num>=len(struct.relLocation[0]):
                struct.proing_list[wni]=[pro_list[0][0],len(struct.relLocation[0])*2]
                pro_list[0][0].num-=len(struct.relLocation[0])
            else:
                struct.proing_list[wni]=[pro_list[0][0],pro_list[0][0].num*2]
                pro_list[0][0].num=0
            # if pro_list[0][1]<=0:
            #     pro_list.pop(0)
            # if len(pro_list)==0:
            #     # break
            #     1
    print('3', time.time())

    for x in struct.product_list:
        x[1].proing_num=0
    for x in struct.proing_list:
        if len(x)>0:
            x[0].proing_num+=x[1]
def getstatis_Cang(struct,truck,whetherGetcapacity=False):

    struct.findlo()
    # click()??
    p3 = [0.250638629283489096, 0.7566489361702128]
    if whetherGetcapacity==True:
        time.sleep(0.5)
        Tough(0.49104234527687296, 0.8737864077669902)
        img=getsc()
        img = scrpart((0.42, 0.53), (0.3, 0.35))
        curnum = finnum(img)
        print(curnum)
        recover1()
        img=getsc()
        if curnum==None or curnum==0:
            cv2.imshow('1',img)
            cv2.waitKey(0)
            img = img[200:250, 600:900]
            curnum = finnum(img)
            if curnum>10000:
                curnum=curnum%1000
            else:
                curnum=curnum%100
        struct.capacity=curnum


    if struct==truck.public_list[1]:
        form=0
    elif struct==truck.public_list[2]:
        form=1
    IMG_list=[]
    for i in range(25):
        getsc()
        a=time.time()

        img_list,ju=candySearch()
        IMG_list.extend(img_list)
        if ju <0.1 :
            break
        swipeRel(p3, (0, -0.3))
    if truck.grade<=37:
        for x in truck.goods_list:
            if x.cang==form:
                x.num=0
        for x in IMG_list:
            curnum = finnum(x)

            if curnum == None:
                continue
            else:
                # goodscur=manage.Goods(num=curnum,path=name1+str(i)+".png")
                curgood = findgoods(x,truck.goods_list, form=1)[1]
                curgood.num = curnum
                curgood.cang=form
    else:
        class Curg():
            def __init__(self,num,img):
                self.num=num
                self.img=img
        cur_goodlist=[]
        for x in IMG_list:
            curnum=finnum(x)
            if curnum==None:
                x=x[0:10,10:20]
                curnum=0
            cur_goodlist.append(Curg(curnum,x))
        for x in truck.goods_list:
            if x.cang==form:
                x.num=findgoods(x.img,cur_goodlist, form=1)[1].num
                print(x.num)
                if x.num==None:
                    cv2.imshow('12',findgoods(x.img,cur_goodlist, form=1)[1].img)
                    cv2.waitKey(0)
    # for x in img_list:
    #     curnum = finnum(x)
    #
    #     if curnum == None:
    #         continue
    #     else:
    #         # goodscur=manage.Goods(num=curnum,path=name1+str(i)+".png")
    #         curgood = findgoods(x,truck.goods_list, form=1)[1]
    #         curgood.num = curnum
    #         curgood.cang=formopkhjkkkkkkkkkkkkkkkkkkkwwwwwwwww
    a = []
    for x in truck.goods_list:
        a.append(x.num)
    recover1()
def salegoods(struct,truck,sale_list):
    print('贩卖')
    struct.findlo()
    getsc()
    while len(sale_list)>0:
        getsc()
        lo1_list=find_colorblocks(form=12)
        for x in lo1_list:
            Tough(x[0]+x[2]/2,x[1]+x[3]/2+200)
        getsc()
        lo2_list=find_colorblocks(form=11)
        if len(lo2_list)>0:
            Tough(lo2_list[-1][0],lo2_list[-1][1])
        else:
            swipeRel((0.5,0.5),(-0.4,0))
            getsc()
            lo1_list = find_colorblocks(form=12)
            for x in lo1_list:
                Tough(x[0] + x[2] / 2, x[1] + x[3] / 2+200)
            getsc()
            lo2_list = find_colorblocks(form=11)
            if len(lo2_list)==0:
                Tough(0.7125407166123778, 0.5339805825242718)
                Tough(0.500814332247557, 0.6990291262135923)
                break
            else:
                continue
        if sale_list[0][0].product_struct!=truck.struct_list[0]:
            Tough(0.1262214983713355, 0.521497919556172)
        for i in range(20):
            getsc()
            cim_list,ratio=candySearch(form=1)
            ju1=0
            for x in cim_list:
                x[0]=findgoods(x[0],truck.goods_list,form=1,whetherShow=False)[1]
                if x[0]==sale_list[0][0]:
                    ju1=1
                    Tough(x[1][0],x[1][1])
                    time.sleep(0.5)
                    for i in range(sale_list[0][1]-int(x[0].num/2)):
                        x[0].num-=1
                        Tough(0.762214983713355, 0.3522884882108183)
                    Tough(0.6262214983713354, 0.7919556171983356)
                    if x[0].num==1:
                        x[0].num=0
                    else:
                        x[0].num=x[0].num-int(x[0].num/2)
                    break
            if ratio<0.1 and ju1==0:
                # cv2.imshow('2',sale_list[0][0].img)
                # cv2.waitKey(0)
                recover1()
            if ratio<0.1 or ju1==1:
                break

            swipeRel((0.23638629283489096, 0.7566489361702128), (0, -0.3))
        sale_list.pop(0)
    recover1()
    time.sleep(0.5)
    Tough(0.03,0.08)
def coorder_Ship(struct,truck):
    for x in truck.goods_list:
        x.N1=0
    struct.findlo()
    getsc()
    def COMOR(lo):
        Tough(lo[0],lo[1])
        time.sleep(0.2)
        Tough(0.756514657980456, 0.4618585298196949)
        Tough(0.6677524429967426, 0.20249653259361997)
    order_lo=findFrame4()
    if len(order_lo)==0:
        order_lo = findFrame4(form=1)
        for x in order_lo:
            x=findgoods(x,truck.goods_list)[1]
            if x.product_struct == truck.struct_list[0]:
                x.N1+=10
                x.adK0(a=0.1, b=1)
            else:
                x.N1+=3
                x.adK0(a=0.1, b=1)
        recover1()
    else:
        for x in order_lo:
            if x[0]==0:
                continue
            elif x[-1]==True:
                x[1] = findgoods(x[1], truck.goods_list,whetherShow=False)[1]
                # if x[1].product_struct==truct.struct_list[0]:
                print(x[1].num,x[1].N0)
                if x[1].num-x[2]>=x[1].N0:
                    COMOR(x[0])
                    x[1].num -=x[2]
                else:
                    x[1].N1+=x[2]
                # else:
                #     COMOR(x[0])
            elif x[-1]==False:
                x[1] = findgoods(x[1], truck.goods_list)[1]
                x[1].adK0(a=0.1, b=1)
                x[1].N1+=x[2]
        order_lo=findFrame4()
        jugo=1
        for x in order_lo:
            if x[0]!=0:
                jugo=0
                break
        if jugo==1:
            Tough(0.743485342019544, 0.8196948682385575)
            time.sleep(10)
    recover1()

if __name__=='__main__':
    1


