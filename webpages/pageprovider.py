__author__ = 'HenryPabst'

import cherrypy

from webprojDatabase.accountmanagement import AccountManagement


class PageProvider(object):
    """
    Object passed to cherrypy for providing webpages.
    """

    @cherrypy.expose
    def index(self):
        """
        The main, front page of our website.
        :return: HTML page for this webpage.
        """
        return open("html/index.html")

    @cherrypy.expose
    def login(self):
        """
        The login page of our website, the user provides a username and password.
        :return: HTML page for this webpage.
        """
        return open("html/login.html")

    @cherrypy.expose
    def createaccount(self):
        """
        The account creation page of our website, the user provides relevant information
        for the creation of their account.
        :return: HTML page for this webpage.
        """
        return open("html/createaccount.html")

    @cherrypy.expose
    def checklogin(self, uname, password):
        """
        Login check page, should never actually be visible to the user.
        :param uname: The account username to check for in the database.
        :param password: The account password to check for in the database.
        :return: None
        """
        #We'll need to check here to see if the username and password match, then provide a session key if they do, otherwise
        #we'll need to say their username or password was wrong, and redirect them to the login page.
        x = AccountManagement()
        if x.UserLogin(uname, password):
            #This is temporary, we'll raise an HTTPRedirect exception here to send the user to another page.
            return "valid username and password, uname: %s, pass %s" %(uname, password)
        else:
            return "invalid username or password, uname: %s, pass %s" %(uname, password)


    @cherrypy.expose
    def checkaccountcreation(self, fname = None, lname = None, address = None, email = None, phonenum = None, uname = None,
                             password = None, passconf = None):
        """
        Webpage that checks if all the provided info is good for creating a new account.
        :param fname: The new account's first name.
        :param lname: The new account's last name.
        :param address: The new account's address.
        :param email: The new account's email address.
        :param phonenum: The new account's phone number.
        :param uname: The new account's username
        :param password: The new account's password.
        :param passconf: The new account's password confirmation.
        :return:
        """
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
        else:
            return "something went wrong maybe pword didnt match or username/email already exists"