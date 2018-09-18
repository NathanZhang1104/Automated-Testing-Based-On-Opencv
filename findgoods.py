# import the necessary packages
import pickle
from disbackground import dback
import cv2
from matplotlib import pyplot as plt
# initialize the index dictionary to store the image name
# and corresponding histograms and the images dictionary
# to store the images themselves

# loop over the image paths
def findgoods(img,goods_list,whetherShow=False,form=0):
    index = {}
    images = {}
    if type(img)==str:
        img=cv2.imread(img)
    testImg=cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    testHist = cv2.calcHist([img], [0, 1, 2], None, [8, 8, 8],
                        [0, 256, 0, 256, 0, 256])
    testHist = cv2.normalize(testHist, testHist).flatten()
    sample_list=goods_list
    for good in sample_list:
        # extract the image filename (assumed to be unique) and
        # load the image, updating the images dictionary
        if form==0:
            image = good.dbimg
        elif form==1:
            image=good.img
        # image[:,:,[0,0,0]]=[255,255,255]
        # image=dback(imagePath)
        # x1=[0,0,0]
        # x1=np.array(x1)
        # # np.where(image==x.all(),1,1)
        # for i in range(image.shape[0]):
        #     for j in range(image.shape[1]):
        #         if (image[i][j]==x1).all():
        #             image[i,j]=[178,233,254]
        images[good] = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # extract a 3D RGB color histogram from the image,
        # using 8 bins per channel, normalize, and update
        # the index
        hist = cv2.calcHist([image], [0, 1, 2], None, [8, 8, 8],
                            [0, 256, 0, 256, 0, 256])
        hist = cv2.normalize(hist,hist).flatten()
        index[good] = hist
    OPENCV_METHODS = (
        ("Correlation", cv2.HISTCMP_CORREL),
        ("Chi-Squared", cv2.HISTCMP_CHISQR),
        ("Intersection", cv2.HISTCMP_INTERSECT),
        ("Hellinger", cv2.HISTCMP_BHATTACHARYYA))

    # loop over the comparison methods
    for (methodName, method) in OPENCV_METHODS:
        # initialize the results dictionary and the sort
        # direction
        results = {}
        reverse = False

        # if we are using the correlation or intersection
        # method, then sort the results in reverse order
        if methodName in ("Correlation", "Intersection"):
            reverse = True
    for (k, hist) in index.items():
        # compute the distance between the two histograms
        # using the method and update the results dictionary]
        d = cv2.compareHist(testHist, hist, method)
        results[k] = d
    # sort the results
    results = sorted([(v, k) for (k, v) in results.items()], key=lambda x:x[0],reverse=reverse)

    # # initialize the results figure
    if whetherShow:
        fig = plt.figure("Results: %s" % (methodName))
        fig.suptitle(methodName, fontsize=20)
        ax = fig.add_subplot(3, 3, 1)
        ax.set_title('test')
        plt.imshow(testImg)
        plt.axis("off")
        # loop over the results
        for (i, (v, k)) in enumerate(results):
            # show the result
            if i>7:
                break
            ax = fig.add_subplot(3, 3, i +2)
            ax.set_title(str(results[i][1].path[10:-4])+': '+"%.2f" % results[i][0] )
            plt.imshow(images[k])
            plt.axis("off")
        plt.show()
    # show the OpenCV methods
    return results[0]

def matchContour(img):
    if 1:
        pa = []
        for j in range(1, 19):
            for i in range(5):
                pa.append('iby\\goods\\goods' + str(j) + 'r' + str(i) + 'bg.png')
                if j * 10 + j <= 42:
                    pa.append('iby\\plants\\plants' + str(j) + 'r' + str(i) + 'bg.png')
    cv2.imwrite('rf\\temc.png',dback(img,form=1))
    jp= 'rf\\temc.png'
    pa.append(jp)
    img1=cv2.imread(jp)
    # img1=img1[:int(img1.shape[0]/1.8),:]
    gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
    # thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
    ret, thresh = cv2.threshold(gray, 50, 255, 0)
    imgx, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    contours.sort(key=lambda x:cv2.contourArea(x),reverse=True)

    contours1 =contours[0]
    index=[]
    for x in pa:
        img1=cv2.imread(x)
        # img1 = img1[:int(img1.shape[0] / 2), :]
        gray = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
        # thresh = cv2.adaptiveThreshold(gray,255,1,1,11,2)
        ret, thresh = cv2.threshold(gray, 50, 255, 0)
        imgx, contours, hierarchy = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        contours.sort(key=lambda x: cv2.contourArea(x), reverse=True)
        contours2 = contours[0]
        hull=cv2.convexHull(contours2)
        img1 = cv2.drawContours(img1, contours, 0, (0, 255, 0), 3)
        # img1 = cv2.drawContours(img1, [hull], 0, (255,255,255), 3)
        result1=cv2.matchShapes(contours1, contours2, 3, 0.0)
        index.append([x,img1,result1])
    index.sort(key=lambda x:x[2])
    fig = plt.figure("Results" )
    fig.suptitle('1', fontsize=20)
    for i in range(len(index)):
        ax = fig.add_subplot(11, 11, i +1)
        ax.set_title("%s: %.2f" % (index[i][0][-9:-6], index[i][2]))
        b,g,r = cv2.split(index[i][1])
        index[i][1]= cv2.merge([r,g,b])
        plt.imshow(index[i][1])
        plt.axis("off")
    plt.show()
# matchContour('rf\\s1.png')
# help(cv2.matchShapes)
if __name__=='__main__':
    import manage
    f = open('rf\\goods.txt', 'rb')
    list1 = pickle.load(f)
    f.close()
    # # # manage.struct_list=[]
    goods_list=list1[0]
    manage.T(0)

    a=findgoods('rf\\scrpart.png',goods_list,whetherShow=True,)

    manage.T(1)