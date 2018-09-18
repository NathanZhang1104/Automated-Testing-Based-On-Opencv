import cv2
import numpy as np

from matplotlib import pyplot as plt
class Staticpt:
    def __init__(self,imgs):
        sift = cv2.xfeatures2d.SIFT_create()
        self.statickp,self.staticdes=sift.detectAndCompute(imgs,None)
def loftwo (data,b=1):
    total_data = data[:,0:1]
    i=0
    while i<len(total_data):
        if total_data[i]==0:
            total_data = np.delete(total_data, i, axis=0)
            i-=1
        i+=1
    median = np.median(total_data)
    mad = b * np.median(np.abs(total_data - median))
    lower_limit1 = median - (3 * mad)
    upper_limit1 = median + (3 * mad)
    total_data = data[:, 1:2]
    i = 0
    while i < len(total_data):
        if total_data[i] == 0:
            total_data = np.delete(total_data, i, axis=0)
            i-=1
        i+=1
    median = np.median(total_data)
    mad = b * np.median(np.abs(total_data - median))
    lower_limit2 = median - (3 * mad)
    upper_limit2 = median + (3 * mad)
    ret =[[lower_limit1,lower_limit2],[upper_limit1,upper_limit2]]
    return ret
def detect(test,sample='rf\\scr.png',several=False,whetherShow=False,form=0,static=False,staticpt1=0):
    if type(test)==str:
        test=cv2.imread(test,0)
    else:
        if len(test.shape)==3:
            test= cv2.cvtColor(test, cv2.COLOR_BGR2GRAY)
    if type(sample)==str:
        sample=cv2.imread(sample,0)
    else:
        if len(sample.shape)==3:
            sample= cv2.cvtColor(sample, cv2.COLOR_BGR2GRAY)
    img1 = test # trainImage
    img2 = sample
    sift=cv2.xfeatures2d.SIFT_create()
    kp1, des1 = sift.detectAndCompute(img1,None)
    if static==True:
        kp2, des2 =staticpt1.statickp, staticpt1.staticdes
    else:
        kp2, des2 = sift.detectAndCompute(img2,None)
    FLANN_INDEX_KDTREE = 0
    index_params = dict(algorithm = FLANN_INDEX_KDTREE, trees = 5)
    search_params = dict(checks = 50)
    flann = cv2.FlannBasedMatcher(index_params, search_params)
    matches = flann.knnMatch(des1,des2,k=5)
    good = []
    if several:
        for x in matches:
            for i in range(len(x) - 1):
                if x[i].distance < 0.7 * x[i + 1].distance or x[i].distance < 200:
                    good.append(x[i])
    else:
        for x in matches:
            if x[0].distance<0.7*x[1].distance:
                good.append(x[0])
    if form==0:
        MIN_MATCH_COUNT =3
        if len(good)>=MIN_MATCH_COUNT:
            local_list=[]
            while len(good)>=MIN_MATCH_COUNT:
                src_pts = np.float32([ kp1[m.queryIdx].pt for m in good ]).reshape(-1,1,2)
                dst_pts = np.float32([ kp2[m.trainIdx].pt for m in good ]).reshape(-1,1,2)

                # print(dst_pts)
                M, mask = cv2.findHomography(src_pts, dst_pts, cv2.RANSAC,5)
                matchesMask= mask.ravel().tolist()
                # judst_pts=dst_pts.reshape(-1,2)
                # # for i in range(len(judst_pts)):
                # #     if matchesMask[i]==0:
                # #         judst_pts[i][0]=judst_pts[i][1]=0
                # matchesMask1=[[x,x] for x in matchesMask]
                # judst_pts=judst_pts*matchesMask1
                # julo=loftwo(judst_pts)
                # pt1=[]
                # pt2=[]
                # # for i in range(len(judst_pts)):
                # i=0
                # for i in range(len(judst_pts)):
                #     if judst_pts[i][0]>julo[1][0] or judst_pts[i][0]<julo[0][0]or judst_pts[i][1]>julo[1][1]or judst_pts[i][1]<julo[0][1]:
                #         if judst_pts[i][0] != 0:
                #             print(1)
                #             src_pts1 = np.delete(src_pts, i, axis=0)
                #             dst_pts1 = np.delete(dst_pts, i, axis=0)
                #         judst_pts[i]=[0,0]
                #         matchesMask[i]=0
                #
                #
                #     else:
                #         pt1.append(src_pts[i])
                #         pt2.append(dst_pts[i])
                # pt1=np.array(pt1)
                # pt2=np.array(pt2)
                # print(pt2)
                # M1, maskx = cv2.findHomography(src_pts1,dst_pts1, cv2.RANSAC,5)
                if sum(matchesMask)<MIN_MATCH_COUNT:
                    break
                src_pts.sort(axis=0)
                x1=src_pts[0][0][0];x2=src_pts[-1][0][0]
                y1=src_pts[0][0][1];y2=src_pts[-1][0][1]
                pts = np.float32([ [x1,y1],[x1,y2],[x2,y2],[x2,y1] ]).reshape(-1,1,2)
                dst = cv2.perspectiveTransform(pts,M)
                dst1=dst.reshape(4,2)
                dst1=np.append(dst1,dst1[1:3],axis=0)
                if cv2.matchShapes(pts,dst,1,0.0)>0.1:
                   break
                pt1 =[]
                for i in range(len(dst_pts)):
                    if matchesMask[i]!=0:
                        pt1.append(dst_pts[i][0])
                pt1=np.array(pt1)
                pt1=np.sort(pt1,axis=0)
                l1=int(len(pt1)/2)
                # [pt1[l1] + pt1[l1 + 1] + pt1[l1 - 1]]
                local_list.append([int((pt1[0][0]+pt1[-1][0])/2),int(pt1[-1][1])])
                if whetherShow:
                    draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                                       singlePointColor=None,
                                       matchesMask=matchesMask,  # draw only inliers
                                       flags=2)
                    # img1=cv2.imread(test);b, g, r = cv2.split(img1);img1= cv2.merge([r, g, b])
                    # img2=cv2.imread(sample); b, g, r = cv2.split(img2);img2= cv2.merge([r, g, b])
                    cv2.polylines(img2, [np.int32(dst)], True, [255,255,255], 3, cv2.LINE_AA)
                    cv2.circle(img2,(local_list[-1][0],local_list[-1][1]),5,5,-1)
                    img3=cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)
                    plt.imshow(img3)
                    plt.show()
                i = 0
                while i < len(good):
                    dist = cv2.pointPolygonTest(dst, kp2[good[i].trainIdx].pt, True)
                    if dist >= 0 or matchesMask[i]==1:
                        matchesMask.pop(i)
                        good.pop(i)
                        i -= 1
                    i += 1
            if several:
                ret = local_list
            if not several:
                if len(local_list)>0:
                    ret = local_list[0]
                else:
                    ret=None
        else:
            print ("Not enough matches are found --%d/%d" % (len(good),MIN_MATCH_COUNT))
            ret=[]

    if form==1:
        MIN_MATCH_COUNT=3
        if len(good)>=MIN_MATCH_COUNT:
            if whetherShow:
                matchesMask=None
                draw_params = dict(matchColor=(0, 255, 0),  # draw matches in green color
                                   singlePointColor=None,
                                   matchesMask=matchesMask,  # draw only inliers
                                   flags=2)
                # img1 = cv2.imread(test);
                # b, g, r = cv2.split(img1);
                # img1 = cv2.merge([r, g, b])
                # img2 = cv2.imread(sample);
                # b, g, r = cv2.split(img2);
                # img2 = cv2.merge([r, g, b])
                # cv2.polylines(img2, [np.int32(dst)], True, [255, 255, 255], 3, cv2.LINE_AA)
                img3 = cv2.drawMatches(img1, kp1, img2, kp2, good, None, **draw_params)
                plt.imshow(img3)
                plt.show()
            dst_pts = np.float32([kp2[m.trainIdx].pt for m in good])
            dst_pts=np.sort(dst_pts,0)
            ret=[int(dst_pts[int(len(dst_pts)/2)][0]),int(dst_pts[int(len(dst_pts)/2)][1])]
        else:
            # print("Not enough matches are found --%d/%d" % (len(good),MIN_MATCH_COUNT))
            ret=None
    return ret

# for i in range(1,4):
#     for j in  range(1,3):
        # detect('iby\\struct\\struct'+str(i)+"r"+str(j)+'.png',several=True,whetherShow=True)
if __name__=='__main__':
    img1=cv2.imread('iby\\struct\\struct10.png')
    cv2.imshow('1',img1)
    cv2.waitKey()
    # img1=img1[380:440,455:565]
    # cv2.imshow('1',img1)
    # cv2.waitKey(0)
    # cv2.imwrite('iby\\struct\\struct1r1.png',img1)
    # detect(cv2.imread("iby\\struct\\struct1r1.png"),sample=cv2.imread('rf\\scr.png'),several=True,whetherShow=True,form=0)
    detect(img1,sample=cv2.imread('rf\\scr.png'),several=True,whetherShow=True,form=0)




