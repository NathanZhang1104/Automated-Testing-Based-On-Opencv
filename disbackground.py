import numpy as np
import cv2
from matplotlib import pyplot as plt
def dback(img='rf\\scrpart.png',form=0,whetherShow=False,rect=0,dis=0,newmask=[0]):
    if type(img)==str:
        img=cv2.imread(img)
    img1=img
    mask = np.zeros(img.shape[:2],np.uint8)

    bgdModel = np.zeros((1,65),np.float64)
    fgdModel = np.zeros((1,65),np.float64)
    if rect==0:
            rect= (0,0,int(img.shape[1]),int(img.shape[0]))
    else:
        if rect[0]<1:
            rect = (int(img.shape[1]*rect[0]),int(img.shape[0]*rect[1]),int(img.shape[1]*rect[2]),int(img.shape[0]*rect[3]))
        else:
            rect=(rect[0],rect[1],rect[2],rect[3])

    if form==0:
        cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
        mask2 = np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    elif form==1:
        cv2.grabCut(img, mask, rect, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_RECT)
        mask[newmask == 255]= 1
        mask[newmask == 0]=0
        mask, bgdModel, fgdModel = cv2.grabCut(img, mask, None, bgdModel, fgdModel, 5, cv2.GC_INIT_WITH_MASK)
        mask2= np.where((mask == 2) | (mask == 0), 0, 1).astype('uint8')
    elif form==2:
        mask2=np.zeros(img.shape[:2],np.uint8)
        mask2[rect[1]:rect[3],rect[0]:rect[2]]=1
    if dis!=0:
        mask3=cv2.inRange(img1,np.array([dis[0]-2,dis[1]-2,dis[2]-2]),np.array([dis[0]+2,dis[1]+2,dis[2]+2]))
        mask3=np.where(mask3==255,0,1)
        mask3=mask3.astype(np.uint8)
        mask2=mask2*mask3

    ratio=(np.sum(np.reshape(mask2,(1,-1)))/mask2.size)
    img = img*mask2[:,:,np.newaxis]

    ret=img,ratio
    if whetherShow:
        b,g,r = cv2.split(img)
        img = cv2.merge([r,g,b])
        b,g,r = cv2.split(img1)
        img1 = cv2.merge([r,g,b])
        cv2.rectangle(img1,(rect[0],rect[1]),(rect[2],rect[3]),(0,255,0),1)
        plt.subplot(121);plt.imshow(img1)
        plt.subplot(122);plt.imshow(img)
        plt.show()
    return ret
if __name__=='__main__':
    # fig = plt.figure("Results" )
    # fig.suptitle('1', fontsize=20)
    # for i in range(1,4):
    #     for j in range(5):
    #         path1='iby\\plants\\plants'+str(i)+'r'+str(j)+'bg.png'
    #         # dback(path1,save=True)
    #         ax = fig.add_subplot(10, 10, (i-1)*5+j + 1)
    #         ax.set_title(str(i)+str(j))
    #         img=cv2.imread(path1)
    #         b, g, r = cv2.split(img)
    #         img = cv2.merge([r, g, b])
    #         plt.imshow(img)
    #         plt.axis("off")

    path1 = 'iby\\goods\\goods1r1.png'
    dback(path1,form=1,rect=[2,10,120,120],dis=[-1,-1,-1],whetherShow=True)





