
__author__ = 'KyleHayward'

import cx_Oracle
import time



#TODO handle failed oracle connections


class AccountDbManagement:


    def CheckIfUsernameExists(self, uname):
        """
        Checks to see if the passed in username exists in the database.
        :param uname: The username to check for.
        :return: Boolean value based on whether the username was found or not.
        """
        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        query = "select count(*) FROM users WHERE user_name = :uname"
        cur.execute(query, {'uname':uname})    
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
        query = "select count(*) FROM persons WHERE email = :email"
        cur.execute(query, {'email':email})    
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
        
        usersInsert = "insert into users( user_name, password, date_registered) values (:uname, :password, sysdate)"
        personsInsert ="insert into persons(user_name, first_name, last_name, address, email, phone) values ( :uname, :fname, :lname, :address, :email, :phonenum)"
        cur.execute(usersInsert, {'uname':uname, 'password':password})
        cur.execute(personsInsert, {'uname':uname, 'fname':fname, 'lname':lname, 'address':address, 'email':email, 'phonenum':phonenum})
        connection.commit()
        cur.close()
        connection.close()
        return True


    def CheckLogin(self, uname, password):
        """
        Checks to see if the provided login information exists in the database.
        :param uname: The username to be checked for.
        :param pword: The password to be checked for.
        :return: Boolean depending on whether the provided username and password were found.
        """
        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        
        query = "select count(*) from users where user_name = :uname and password = :password"
        cur.execute(query, {'uname':uname, 'password':password})
        validUnamePword = cur.fetchall()
        if validUnamePword == [(1,)]:
            cur.close()
            connection.close()
            return True
        else:
            cur.close()
            connection.close()
            return False
