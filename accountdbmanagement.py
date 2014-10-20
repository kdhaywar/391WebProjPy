import os


__author__ = 'KyleHayward'

import cherrypy
import cx_Oracle
import hashlib, uuid




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
        sql = "select count(*) FROM users WHERE user_names == (%s)" %(uname)
        if cur.exeute(sql) == 1:
            cur.close()
            connection.close()
            return true

        cur.close()
        connection.close()
        return false



    def CheckIfEmailExists(self, email):
        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        #for sql injection
        #               cur.prepare('select * from departments where department_id = :id')
        #               cur.execute(None, {'id': 210})
        #               res = cur.fetchall()        
        sql = "select count(*) FROM persons WHERE email == (%s)" %(email)
        if cur.exeute(sql) == 1:
            cur.close()
            connection.close()
            return(true)

        cur.close()
        connection.close()
        return false










    def CreateUserAccount(self, fname, lname, address, email, phonenum, uname, password):
        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        current_date = sys.date()
        hashed_password = hashlib.sha512(password +uname).hexdigest()
        usersAccountSql = "insert into users(user_name, password, date_registered) values (%s %s %s)" %(uname, hashed_password, current_date)
        personsAccountSql ="insert into persons(user_name, first_name, last_name, address, email, phone) values (%s %s %s %s %s %s)" %(uname, fname, lname, address, email, phone)
        cur.execute(usersAccountSql)
        cur.execute(personsAccountSql)
        ## may need this connection.commit()
        cur.close()
        connection.close()
        return(true)





    def CheckLogin(self, uname, pword):
        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        #uncomment for hashed passwords
        #hashed_password = hashlib.sha512(password + uname).hexdigest()
        #sql = "select count(*) from users where user_name == %s and password == %s"  %(uname, hashed_password)
        #comment bellow for hashed pw
        sql = "select count(*) from users where user_name = '%s' and password = '%s'"  %(uname, pword)
        if cur.execute(sql) == 1:
            cur.close()
            connection.close()
            return True
        cur.close()
        connection.close()
        return False
