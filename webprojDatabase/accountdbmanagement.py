
__author__ = 'KyleHayward'

import cx_Oracle
import time




##### TODO######
#prevent sql injections
#salt passwords maybe?
### user input contrants
# handle failed oracle connections


class AccountDbManagement:


    def CheckIfUsernameExists(self, uname):
        """
        Checks to see if the passed in username exists in the database.
        :param uname: The username to check for.
        :return: Boolean value based on whether the username was found or not.
        """
        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()

        #for sql injection
        #               cur.prepare('select * from departments where department_id = :id')
        #               cur.execute(None, {'id': 210})
        #               res = cur.fetchall()
        sql = "select count(*) FROM users WHERE user_name = '%s'" %(uname)

        cur.execute(sql)    
        numUname = cur.fetchall()
        if numUname == [(0,)]:
            cur.close()
            connection.close()
            return False
        else:
            cur.close()
            connection.close()
            return True


    def CheckIfEmailExists(self, email):
        """
        Checks to see if the passed in email address exists in the database.
        :param email: The email address to be checked against.
        :return: Boolean value based on whether or not the email is found.
        """
        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        #for sql injection
        #               cur.prepare('select * from departments where department_id = :id')
        #               cur.execute(None, {'id': 210})
        #               res = cur.fetchall()        
        sql = "select count(*) FROM persons WHERE email = '%s'" %(email)
        cur.execute(sql)    
        numEmail = cur.fetchall()
        if numEmail == [(0,)]:
            cur.close()
            connection.close()
            return False
        else:
            cur.close()
            connection.close()
            return True


    def CreateUserAccount(self, fname, lname, address, email, phonenum, uname, password):
        """
        Inserts a new user account into our databse.
        :param fname: The first name of the new account.
        :param lname: The last name of the new account.
        :param address: The address of the new account.
        :param email: The email address of the new account.
        :param phonenum: The phone number of the new account.
        :param uname: The username of the new account.
        :param password: The password of the new account.
        :return: True in all cases.
        """
        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()

        
        #hashed_password = hashlib.sha512(password +uname).hexdigest()
        
        usersAccountSql = "insert into users values ('%s', '%s', sysdate)" %(uname, password, current_date)
        personsAccountSql ="insert into persons values ('%s', '%s', '%s', '%s', '%s', '%s')" %(uname, fname, lname, address, email, phonenum)
        cur.execute(usersAccountSql)
        cur.execute(personsAccountSql)
        connection.commit()
        cur.close()
        connection.close()
        return True


    def CheckLogin(self, uname, pword):
        """
        Checks to see if the provided login information exists in the database.
        :param uname: The username to be checked for.
        :param pword: The password to be checked for.
        :return: Boolean depending on whether the provided username and password were found.
        """
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
        else:
            cur.close()
            connection.close()
            return False
