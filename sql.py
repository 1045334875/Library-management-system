from readline import insert_text
from datetime import date
from tkinter import messagebox
import pymysql
import tkinter as tk
from tkinter.messagebox import * 


class DB:
    def __init__(self):
        self.con=pymysql.connect(
            host='127.0.0.1',
            port=3306,
            user='root',
            password='11223344',
            database='lab5',
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor)
        self.cur = self.con.cursor()

    def query_sql(self,sql):
        self.cur.execute(sql)
        return self.cur.fetchall()

    def update_sql(self,sql):
        self.cur.execute(sql)
        self.con.commit()

    def close(self):
        self.cur.close()
        self.con.close()

class Identity:
    def __init__(self):
        self.db = DB()

    def login(self, userid, cipher):
        sql = "select root from card where userid = '{}' and secret = '{}'".format(userid, cipher)
        res = self.db.query_sql(sql)
        print(res)
        return res

    def checkID(self, name):
        sql = "select cardID from card where userid = '{}'".format(name)
        res = self.db.query_sql(sql)
        print(res)
        return res

    def changepwd(self, userid, cipher):
        sql = "update card set secret='{}' where cardID = '{}'".format(cipher,userid)
        self.db.update_sql(sql)

    def register(self, name, work, id, cipher):

        sql = "insert into card(username, userwork, userid, secret) value('{}','{}','{}','{}')".format(name, work, id, cipher)
        self.db.update_sql(sql)
        print("Insert successful!")

    def allIdentity(self):
        sql = "select cardID, username, userwork, userid, secret, root from card"
        res = self.db.query_sql(sql)
        return res

    def userIdentity(self,id):
        sql = f"select cardID, username, userwork, userid, secret, root from card where cardID={id}"
        res = self.db.query_sql(sql)
        return res

    def deleteCard(self, cardid):
        sql = f"delete from card where cardID = {cardid}"
        self.db.update_sql(sql)
        print("delete successful")

class Books:
    def __init__(self):
        self.db = DB()
        self.identity = Identity()
        #self.returnBook(1,7)

    def insertBook(self, bno, category, title, press, year, author, price, total, stock):
        sql = "insert into book(bno, category, title, press, year, author, price, total, stock) value('{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(bno,category,title,press, year, author, price, total, stock)
        self.db.update_sql(sql)

    def allBook(self):
        sql = "select bno, category, title, press, year, author, price, total, stock from book"
        res_book = self.db.query_sql(sql)
        return res_book

    def queryBookbyName(self,name):
        sql = f'select * from book where title="{name}" '
        res_books = self.db.query_sql(sql)
        #print("图书详细信息",res_books[0])
        return res_books

    def queryBookbyAuthor(self,name):
        sql = f'select * from book where author="{name}" '
        res_books = self.db.query_sql(sql)
        #print("图书详细信息",res_books[0])
        return res_books

    def queryBookbyCategory(self,name):
        sql = f'select * from book where category="{name}" '
        res_books = self.db.query_sql(sql)
        return res_books

    def queryBookbyPress(self,name):
        sql = f'select * from book where press="{name}" '
        res_books = self.db.query_sql(sql)
        return res_books

    def lendBook(self,cardID, bno):
        sql = f'select id from lendrecord where cardID="{cardID}" and bno="{bno}" '
        lendid=0
        lendid = self.db.query_sql(sql)
        if lendid != ():
            print(lendid)
            print("Has record")
            return 2
        sql = f'select stock from book where bno="{bno}" '
        stock = self.db.query_sql(sql)
        newstock = stock[0]['stock']-1
        if int(newstock) >= 0:
            todate=date.today() 
            #add lend record
            sql = "insert into lendrecord(cardID, bno, lendDate) value('{}','{}','{}')".format(cardID, bno, todate)
            self.db.update_sql(sql)
            #update book stock
            sql = f"update book set stock={newstock} where bno = {bno}"
            self.db.update_sql(sql)
            print("Lend book successful")
            return 1
        else: return 0

    def returnBook(self, id):
        todate= date.today()
        print(todate)
        #record return time
        sql2 = 'update lendrecord set backDate="{}" where id="{}"'.format(todate,id)
        self.db.update_sql(sql2)
        #update stock
        sql = f'select bno from lendrecord where id="{id}" '
        bno = self.db.query_sql(sql)
        bbno = bno[0]['bno']
        print(bbno)
        sql = f'select stock from book where bno="{bbno}" '
        stock = self.db.query_sql(sql)
        print(stock)
        newstock = stock[0]['stock']+1
        sql = f"update book set stock={newstock} where bno = {bbno}"
        self.db.update_sql(sql)

        print("Return book successful")
        return 1


    def deleteBook(self,bno):
        sql = f'delete from book where bno={bno}'
        self.db.update_sql(sql)

    def allRecord(self):
        sql = "select id, lendrecord.cardID, card.username, lendrecord.bno, book.title, lendDate, backDate from lendrecord, book, card where book.bno=lendrecord.bno and card.cardID=lendrecord.cardID"
        res_record = self.db.query_sql(sql)
        return res_record

    def queryRecordbyName(self,name):
        sql = f"select id, lendrecord.cardID, card.username, lendrecord.bno, book.title, lendDate, backDate from lendrecord, book, card where book.bno=lendrecord.bno and card.cardID=lendrecord.cardID and card.username={name} and backDate is null"
        res_record = self.db.query_sql(sql)
        return res_record

    def queryRecordbyId(self,name):
        sql = f"select id, lendrecord.cardID, card.username, lendrecord.bno, book.title, lendDate, backDate from lendrecord, book, card where book.bno=lendrecord.bno and card.cardID=lendrecord.cardID and card.cardID={name} and backDate is null"
        res_record = self.db.query_sql(sql)
        return res_record

    def queryAllRecordbyId(self,name):
        sql = f"select id, lendrecord.cardID, card.username, lendrecord.bno, book.title, lendDate, backDate from lendrecord, book, card where book.bno=lendrecord.bno and card.cardID=lendrecord.cardID and card.cardID={name}"
        res_record = self.db.query_sql(sql)
        return res_record


    def deleteRecord(self,id):
        sql = f'delete from lendrecord where id = {id}'
        self.db.update_sql(sql)
