import tkinter as tk
from  tkinter import *
import time
import manage
from tkinter import ttk
from matplotlib import pyplot as plt
import cv2
import cpu
import panorama
import os
import mouse1
import  traceback

retval = os.getcwd()
os.chdir( retval)
class CanvasDemo(tk.Toplevel):
    def __init__(self,si):
        super().__init__()
        self.title('位置')
        # 弹窗界面
        self.si=si
        self.setup_UI()
        self.after(10, self.move_ball)
        self.rello=manage.truck.struct_list[self.si].relLocation

    def mouseMove(self, event):
        self.mouse_x = event.x
        self.mouse_y = event.y
        origin=[manage.truck.initorigin[0]*manage.truck.scrrect[0],manage.truck.initorigin[1]*manage.truck.scrrect[1]]
        # im1=panorama.showStruct(manage.truck.panoimg,manage.truck.struct_list[self.si].relLocation,origin)or
        # im1 = cv2.resize(im1, (1300, 700), interpolation=cv2.INTER_CUBIC)
        x1=self.mouse_x*manage.truck.panoimg.shape[1]/1200
        y1=self.mouse_y*manage.truck.panoimg.shape[0]/600
        lo1=[int(x1-origin[0]),int(y1-origin[1])]
        self.rello.append(lo1)
        im1=panorama.showStruct(manage.truck.panoimg,self.rello,origin)
        im1 = cv2.resize(im1, (1200, 600), interpolation=cv2.INTER_CUBIC)
        cv2.imwrite('rf\\temc.png', im1)
        im = tk.PhotoImage(file='rf\\temc.png')
        self.canvas.create_image(600, 300, image=im)
        self.canvas.image = im

    def move_ball(self, *args):
        # 当鼠标在窗口中按下左键拖动的时候执行
        Widget.bind(self.canvas, "<Button-1>", self.mouseMove)
    def setup_UI(self):
        #在窗口画布

        def change():
            # cv2.imshow('1',manage.truck.panoimg)
            # cv2.waitKey(0)
            im1 = panorama.showStruct(manage.truck.panoimg,[], origin)
            im1 = cv2.resize(im1, (1200, 600), interpolation=cv2.INTER_CUBIC)
            # im1=np.resize(im1,(500,1000))
            cv2.imwrite('rf\\temc.png', im1)
            im = tk.PhotoImage(file='rf\\temc.png')
            self.canvas.create_image(600, 300, image=im)
            self.canvas.image = im
            self.rello=[]
        def save():
            manage.changerello(self.si,self.rello)
        self.canvas = Canvas(self, width =1200, height = 600, bg = "white")
        self.canvas.pack(side="top")
        origin=[manage.truck.initorigin[0]*manage.truck.scrrect[0],manage.truck.initorigin[1]*manage.truck.scrrect[1]]
        im1=panorama.showStruct(manage.truck.panoimg,manage.truck.struct_list[self.si].relLocation,origin)
        im1 = cv2.resize(im1, (1200, 600), interpolation=cv2.INTER_CUBIC)
        # im1=np.resize(im1,(500,1000))
        cv2.imwrite('rf\\temc.png',im1)
        im = tk.PhotoImage(file='rf\\temc.png')
        self.canvas.create_image(600, 300, image=im)
        self.canvas.image = im
        #创建frame的框架，窗口window为这个框架的父容器
        frame = Frame(self)
        frame.pack(side="top")
        #frame框架作为Button的父容器
        bt1 = Button(frame, text = "清空", command = change,width=20)

        bt1.grid(row = 1, column = 1)
        bt2 = Button(frame, text="保存", command=save,width=20)
        bt2.grid(row = 1, column = 2)
class Ppw(tk.Toplevel):
  def __init__(self,text):
    super().__init__()
    self.title('提示')
    # 弹窗界面
    self.setup_UI(text)
  def setup_UI(self,text):
    text1 =tk.StringVar()
    text1.set(text)
    lb = tk.Label(self, textvariable=text1)
    lb.grid(column=0, row=0)

  def ok(self):
    self.userinfo = [self.name.get(), self.age.get()] # 设置数据
    self.destroy() # 销毁窗口
class MyDialog(tk.Toplevel):
  def __init__(self):
    super().__init__()
    truck=manage.Truck()
    truck.reload()
    self.title('生产设置')
    # 弹窗界面
    self.setup_UI()
  def setup_UI(self):
    # 第一行（两列）
    frameLT = tk.Frame(self,width=500, height=320)
    frameRT =tk.Frame(self,width=200, height=500)
    # row1.pack(fill="x")
    # tk.Label(frameLT, text='姓名：', width=8).pack(side=tk.LEFT)
    # self.name = tk.StringVar()
    # tk.Entry(frameLT, textvariable=self.name, width=20).pack(side=tk.LEFT)
    # tk.Label(frameRT, text='姓名2：', width=8).pack(side=tk.LEFT)

    # # 第二行
    # row2 = tk.Frame(self)
    # row2.pack(fill="x", ipadx=1, ipady=1)
    # tk.Label(row2, text='年龄：', width=8).pack(side=tk.LEFT)
    # self.age = tk.IntVar()
    # tk.Entry(row2, textvariable=self.age, width=20).pack(side=tk.LEFT)
    # # 第三行
    # row3 = tk.Frame(self)
    # row3.pack(fill="x")
    # tk.Button(row3, text="取消", command=self.cancel).pack(side=tk.RIGHT)
    # tk.Button(row3, text="确定", command=self.ok).pack(side=tk.RIGHT)
    def showstr(*args):
        # label.destroy()
        si=number.get()
        cv2.imwrite('rf\\temc.png',manage.truck.struct_list[int(si)].img)
        im = tk.PhotoImage(file='rf\\temc.png', width=220, height=250)

        label = tk.Label(frameRT, image=im)
        label.image=im
        label.grid(row=0, column=4)
    def showproduct():
        si=int(number.get())
        list1 = manage.truck.struct_list[si].product_list
        for i1 in range(len(manage.truck.struct_list[si].product_list)):
            x = list1[i1]
            plt.subplot(len(manage.truck.struct_list[si].product_list), 2, 2 * i1 + 1)
            t = "物品编号：%s，预设生产量：%s" % (i1,x[1].N0)
            # t2 = "预设生产量：%s N1：%s " % (x[1].N0, x[1].N1)
            plt.text(150, 50, t, ha='left', fontsize=10, rotation=0, wrap=True,fontproperties="SimHei")
            # plt.text(150, 100, t2, ha='left', fontsize=10, rotation=0, wrap=True,fontproperties="SimHei")
            img1 = cv2.cvtColor(x[1].img, cv2.COLOR_BGR2RGB)
            plt.imshow(img1)
        plt.show()
    def changeN0():
        gi=int(self.goodi.get())
        ni=int(self.goodN0.get())
        si=int(number.get())
        manage.changeN0(si,gi,ni)

    def canvas():
        canvas= CanvasDemo(int(number.get()))
        canvas.geometry('1200x650+500+200')
        self.wait_window(canvas)  # 这一句很重要！！！


    text =tk.StringVar()
    text.set('建筑')
    lb = tk.Label(frameLT, textvariable=text)
    lb.grid(column=0, row=0)
    number = tk.StringVar()
    numberChosen = ttk.Combobox(frameLT,width=12, textvariable=number, state='readonly')
    numberChosen['values'] = list(range(20)) # 设置下拉列表的值
    numberChosen.bind("<<ComboboxSelected>>", showstr)
    numberChosen.grid(column=0, row=1)  # 设置其在界面中出现的位置  column代表列   row 代表行
    numberChosen.current(0)  # 设置下拉列表默认显示的值，0为 numberChosen['values'] 的下标值
    frameLT.grid(row=0, column=0, columnspan=2, padx=1, pady=0)
    frameRT.grid(row=0, column=3, columnspan=2, padx=1, pady=0)
    tk.Label(frameLT, text='物品编号：', width=10).grid(column=0, row=10)
    self.goodi = tk.IntVar()
    tk.Entry(frameLT, textvariable=self.goodi, width=10).grid(column=1, row=10)
    tk.Label(frameLT, text='预设生产量：', width=10).grid(column=0, row=11)
    self.goodN0 = tk.IntVar()
    tk.Entry(frameLT, textvariable=self.goodN0, width=10).grid(column=1, row=11)
    tk.Button(frameLT, text="储存",command=changeN0,width=10).grid(column=1,row=12)
    tk.Button(frameLT, text="生产品展示",command=showproduct,width=10).grid(column=1,row=1)
    tk.Button(frameLT, text="位置修改",command=canvas,width=10).grid(column=1,row=0)
    if 1:
        si = number.get()
        cv2.imwrite('rf\\temc.png', manage.truck.struct_list[int(si)].img)
        im = tk.PhotoImage(file='rf\\temc.png', width=220, height=250)
        label = tk.Label(frameRT, image=im)
        label.image = im
        label.grid(row=0, column=4)
  def ok(self):
    self.userinfo = [self.name.get(), self.age.get()] # 设置数据
    self.destroy() # 销毁窗口
  def cancel(self):
    self.userinfo = None # 空！
    self.destroy()
class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.pack()
        self.create_widgets()
    def create_widgets(self):
        def say_hi():
            for x in list1:
                x[0].changewhether(x[2].get())
        # print(CheckVar1.get())
        list1=[[manage.WHETHER_crop,'农田生产',0],[manage.WHETHER_farm,'牧场生产',0],[manage.WHETHER_struct,'建筑生产',0],[manage.WHETHER_sale,'售物贩卖',0],[manage.WHETHER_ship,'轮船订单',0]]
        for x in list1:
            x[2] = tk.IntVar()
            x[2].set(1)
            self.hi_there =tk.Checkbutton( text=x[1], variable=x[2], \
                     onvalue=1, offvalue=0, height=1, \
                     width=10)
            self.hi_there["command"] =say_hi
            self.hi_there.pack(side="left")

        # self.quit = tk.Button(self, text="QUIT", fg="red",
        #                       command=root.destroy)
        # self.quit.pack(side="right")
        def location():  # 当acction被点击时,该函数则生效z
            manage.getpanorama()
        def savelocation():
            manage.savepanorama()
        def run():
            judge=self.check()
            if judge==True:
                for i in range(1):
                    try:
                        manage.main()
                    except:
                        k = traceback.format_exc()
                        print(k)
                        self.ppw2(k)
                        # mouse1.moveTo(0.03, 0.08)
                        # time.sleep(0.5)
                        # mouse1.click()
                        # time.sleep(5)
            else:
                self.ppw1()
        # 按钮
        row4 = tk.Frame(self)
        row4.pack(fill="x")
        tk.Label(row4, text='序列号：', width=10).grid(column=0, row=9)
        # self.goodi = tk.IntVar()

        v = tk.StringVar(value=cpu.get_cpu_info())

        self.entry1=tk.Entry(row4, textvariable=v, width=20)
        self.entry1.grid(column=1, row=9)

        tk.Label(row4, text='注册码：', width=10).grid(column=0, row=11)
        self.password = tk.IntVar(value=manage.truck.password)
        tk.Entry(row4, textvariable=self.password, width=20).grid(column=1, row=11)
        # tk.Button(row4, text="登陆", pady=1,padx=30,command=self.check,bg='PaleGoldenrod',fg='black').grid(column=1, row=12)\
        self.action2 = tk.Button(self, text="开始运行",
                                 command=run,
                                 padx=200,pady=10,bg="LightSlateGray",font=10,
                                 fg="white")  # 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
        self.action2.pack(side="top", anchor=tk.N, expand='yes',fill='both')
        self.action = tk.Button(self, text="全局定位",
                            command=location,padx=30,bg='LightSlateGray',fg='white')  # 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
        self.action.pack(side="left")
        self.action1 = tk.Button(self, text="保存定位",
                                command=savelocation,padx=0,)  # 创建一个按钮, text：显示按钮上面显示的文字, command：当这个按钮被点击之后会调用command函数
        self.action1.pack(side="left")

        row3 = tk.Frame(self)
        row3.pack(fill="x")
        tk.Button(row3, text="生产设置", padx=20,command=self.setup_config,bg='PaleGoldenrod',fg='black').pack(side=tk.RIGHT,)
        # 设置参数
    def check(self):
            password=self.password.get()
            manage.changepassword(password)
            judge=cpu.check(encry=cpu.get_cpu_info(), password=password)
            return judge
    def setup_config(self):
        # 接收弹窗的数据
        inputDialog = MyDialog()
        inputDialog.geometry('500x500+500+200')
        self.wait_window(inputDialog)  # 这一句很重要！！！
    def ppw1(self):
        ppw1= Ppw(text='注册码错误，请查看帮助')
        ppw1.geometry('200x100+500+200')
    def ppw2(self,k):
        ppw1= Ppw(text=k)
        ppw1.geometry('500x300+500+200')

root = tk.Tk()
root.title('微爱Nana')
# root.wm_attributes('-topmost',1)
root.geometry('500x300+500+200')


app = Application(master=root)


app.mainloop()

