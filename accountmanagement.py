import os
from accountdbmanagement import AccountDbManagement
import cherrypy

__author__ = 'KyleHayward'



class AccountManagement(object):



    def UserLogin(self, uname, password):


        x = AccountDbManagement()
        if x.CheckLogin(uname, password):
            return True 
        
        return False













    def CreateUserAccount(self, fname, lname, address, email, phonenum, uname, password, passconf):

        ###todo###
        ## check user input contraints
        ##check if password is null
        x = AccountDbManagement()
        if x.CheckIfUsernameExists(uname):
        ###username already exists
            return False
 

        elif x.CheckIfEmailExists(email):
        ##email already exists
            return False
    
    
        elif password != passconf or password == True:
            ##password and passconf do not match
            return False
    
        else:
            x.CreateUserAccount(fname, lname, address, email, phonenum, uname, password)
            
        return True