from tkinter import * 
from tkinter.messagebox import * 
import hashlib
from sql import Identity
from LoginPage import *
from MainPage import *
from Loginstate import *

class RegisterPage(object): 
    def __init__(self, master=None): 
        self.root = master #定义内部变量root 
        self.root.configure(bg="#fffaf4")
        self.root.geometry("1200x600+200+80")
        self.username = StringVar() 
        self.password = StringVar() 
        self.userid = StringVar()
        self.userwork = StringVar()
        self.createPage() 
 
    def createPage(self): 
        self.page = Frame(self.root) #创建Frame 
        self.page.pack() 
        self.page.configure(bg="#fffaf4") 
        Label(self.page, text='用户注册', font=("华文行楷", 20), fg="#86967e",bg="#fffaf4").grid(row=0, stick=W) 
        Label(self.page, text = '真实姓名: ',bg="#fffaf4").grid(row=1, stick=W, pady=12) 
        Entry(self.page, textvariable=self.username).grid(row=1, column=1, stick=E) 
        Label(self.page, text = '工作: ',bg="#fffaf4").grid(row=2, stick=W, pady=12) 
        Entry(self.page, textvariable=self.userwork).grid(row=2, column=1, stick=E) 
        Label(self.page, text = '用户名: ',bg="#fffaf4").grid(row=3, stick=W, pady=10) 
        Entry(self.page, textvariable=self.userid).grid(row=3, column=1, stick=E) 
        Label(self.page, text = '密码: ',bg="#fffaf4").grid(row=4, stick=W, pady=10) 
        Entry(self.page, textvariable=self.password, show='*').grid(row=4, column=1, stick=E) 
        Button(self.page, text='注册', command=self.commitRegister).grid(row=5, stick=W, pady=10) 
        Button(self.page, text='退出', command=self.root.quit).grid(row=5, column=2, stick=E) 

    def commitRegister(self): 
        name = self.username.get() 
        work = self.userwork.get() 
        id = self.userid.get() 
        secret = self.password.get() 
        encrypt=hashlib.md5(secret.encode()).hexdigest()
        Identity().register(name,work,id,encrypt)
        cardid = Identity().checkID(id)
        print(cardid)
        Loginstate().update(cardid[0]['cardID'])
        print(Loginstate().search)
        self.page.destroy() 
        MainPage(self.root) 
    