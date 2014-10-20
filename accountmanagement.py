import os
from accountdbmanagement import AccountDbManagement
import cherrypy

__author__ = 'KyleHayward'



class AccountManagement(object):



    def UserLogin(self, uname, password):


        x = AccountDbManagement()
        if x.CheckLogin(uname, password):
            return(true)

        #if CheckLogin(self, uname, password):
         #   return(true)

        
        return(0)













    def CreateUserAccount(self, fname, lname, address, email, phonenum, uname, password, passconf):

        ###todo###
        ## check user input contraints

        if CheckIfUsernameExists(uname):
        ###username already exists
            return(false)
 

        elif CheckIfEmailExists(email):
        ##email already exists
            return(false)
    
    
        elif password != passconf:
            ##password and passconf do not match
            return(false)
    
        else:
            CreateUserAccount(fname, lname, address, email, phonenum, uname, password)