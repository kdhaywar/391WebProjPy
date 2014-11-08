from util import ProjImage

__author__ = 'HenryPabst'

import cherrypy

from webprojDatabase.accountmanagement import AccountManagement
from webprojDatabase.imageManagement import ImageManagement
from util.ProjImage import ProjImage


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
        if "user" in cherrypy.session.keys():
            raise cherrypy.HTTPRedirect("/home")
        else:
            return open("static/index.html")

    @cherrypy.expose
    def login(self):
        """
        The login page of our website, the user provides a username and password.
        :return: HTML page for this webpage.
        """
        return open("static/login.html")

    @cherrypy.expose
    def createaccount(self):
        """
        The account creation page of our website, the user provides relevant information
        for the creation of their account.
        :return: HTML page for this webpage.
        """
        return open("static/createaccount.html")

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
            cherrypy.session["user"] = uname;
            raise cherrypy.HTTPRedirect("/home")
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
            cherrypy.session["user"] = uname;
            raise cherrypy.HTTPRedirect("/home")
        else:
            return "something went wrong maybe pword didnt match or username/email already exists"

    @cherrypy.expose
    def home(self):
        #return "This is the homepage for the logged in user, WIP."
        if "user" not in cherrypy.session.keys():
            raise cherrypy.HTTPRedirect("/")
        baseHtml = """<!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <link type="text/css" rel="stylesheet" href="home.css"/>
    <title></title>
</head>
<body>
    <div>
        <h1>I CAN'T BELIEVE IT'S NOT IMGUR!</h1>
    </div>
    <div>
        <h2>Welcome, %s!</h2>
    </div>
    <div class="buttonHolder">
        <form method="post" action="upload">
            <button type="submit">Upload Images</button>
        </form>
        <form method="post" action="groupDisplay">
            <button type="submit">Group Management</button>
        </form>
        <form method="post" action="search">
            <button type="submit">Search Images</button>
        </form>
        <form method="post" action="logout">
            <button type="submit">Logout</button>
        </form>
    </div>
</body>
</html>"""

        return baseHtml % (cherrypy.session["user"])


    @cherrypy.expose
    def upload(self):
        if "user" not in cherrypy.session.keys():
            raise cherrypy.HTTPRedirect("/home")
        return open("static/upload.html")


    @cherrypy.expose
    def uploadImages(self, **kwargs):
        """
        Webpages that serves to upload images for us.
        kwargs is a dictionary containing a bunch of key-value pairs corresponding to the values the
        user provided.
        kwargs["files"] will be a list of file-like objects corresponding to the actual files the user wanted to upload.
        (Can't guarantee they are images though, might help to look at http://svn.cherrypy.org/trunk/cherrypy/tutorial/tut09_files.py).
        kwargs["location"] will be text describing the location the image was taken at.
        kwargs["picDate"] will be a string(?) of format mm/dd/yyyy for the date the image was taken. Need testing on campus.
        kwargs["picSubject"] will be a string describing the subject of the image.
        kwargs["picSecurity"] will be a string describing security setting, either Public, Group, or Private.
        kwargs["picGroup"] will be a string describing the group name if the Group security setting is chosen.
        """
        
        #redirects user if no session key to prevent NULL user images being uploaded
        if "user" not in cherrypy.session.keys():
            raise cherrypy.HTTPRedirect("/home")        
        
        for k, v in kwargs.items():
            print k, v, type(v)
        images = list()
        #Will need to put checks here for proper formatting of date, filename, etc.
        fileobjects = list()
        if isinstance(kwargs["files"], list):
            fileobjects = kwargs["files"]
        else:
            fileobjects.append(kwargs["files"])
        for item in fileobjects:
            newImage = ProjImage()
            newImage.imageFile = item.file.read()
            newImage.imageLocation = kwargs["location"]
            newImage.imageDate = kwargs["picDate"]
            newImage.imageSubject = kwargs["picSubject"]
            newImage.imagePrivacy = kwargs["picSecurity"]
            newImage.imageGroup = kwargs["picGroup"]
            #newImage.ownerName = cherrypy.session.get("user")  should we use this?
            newImage.ownerName = cherrypy.session["user"]
            images.append(newImage)
            

        for k in images:
            print k

            x = ImageManagement()
            ##add better error checking and maybe move for loop to function?
            if x.ImportImage(k):
                return "maybe worked???"             

            else:
                return "didnt work?"             
            
        return "WIP"

    @cherrypy.expose
    def search(self):
        """
        The webpage that allows a user to enter an image search query.
        :return: HTML for the webpage.
        """
        if "user" not in cherrypy.session.keys():
            raise cherrypy.HTTPRedirect("/home")
        return "Search webpage, WIP"


    @cherrypy.expose
    def groupDisplay(self):
        """
        The webpage that displays group management information to the user.
        :return: HTML for the webpage.
        """
        #TODO: Database side for  getting Group information and then creating HTML to display it to the user.
        if "user" not in cherrypy.session.keys():
            raise cherrypy.HTTPRedirect("/home")
        return "Group display webpage, WIP"

    @cherrypy.expose
    def groupCreation(self):
        """
        The webpage that allows the user to create a new group.
        :return: HTML for the webpage.
        """
        if "user" not in cherrypy.session.keys():
            raise cherrypy.HTTPRedirect("/home")
        return "Group creation webpage, WIP."


    @cherrypy.expose
    def addNewGroup(self, groupName=None, groupUsers=None):
        """
        Method called from the groupCreation webpage when we want to add a new group to the database.
        :return: A message detailing whether or not the group was correctly created.
        """
        return "Group adding method, WIP"


    @cherrypy.expose
    def adminDataAnalysis(self):
        """
        The webpage that allows for administrator data analysis.
        :return:
        """
        if "user" not in cherrypy.session.keys() or cherrypy.session["user"] != "admin":
            raise cherrypy.HTTPRedirect("/")
        return "Admin data analysis webpage, WIP"

    @cherrypy.expose
    def logout(self):
        """
        Logs the user out and returns them to the front page of the website.
        :return: None
        """
        cherrypy.session.pop("user", None)
        raise cherrypy.HTTPRedirect("/")
