__author__ = 'HenryPabst'

import cherrypy


class PageProvider(object):

    @cherrypy.expose
    def index(self):
        return open("html/index.html")

    @cherrypy.expose
    def login(self):
        return "Login page, WIP"

    @cherrypy.expose
    def createaccount(self):
        return "Account creation, WIP"