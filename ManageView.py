from tkinter import *
from tkinter.messagebox import * 
from tkinter import ttk
from sql import Books, Identity
 
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
        Label(self, text='插入图书', font=("华文行楷", 20), justify = CENTER , fg="#86967e",bg="#fffaf4").grid(row=0, pady=10) 
        
        Label(self, text = '书籍编号: ',bg="#fffaf4").grid(row=1, stick=W, pady=10) 
        Entry(self, textvariable=self.bno).grid(row=1, column=1, stick=E) 
        Label(self, text = '书籍类型: ',bg="#fffaf4").grid(row=2, stick=W, pady=10) 
        Entry(self, textvariable=self.category).grid(row=2, column=1, stick=E) 
        Label(self, text = '书籍名称: ',bg="#fffaf4").grid(row=3, stick=W, pady=10) 
        Entry(self, textvariable=self.title).grid(row=3, column=1, stick=E) 
        Label(self, text = '出版社: ',bg="#fffaf4").grid(row=4, stick=W, pady=10) 
        Entry(self, textvariable=self.press).grid(row=4, column=1, stick=E) 
        Label(self, text = '出版日期: ',bg="#fffaf4").grid(row=5, stick=W, pady=10) 
        Entry(self, textvariable=self.year).grid(row=5, column=1, stick=E) 
        Label(self, text = '作者: ',bg="#fffaf4").grid(row=6, stick=W, pady=10) 
        Entry(self, textvariable=self.author).grid(row=6, column=1, stick=E) 
        Label(self, text = '价格: ',bg="#fffaf4").grid(row=7, stick=W, pady=10) 
        Entry(self, textvariable=self.price).grid(row=7, column=1, stick=E) 
        Label(self, text = '总量: ',bg="#fffaf4").grid(row=8, stick=W, pady=10) 
        Entry(self, textvariable=self.total).grid(row=8, column=1, stick=E) 
        Label(self, text = '在库数量: ',bg="#fffaf4").grid(row=9, stick=W, pady=10) 
        Entry(self, textvariable=self.stock).grid(row=9, column=1, stick=E) 
        Button(self, text='录入', command=self.insertBook).grid(row=10, column=0, stick=E, pady=10) 

    def insertBook(self):
        bno = self.bno.get() 
        category = self.category.get() 
        title = self.title.get()
        press = self.press.get()
        year = self.year.get()
        author = self.author.get()
        price = self.price.get()
        total = self.total.get()
        stock = self.stock.get()
        if bno == '' or title == '' or category == '' or press == '' or year == '' or author == '' or price == '' or total == '' or stock == ''  :
            showinfo('警告！','请输入完整信息！')
        else: 
            Books().insertBook(bno, category, title, press, year, author, price, total, stock)
            showinfo('提示','插入图书成功')

#show all the lend record
class QueryFrame(Frame): # 继承Frame类 
    def __init__(self, master=None): 
        Frame.__init__(self, master) 
        self.root = master #定义内部变量root 
        self.itemName = StringVar() 
        self.createPage() 

    def createPage(self): 
        self.configure(bg="#fffaf4") 
        Label(self, text='借阅记录', font=("华文行楷", 20), fg="#86967e",bg="#fffaf4").pack() 
        column = ['id', 'bno', 'title', 'cardID', 'username', 'lendDate', 'backDate']
        text_arr = ['编号','书籍编号','书名','借书证号','借阅人','借出时间','归还时间']
        self.tree = ttk.Treeview(self, show="headings", columns=column)

        #print the heading of book lists
        for i in range(len(column)):
            self.tree.heading(column[i], text=text_arr[i])
            self.tree.column(column[i],width=100,anchor='center')
        self.tree.place(x=200,y=20,width=900,height=900)
        self.tree.pack()#一定要加这个pack，才能让表格显示出来
        record_arr = Books().allRecord()

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
                self.tree.insert('','end',values=values)
            
        except:
            showinfo('警告！','获取借阅数据失败！')

        Button(self ,text='删除图书',command=self.deleterecord).pack()

    def deleterecord(self):
        id = 0
        curitem = self.tree.focus()
        card = self.tree.item(curitem,option='values')
        if(card != ''): id = card[0]
        if id == 0:
            showinfo('警告！',"请点击借阅信息再删除")
        else: 
            Books().deleteRecord(id)
            self.tree.delete(curitem)
            showinfo('提示',"删除借阅信息成功！")

#show all users 
class CountFrame(Frame): # 继承Frame类 
    def __init__(self, master=None): 
        Frame.__init__(self, master) 
        self.root = master #定义内部变量root 
        self.createPage() 


    def createPage(self): 
        self.configure(bg="#fffaf4") 
        Label(self, text='管理用户', font=("华文行楷", 20), fg="#86967e",bg="#fffaf4").pack() 
        column = ['cardID', 'username', 'userwork', 'userid', 'secret', 'root']
        text_arr = ['编号','用户姓名','用户工作','账号','密码','管理员']
        self.tree = ttk.Treeview(self, show="headings", columns=column)

        #print the heading of book lists
        for i in range(len(column)):
            self.tree.heading(column[i], text=text_arr[i])
            self.tree.column(column[i],width=100,anchor='center')
        self.tree.place(x=200,y=20,width=900,height=900)
        self.tree.pack()#一定要加这个pack，才能让表格显示出来
        book_arr = Identity().allIdentity()
        
        try:
            for book in book_arr:
                values=[]
                #print(book)
                values.append(book['cardID'])
                values.append(book["username"])
                values.append(book["userwork"])
                values.append(book["userid"])
                values.append(book["secret"])
                values.append(book["root"])
                self.tree.insert('','end',values=values)
        except:
            showinfo('警告！','获取用户数据失败！')

        Button(self ,text='删除用户',command=self.deleteuser).pack()
        Button(self ,text='设置为管理员',command=self.upUserRoot).pack()

    def deleteuser(self):
        cardid = 0
        curitem = self.tree.focus()
        card = self.tree.item(curitem,option='values')
        if(card != ''): cardid = card[0]
        print(cardid)
        if cardid == 0:
            showinfo('警告！',"请点击用户信息再删除")
        else: 
            Identity().deleteCard(cardid)
            self.tree.delete(curitem)
            print("Delete successful")
            showinfo('提示',"删除用户信息成功！")

    def upUserRoot(self):
        cardid = 0
        curitem = self.tree.focus()
        card = self.tree.item(curitem,option='values')
        if(card != ''): cardid = card[0]
        print(cardid)
        if cardid == 0:
            showinfo('警告！',"请点击用户信息再进行授权")
        else: 
            Identity().setroot(cardid)
            card = list(card)
            card[5]=1
            card = tuple(card)
            self.tree.item(curitem,values=card)
            print("Delete successful")
            showinfo('提示',"用户授权管理员成功！")




#Show all the books
class AboutFrame(Frame): # 继承Frame类 
    def __init__(self, master=None): 
        Frame.__init__(self, master) 
        self.root = master #定义内部变量root 
        self.createPage() 

    def createPage(self): 
        self.configure(bg="#fffaf4") 
        Label(self, text='所有图书', font=("华文行楷", 20), fg="#86967e",bg="#fffaf4").pack() 
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

        Button(self ,text='删除图书',command=self.deletebook).pack()

    def deletebook(self):
        bno = 0
        curitem = self.tree.focus()
        card = self.tree.item(curitem,option='values')
        if(card != ''): bno = card[0]
        print(bno)
        if bno == 0:
            showinfo('警告！',"请点击图书信息再删除")
        else: 
            Books().deleteBook(bno)
            self.tree.delete(curitem)
            showinfo('提示',"删除图书信息成功！")

