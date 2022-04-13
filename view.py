from struct import pack
from tkinter import * 
from tkinter.messagebox import * 
from tkinter import ttk
from sql import Books, Identity
from Loginstate import *
import hashlib
 
#insert a book
class InputFrame(Frame): # 继承Frame类 
    def __init__(self, master=None): 
        Frame.__init__(self, master) 
        self.root = master #定义内部变量root 
        self.bno = StringVar() 
        self.category = StringVar() 
        self.title = StringVar() 
        self.press= StringVar() 
        self.year = StringVar() 
        self.author = StringVar() 
        self.price = StringVar() 
        self.total= StringVar() 
        self.stock= StringVar() 
        self.createPage() 

    def createPage(self): 
        self.configure(bg="#fffaf4") 
        Label(self, text='查询图书', font=("华文行楷", 20), justify = CENTER , fg="#86967e",bg="#fffaf4").pack()
        Label(self, text = '书籍类型: ',bg="#fffaf4").pack()
        Entry(self, textvariable=self.category).pack()
        Label(self, text = '书籍名称: ',bg="#fffaf4").pack()
        Entry(self, textvariable=self.title).pack()
        Label(self, text = '出版社: ',bg="#fffaf4").pack()
        Entry(self, textvariable=self.press).pack()
        Label(self, text = '作者: ',bg="#fffaf4").pack()
        Entry(self, textvariable=self.author).pack()
        Button(self, text='查询', command=self.checkBook).pack()

        column = ['bno', 'category', 'title', 'press', 'year', 'author', 'price', 'total', 'stock']
        text_arr = ['编号','类型','书名','出版社','出版日期','作者','价格','总量','在库']
        self.tree = ttk.Treeview(self, show="headings", columns=column)
    
        #print the heading of book lists
        for i in range(len(column)):
            self.tree.heading(column[i], text=text_arr[i])
            self.tree.column(column[i],width=100,anchor='center')
        self.tree.place(x=200,y=200,width=900,height=900)
        self.tree.pack()#一定要加这个pack，才能让表格显示出来
        Button(self ,text='借阅图书',command=self.lendbook).pack()


    def addResult(self,book_arr):
        try:
            for book in book_arr:
                values=[]
                print(book)
                values.append(book['bno'])
                values.append(book["category"])
                values.append(book["title"])
                values.append(book["press"])
                values.append(book["year"])
                values.append(book["author"])
                values.append(book["price"])
                values.append(book["total"])
                values.append(book["stock"])
                self.tree.insert('','end',values=values)
        except:
            showinfo('警告！','获取图书数据失败！')

    def lendbook(self):
        bno = 0
        curitem = self.tree.focus()
        card = self.tree.item(curitem,option='values')
        if(card != ''): bno = card[0]
        print(card[-1])
        newstock = int(card[-1])
        newstock = newstock-1
        print(newstock)
        if bno == 0:
            showinfo('警告！',"请点击图书信息再借阅")
        else: 
            res = Books().lendBook(Loginstate().search,bno)
            if res==1:
                showinfo('提示',"借阅图书成功！")
                card = list(card)
                card[8]=newstock
                card = tuple(card)
                print(card)
                #self.tree.delete(curitem)
                self.tree.item(curitem,values=card)
            else:
                showinfo('提示','库存不够了，请等待还书！')



    def checkBook(self):
        x=self.tree.get_children()
        for item in x:
            self.tree.delete(item)
        bno = self.bno.get() 
        category = self.category.get() 
        title = self.title.get()
        press = self.press.get()
        year = self.year.get()
        author = self.author.get()
        price = self.price.get()
        total = self.total.get()
        stock = self.stock.get()
        if(title != ''):
            res=[]
            res = Books().queryBookbyName(title)
            self.addResult(res)
        if(press != ''):
            res=[]
            res = Books().queryBookbyPress(press)
            self.addResult(res)

        if(author != ''):
            res=[]
            res = Books().queryBookbyAuthor(author)
            self.addResult(res)

        if(category != ''):
            res=[]
            res = Books().queryBookbyCategory(category)
            self.addResult(res)
        print("Insert successful")

#show all the lend record
class QueryFrame(Frame): # 继承Frame类 
    def __init__(self, master=None): 
        Frame.__init__(self, master) 
        self.root = master #定义内部变量root 
        self.itemName = StringVar() 
        self.createPage() 

    def createPage(self): 
        self.configure(bg="#fffaf4") 
        Label(self, text='归还图书', font=("华文行楷", 20), fg="#86967e",bg="#fffaf4").pack() 
        column = ['id', 'bno', 'title', 'cardID', 'username', 'lendDate', 'backDate']
        text_arr = ['编号','书籍编号','书名','借书证号','借阅人','借出时间','归还时间']
        self.tree = ttk.Treeview(self, show="headings", columns=column)

        #print the heading of book lists
        for i in range(len(column)):
            self.tree.heading(column[i], text=text_arr[i])
            self.tree.column(column[i],width=100,anchor='center')
        self.tree.place(x=200,y=20,width=900,height=900)
        self.tree.pack()#一定要加这个pack，才能让表格显示出来
        userid = Loginstate().search
        print(userid)
        record_arr = Books().queryRecordbyId(1)

        try:
            for record in record_arr:
                values=[]
                values.append(record['id'])
                values.append(record["bno"])
                values.append(record["title"])
                values.append(record["cardID"])
                values.append(record["username"])
                values.append(record["lendDate"])
                values.append(record["backDate"])
                #print(values)
                self.tree.insert('','end',values=values)
        except:
            showinfo('警告！','获取借阅数据失败！')

        Button(self ,text='归还图书',command=self.returnbook).pack()

    def returnbook(self):
        id = 0
        curitem = self.tree.focus()
        card = self.tree.item(curitem,option='values')
        if(card != ''): id = card[0]
        if id == 0:
            showinfo('警告！',"请点击借阅信息再归还")
        else: 
            Books().returnBook(id)
            self.tree.delete(curitem)
            showinfo('提示',"归还图书成功！")


#show all users 
class CountFrame(Frame): # 继承Frame类 
    def __init__(self, master=None): 
        Frame.__init__(self, master) 
        self.root = master #定义内部变量root 
        self.createPage() 

    def createPage(self): 
        self.configure(bg="#fffaf4") 
        Label(self, text='借阅图书', font=("华文行楷", 20), fg="#86967e",bg="#fffaf4").pack() 
        column = ['bno', 'category', 'title', 'press', 'year', 'author', 'price', 'total', 'stock']
        text_arr = ['编号','类型','书名','出版社','出版日期','作者','价格','总量','在库']
        self.tree = ttk.Treeview(self, show="headings", columns=column)
    
        #print the heading of book lists
        for i in range(len(column)):
            self.tree.heading(column[i], text=text_arr[i])
            self.tree.column(column[i],width=100,anchor='center')
        self.tree.place(x=200,y=20,width=900,height=1900)
        self.tree.pack()#一定要加这个pack，才能让表格显示出来
        book_arr = Books().allBook()
        
        try:
            for book in book_arr:
                values=[]
                values.append(book['bno'])
                values.append(book["category"])
                values.append(book["title"])
                values.append(book["press"])
                values.append(book["year"])
                values.append(book["author"])
                values.append(book["price"])
                values.append(book["total"])
                values.append(book["stock"])
                self.tree.insert('','end',values=values)
        except:
            showinfo('警告！','获取图书数据失败！')

        Button(self ,text='借阅图书',command=self.lendbook).pack()

    def lendbook(self):
        bno = 0
        curitem = self.tree.focus()
        card = self.tree.item(curitem,option='values')
        if(card != ''): bno = card[0]
        print(card[-1])
        newstock = int(card[-1])
        newstock = newstock-1
        print(newstock)
        if bno == 0:
            showinfo('警告！',"请点击图书信息再借阅")
        else: 
            res = Books().lendBook(Loginstate().search,bno)
            if res==1:
                showinfo('提示',"借阅图书成功！")
                card = list(card)
                card[8]=newstock
                card = tuple(card)
                print(card)
                #self.tree.delete(curitem)
                self.tree.item(curitem,values=card)
            elif res==2:
                showinfo('警告！',"您已经借阅此图书，请归还再借阅！")
            else:
                showinfo('警告','库存不够，请等待还书！')




#Show all the books
class AboutFrame(Frame): # 继承Frame类 
    def __init__(self, master=None): 
        Frame.__init__(self, master) 
        self.root = master #定义内部变量root 
        self.password = StringVar()
        self.createPage() 

    def createPage(self): 
        self.configure(bg="#fffaf4") 
        Label(self, text='个人信息', font=("华文行楷", 20), fg="#86967e",bg="#fffaf4").pack() 
        userInf = Identity().userIdentity(1)#Loginstate().search)
        Label(self, text=('卡号:  '+str(userInf[0]["cardID"])),bg="#fffaf4").pack()
        Label(self, text=('姓名:  '+userInf[0]["username"]),bg="#fffaf4").pack()
        Label(self, text=('工作:  '+userInf[0]["userwork"]),bg="#fffaf4").pack()
        Label(self, text=('ID:  '+userInf[0]["userid"]),bg="#fffaf4").pack()
        Entry(self, textvariable=self.password).pack()
        Button(self, text='更改密码', command=self.changepwd).pack()

        column = ['id', 'bno', 'title', 'cardID', 'username', 'lendDate', 'backDate']
        text_arr = ['编号','书籍编号','书名','借书证号','借阅人','借出时间','归还时间']
        self.tree = ttk.Treeview(self, show="headings", columns=column)

        #print the heading of book lists
        for i in range(len(column)):
            self.tree.heading(column[i], text=text_arr[i])
            self.tree.column(column[i],width=100,anchor='center')
        self.tree.place(x=200,y=20,width=900,height=900)
        self.tree.pack()#一定要加这个pack，才能让表格显示出来
        userid = Loginstate().search
        print(userid)
        record_arr = Books().queryAllRecordbyId(1)

        try:
            for record in record_arr:
                values=[]
                values.append(record['id'])
                values.append(record["bno"])
                values.append(record["title"])
                values.append(record["cardID"])
                values.append(record["username"])
                values.append(record["lendDate"])
                if record["backDate"]==None:
                    values.append("待归还")
                else: values.append(record["backDate"])
                #print(values)
                self.tree.insert('','end',values=values)
        except:
            showinfo('警告！','获取借阅数据失败！')

    def changepwd(self):
        secret = self.password.get()
        encrypt=hashlib.md5(secret.encode()).hexdigest()
        Identity().changepwd(1,encrypt)
        showinfo('提示','密码更改成功')