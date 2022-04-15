from tkinter import * 
from view import * #菜单栏对应的各个子页面 
 
class MainPage(object): 
    def __init__(self, master=None): 
        self.root = master #定义内部变量root 
        self.root.configure(bg="#fffaf4")
        self.root.geometry("1200x600+200+80")
        self.createPage() 
 
    def createPage(self): 
        self.inputPage = InputFrame(self.root) # 创建不同Frame 
        self.queryPage = QueryFrame(self.root) 
        self.countPage = CountFrame(self.root) 
        self.aboutPage = AboutFrame(self.root) 
        self.inputPage.pack() #默认显示数据录入界面 
        menubar = Menu(self.root) 
        menubar.add_command(label='图书查询', command = self.inputData) 
        menubar.add_command(label='归还图书', command = self.queryData) 
        menubar.add_command(label='借阅图书', command = self.countData) 
        menubar.add_command(label='个人界面', command = self.aboutDisp) 
        self.root['menu'] = menubar # 设置菜单栏 

    def inputData(self): 
        self.inputPage = InputFrame(self.root)
        self.inputPage.pack() 
        self.queryPage.pack_forget() 
        self.countPage.pack_forget() 
        self.aboutPage.pack_forget() 

    def queryData(self): 
        self.queryPage = QueryFrame(self.root)
        print("update")
        self.inputPage.pack_forget() 
        self.queryPage.pack() 
        self.countPage.pack_forget() 
        self.aboutPage.pack_forget() 

    def countData(self): 
        self.countPage = CountFrame(self.root)
        self.inputPage.pack_forget() 
        self.queryPage.pack_forget() 
        self.countPage.pack() 
        self.aboutPage.pack_forget() 

    def aboutDisp(self): 
        self.aboutPage = AboutFrame(self.root)
        self.inputPage.pack_forget() 
        self.queryPage.pack_forget() 
        self.countPage.pack_forget() 
        self.aboutPage.pack() 
