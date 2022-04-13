from tkinter import * 
from tkinter.messagebox import * 
from MainPage import * 
from ManagerPage import *
from RegisterPage import *
from Loginstate import *
from sql import Identity
from MainPage import *
import hashlib
 
class LoginPage(object): 
    def __init__(self, master=None): 
        self.root = master #定义内部变量root 
        self.root.configure(bg="#fffaf4")
        self.root.geometry("1200x600+200+80")
        self.username = StringVar() 
        self.password = StringVar() 
        self.createPage() 
 
    def createPage(self): 
        self.page = Frame(self.root) #创建Frame 
        self.page.pack() 
        Label(self.page).grid(row=0, stick=W) 
        Label(self.page, text = '账户: ').grid(row=1, stick=W, pady=10) 
        Entry(self.page, textvariable=self.username).grid(row=1, column=1, stick=E) 
        Label(self.page, text = '密码: ').grid(row=2, stick=W, pady=10) 
        Entry(self.page, textvariable=self.password, show='*').grid(row=2, column=1, stick=E) 
        Button(self.page, text='登陆', command=self.loginCheck).grid(row=3, stick=W, pady=10) 
        Button(self.page, text='注册', command=self.register).grid(row=3, column=1, stick=E) 

    def loginCheck(self): 
        name = self.username.get() #userid actually
        secret = self.password.get() 
        encrypt=hashlib.md5(secret.encode()).hexdigest()
        value = Identity().login(name,encrypt)
        Loginstate().update(name)
        if value[0]['root'] == 1: 
            self.page.destroy() 
            MainPage(self) 
        elif value[0]['root'] == 0:
            self.page.destroy() 
            ManagerPage(self.root) 
        else: 
            showinfo(title='错误', message='账号或密码错误！') 

    def register(self):
        self.page.destroy()
        RegisterPage(self.root)

