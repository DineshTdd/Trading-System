import cx_Oracle
con=cx_Oracle.connect('system/td1998@localhost')
cur=con.cursor()
class trader:
    def __init__(self):
        self.uname=None
        self.pwd=None
        self.accno=None
        self.uname1=None
    def create(self):
        self.uname=input("Enter username:")
        self.pwd=input("Enter password:")
        self.accno=input("Enter accno:")
        cur.execute("insert into trader values(:1,:2,:3)",(self.uname,self.pwd,self.accno))
        cur.execute("insert into account values(:1,:2)",(self.accno,500000.00))
    def login(self):
        uname1=input("USERNAME:")
        a=cur.execute("select uname from trader where uname='%s'"%(uname1))
        uname2=a.fetchone()
        c=uname2[0]
        if(uname1==c):
            pwd1=input("PASSWORD:")
            b=cur.execute("select pwd from trader where uname='%s'"%(uname1))
            pwd2=b.fetchone()
            d=pwd2[0]
            if(pwd1==d):
                print("Login successful")
            else:
                print("Enter the valid password!")
        else:
            print("Enter the valid username!")
    def sourcing(self):
        print("LIST OF AVAILABLE ITEMS\nPERFUMES:\n")
        cur.execute("select * from perfume")
        print(cur.fetchall())
        print("\nDOLLS:\n")
        cur.execute("select * from doll")
        print(cur.fetchall())
    def placeorder(self):
        i=item()
        a=admin()
        while(True):
            print("1.PERFUMES\t2.DOLLS\t3.View Bill\t4.Payment")
            cho=int(input("Enter your choice"))            
            if(cho==1):
                while(True):
                    itemid=int(input("Enter the item no to be purchased"))
                    noitem=int(input("Enter quantity to be purchased"))
                    num=int(1)
                    i.getperfume(itemid,noitem)
                    a.bill(itemid,noitem,num)
                    chy=input("Do you want to continue in perfumes section?\nThen press y if not press n")
                    if(chy=='n'):
                        break
            if(cho==2):        
                while(True):
                    itemid=int(input("Enter the item no to be purchased"))
                    noitem=int(input("Enter quantity to be purchased"))
                    num=int(2)
                    i.getdolls(itemid,noitem)
                    a.bill(itemid,noitem,num)
                    chy=input("Do you want to continue in doll section?\nThen press y if not press n")
                    if(chy=='n'):
                        break
            if(cho==3):
                a.traceorder()
            if(cho==4):
                break
        a.paybill()            
    def pay(self):
        cur.execute("drop table bill")        
    def logout(self):
        print("Thank you")
        exit(1)
class item(trader):
    def __init__(self):
        self.name=None
        self.id=None
        self.rate=None
        self.available=None
    def getperfume(self,itemid,noitem):
        ass=cur.execute("select available from perfume where id='%d'"%(itemid))
        avail=ass.fetchone()
        available=avail[0]
        available-=noitem
        cur.execute("update perfume set available='%d' where id='%d'"%(available,itemid))
    def getdolls(self,itemid,noitem):
        ass=cur.execute("select available from doll where id='%d'"%(itemid))
        avail=ass.fetchone()
        available=avail[0]
        available-=noitem
        cur.execute("update doll set available='%d' where id='%d'"%(available,itemid))
class account(trader):
    def __init__(self):
        trader.__init__(self)
        self.accno=None
        self.due=None
        self.balance=float(0)
    def accountno(self):
        while(True):
            user=input("Enter your username:")
            self.accno=int(input("Enter your account number:"))
            a=cur.execute("select accno from trader where uname='%s'"%(user))
            accno1=a.fetchone()
            c=accno1[0]
            if(self.accno==c):
                print("Your balance in your account:");
                ba=cur.execute("select balance from account where accno='%d'"%(self.accno))
                bal=ba.fetchone()
                self.balance=bal[0]
                print(self.balance)
                break
            else:
                print("Incorrect account number")
    def accountpay(self,totprice):
        self.totprice=totprice
        self.balance-=self.totprice
        print("Your balance after payment:'%f'"%(self.balance))
        cur.execute("update account set balance='%f' where accno='%d'"%(self.balance,self.accno))
        print("The bill has been paid\nGoods will be delivered shortly")                 
class admin(account):
    def __init__(self):
        self.name=None
        self.id=None
        self.totprice=float(0)
        cur.execute("create table bill (name varchar(16),id number(16),price float)")
    def bill(self,itemid,noitem,num):
        self.itemid=itemid
        self.noitem=noitem
        self.num=num
        if(num==1):
            r=cur.execute("select rate from perfume where id='%d'"%(itemid))            
            rate=r.fetchone()
            price=rate[0]
            itemprice=price*noitem
            n=cur.execute("select name from perfume where id='%d'"%(itemid))
            name=n.fetchone()
            itemname=name[0]
        elif(num==2):
            r=cur.execute("select rate from doll where id='%d'"%(itemid))            
            rate=r.fetchone()
            price=rate[0]
            itemprice=price*noitem
            n=cur.execute("select name from doll where id='%d'"%(itemid))
            name=n.fetchone()
            itemname=name[0]
        cur.execute("insert into bill values('%s','%d','%f')"%(itemname,itemid,itemprice))
        self.totprice+=itemprice
    def traceorder(self):
        print("Your bill")
        cur.execute("select * from bill")
        print(cur.fetchall())
        print("\nTotal Price:'%d'"%(self.totprice))
    def paybill(self):
        print("\nTotal Price:'%d'"%(self.totprice))
        ac=account()
        ac.accountno()
        ac.accountpay(self.totprice)                          
t=trader()
print("Welcome to FOREX SYSTEM")
ch=int(input("1.Existing user 2.New user\n Enter your choice:"))
if(ch==2):
    t.create()
    print("ACCOUNT created successfully")
print("LOGIN into your account") 
t.login()
t.sourcing()
t.placeorder()
t.pay()
t.logout()                    
con.commit()
con.close()


        
                    
        
                        
        
        
        
