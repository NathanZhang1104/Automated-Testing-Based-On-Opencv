import cv2
import numpy as np
import random
import string
#######   training part    ###############



############################# testing part  #########################
def finnum(img,form=0,whetherShow=False):
    if type(img)==str:
        gray=cv2.imread(img,0)
    else:
        if len(img.shape)==3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray=img
    out = np.zeros(gray.shape,np.uint8)
    if form==0:
        samples = np.loadtxt('rf\\generalsamples.data', np.float32)
        responses = np.loadtxt('rf\\generalresponses.data', np.float32)
        MAX_DISTANCE=800000
        gray = cv2.resize(gray, (300, 300))
        # blur = cv2.GaussianBlur(gray, (5, 5), 0)
        ret2, thresh = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    elif form==1:
        samples = np.loadtxt('rf\\generalsamples2.data', np.float32)
        responses = np.loadtxt('rf\\generalresponses2.data', np.float32)
        MAX_DISTANCE=900000
        gray = cv2.resize(gray, (gray.shape[1]*4, gray.shape[0]*4))
        # ret, thresh = cv2.threshold(gray, 100, 255, 0)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        ret2, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY+ cv2.THRESH_OTSU)
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        tmp_file_name = 'iby\\time_data\\tmpfile_%s.png' %salt
        cv2.imwrite(tmp_file_name,thresh)
    elif form==2:
        samples = np.loadtxt('rf\\generalsamples2.data', np.float32)
        responses = np.loadtxt('rf\\generalresponses2.data', np.float32)
        MAX_DISTANCE=1500000
        gray = cv2.resize(gray, (gray.shape[1]*4, gray.shape[0]*4))
        # ret, thresh = cv2.threshold(gray, 100, 255, 0)
        blur = cv2.GaussianBlur(gray, (5, 5), 0)
        # ret2, thresh = cv2.threshold(blur, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        ret2, thresh = cv2.threshold(blur, 180, 255, cv2.THRESH_BINARY)
        salt = ''.join(random.sample(string.ascii_letters + string.digits, 8))
        tmp_file_name = 'iby\\time_data\\tmpfile_%s.png' %salt
        # cv2.imwrite(tmp_file_name,thresh)



    responses = responses.reshape((responses.size, 1))
    model = cv2.ml.KNearest_create()
    model.train(samples, cv2.ml.ROW_SAMPLE, responses)
    # help(type(model))

    # thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
    # cv2.imshow('1',thresh)
    # cv2.waitKey(0)
    imgx,contours,hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

    numlist=[]
    for cnt in contours:
        if cv2.contourArea(cnt)>100:
            [x,y,w,h] = cv2.boundingRect(cnt)
            if  h>15 :
                thresh1=thresh.copy()
                cv2.rectangle(thresh1,(x,y),(x+w,y+h),255,1)

                roi = thresh[y:y+h,x:x+w].copy()
                imgxr, contoursr, hierarchyr = cv2.findContours(roi, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

                contoursr.sort(key=lambda x:cv2.contourArea(x),reverse=True)
                for cnt in contoursr[1:]:
                    cv2.drawContours(roi, [cnt], 0, 0, -1)
                # cv2.imshow('im', roi)
                # cv2.waitKey(0)
                roismall = cv2.resize(roi,(10,10))

                roismall = roismall.reshape((1,100))
                roismall = np.float32(roismall)
                retval, results, neigh_resp, dists = model.findNearest(roismall, k = 1)
                if whetherShow:
                    print( retval, results, neigh_resp, dists )
                    cv2.imshow('12', thresh1)
                    cv2.waitKey(0)

                if dists<MAX_DISTANCE:
                    numlist.append([[x,y,w,h],int((results[0][0])),dists])

                string1 = str(int((results[0][0])))
                cv2.putText(out,string1,(x,y+h),0,1,(0,255,0))
    if form==1 or form==2:
        # x1=detect(test=cv2.imread('iby\\single\\shi.png'),sample=thresh,form=1,several=False,)
        # x2=detect(test=cv2.imread('iby\\single\\fen.png'),sample=thresh,form=1,)
        # if x1==None:
        #     x1=[0,0]
        # if x2==None:
        #     x2=[1000,0]
        x1=[0,0]
        x2=[1000,0]
        numlist.sort(key=lambda x:x[2],reverse=False)
        for x in numlist:
            if x[1]==104:
                x1=[x[0][0],x[0][1]]
                break
        for x in numlist:

            if x[1] == 109:
                x2 = [x[0][0], x[0][1]]
        i=0
        ju1=ju2=10
        for x in numlist:
            if x[1]!=104 and x[1]!=109:
                ju1=x[0][1]
                ju2=x[0][3]
                break
        while i <len(numlist):
            # if abs((numlist[i][0][1]-numlist[0][0][1]))/numlist[0][0][3]>0.2 or abs((numlist[i][0][2]-numlist[0][0][2]))/numlist[0][0][2]>1.2or abs((numlist[i][0][3]-numlist[0][0][3]))/numlist[0][0][3]>0.2:
            if numlist[i][0][3]/ju2<0.3 :
                numlist.pop(i)
                i-=1
            elif abs((numlist[i][0][1]+numlist[i][0][3]-ju1-ju2))/ju2>0.3 :
                numlist.pop(i)
                i -= 1
            i+=1
        numlist.sort(key=lambda x:x[0][0],reverse=False)
        time_list=[[],[],[]]
        for i in range(len(numlist)):
            if numlist[i][1]>100:
                continue
            if numlist[i][0][0]>x2[0]:
                time_list[2].append(numlist[i][1])
            elif   numlist[i][0][0]<x2[0] and numlist[i][0][0]>x1[0]:
                time_list[1].append(numlist[i][1])
            elif numlist[i][0][0]<x1[0]:
                time_list[0].append(numlist[i][1])
        for i in range(len(time_list)):
            if len(time_list[i])==2:
                time_list[i]=time_list[i][0]*10+time_list[i][1]
            elif len(time_list[i])==1:
                time_list[i]=time_list[i][0]
            else:
                time_list[i]=0
        time=time_list[1]+time_list[0]*60+time_list[2]/60
        ret=time
        # print(ret)
        # if ret > 700 or ret==0:
        #     cv2.imshow('1', thresh)
        #     cv2.waitKey(0)
    if form==0:
        i=0
        while i < len(numlist):
            # if abs((numlist[i][0][1]-numlist[0][0][1]))/numlist[0][0][3]>0.2 or abs((numlist[i][0][2]-numlist[0][0][2]))/numlist[0][0][2]>1.2or abs((numlist[i][0][3]-numlist[0][0][3]))/numlist[0][0][3]>0.2:
            if numlist[i][0][3] / numlist[0][0][3] < 0.3 or abs((numlist[i][0][1]-numlist[0][0][1]))/numlist[0][0][3]>0.2 :
                numlist.pop(i)
                i -= 1
            i += 1
        if len(numlist)==0:
            ret=None
        else:
            numlist.sort(key=lambda x:x[0][0],reverse=True)
            num=0
            for i in range(len(numlist)):
                num+=10**i*numlist[i][1]
            ret=num
    # cv2.imshow('im',roismall)
    # cv2.imshow('out',out)
    # cv2.waitKey(0)

    return ret

# n = im = finnum('iby\\goods\\goods' + str(5) + 'r' + str(4) + '.png')
if __name__=='__main__':
    # for i in range(1,19):
    #     for j in range(5):
    #         n=im = finnum(cv2.imread('iby\\goods\\goods'+str(i)+'r'+str(j)+'.png'))
    #         # print(i,j)
    #         print(n)
    #         n=finnum(cv2.imread('rf\\temporary.png'))
    #         print(n)
    n=finnum('iby\\time_data\\tmpfile_0sWvLlDn.png',form=0,whetherShow=False)
