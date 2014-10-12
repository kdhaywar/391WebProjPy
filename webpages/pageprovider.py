__author__ = 'HenryPabst'

import cherrypy


class PageProvider(object):

    @cherrypy.expose
    def index(self):
        return open("html/index.html")

    @cherrypy.expose
    def login(self):
        return open("html/login.html")

    @cherrypy.expose
    def createaccount(self):
        return "Account creation, WIP"

    @cherrypy.expose
    def checklogin(self, uname, password):
        return "Account credential checking WIP, uname: %s, pass %s" %(uname, password)