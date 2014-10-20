__author__ = 'HenryPabst'

import cherrypy
from accountmanagement import AccountManagement

class PageProvider(object):

    @cherrypy.expose
    def index(self):
        return open("html/index.html")

    @cherrypy.expose
    def login(self):
        return open("html/login.html")

    @cherrypy.expose
    def createaccount(self):
        return open("html/createaccount.html")

    @cherrypy.expose
    def checklogin(self, uname, password):
        #We'll need to check here to see if the username and password match, then provide a session key if they do, otherwise
        #we'll need to say their username or password was wrong, and redirect them to the login page.
        x = AccountManagement()
        if x.UserLogin(uname, password):
            return "valid username and password, uname: %s, pass %s" %(uname, password)
            
        return "invalid username or password, uname: %s, pass %s" %(uname, password)


    @cherrypy.expose
    def checkaccountcreation(self, fname = None, lname = None, address = None, email = None, phonenum = None, uname = None,
                             password = None, passconf = None):
        x = AccountManagement()
        if x.CreateUserAccount(fname, lname, address, email, phonenum, uname, password, passconf):
            return """Account creation worked WIP, parameter values:
                    fname: %s
                    lname: %s
                    address: %s
                    email: %s
                    phonenum: %s
                    uname: %s
                    password: %s
                    passconf: %s
                    """ %(fname, lname, address, email, phonenum, uname, password, passconf)  
        return "something went wrong maybe pword didnt match or username/email already exists"
            
        
