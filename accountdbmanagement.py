import os


__author__ = 'KyleHayward'

import cherrypy
import cx_Oracle
import hashlib, uuid
import datetime
import time




##### TODO######
#prevent sql injections
#salt passwords maybe?
### user input contrants
# handle failed oracle connections


class AccountDbManagement:

    def CheckIfUsernameExists(self, uname):
        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()

        #for sql injection
        #               cur.prepare('select * from departments where department_id = :id')
        #               cur.execute(None, {'id': 210})
        #               res = cur.fetchall()
        sql = "select count(*) FROM users WHERE user_name = '%s'" %(uname)

        cur.execute(sql)    
        numberOfMatchingUname = cur.fetchall()
        if numberOfMatchingUname == [(0,)]:

            cur.close()
            connection.close()
            return False

        cur.close()
        connection.close()
        return True



    def CheckIfEmailExists(self, email):
        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        #for sql injection
        #               cur.prepare('select * from departments where department_id = :id')
        #               cur.execute(None, {'id': 210})
        #               res = cur.fetchall()        
        sql = "select count(*) FROM persons WHERE email = '%s'" %(email)
        cur.execute(sql)    
        numberOfMatchingEmail = cur.fetchall()        
        if numberOfMatchingEmail == [(0,)]:
            cur.close()
            connection.close()
            return False

        cur.close()
        connection.close()
        return True










    def CreateUserAccount(self, fname, lname, address, email, phonenum, uname, password):
        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        current_date =[]
        current_date = time.strftime('%m-%d-%Y')
        
        #hashed_password = hashlib.sha512(password +uname).hexdigest()
        
        usersAccountSql = "insert into users values ('%s', '%s', to_date('%s','MM-DD-YYYY'))" %(uname, password, current_date)
        personsAccountSql ="insert into persons values ('%s', '%s', '%s', '%s', '%s', '%s')" %(uname, fname, lname, address, email, phonenum)
        cur.execute(usersAccountSql)
        cur.execute(personsAccountSql)
        connection.commit()
        cur.close()
        connection.close()
        return True





    def CheckLogin(self, uname, pword):
        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        #uncomment for hashed passwords
        #hashed_password = hashlib.sha512(password + uname).hexdigest()
        #sql = "select count(*) from users where user_name == %s and password == %s"  %(uname, hashed_password)
        #comment bellow for hashed pw
        sql = "select count(*) from users where user_name = '%s' and password = '%s'"  %(uname, pword)
        cur.execute(sql)
        validUnamePword = cur.fetchall()
        if validUnamePword == [(1,)]:
            cur.close()
            connection.close()
            return True
        cur.close()
        connection.close()
        return False
