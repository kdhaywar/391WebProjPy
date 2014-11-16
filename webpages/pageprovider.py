from util import ProjImage


__author__ = 'HenryPabst'

import cherrypy

from webprojDatabase.accountmanagement import AccountManagement
from webprojDatabase.imageManagement import ImageManagement
from webprojDatabase.groupManagement import GroupManagement
from util.ProjImage import ProjImage
import io
from PIL import Image
from io import BytesIO


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
        #thumbnail size
        size = 128, 128
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
            try:
                im = Image.open(io.BytesIO(newImage.imageFile))
                im.thumbnail(size, Image.ANTIALIAS)
                im.save("a_test.png")
            except IOError:
                print "cannot create thumbnail for", newImage.imageFile           
            newImage.thumbnail = buffer(im.tostring())
            newImage.imageLocation = kwargs["location"]
            newImage.imageDate = kwargs["picDate"]
            newImage.imageSubject = kwargs["picSubject"]
            newImage.imagePrivacy = kwargs["picSecurity"]
            newImage.imageGroup = kwargs["picGroup"]
            newImage.ownerName = cherrypy.session.get("user")
            #newImage.ownerName = cherrypy.session["user"] 
            images.append(newImage)
            

        for k in images:
            print k
      


        # sends a list of ProjImage to Import Image
        x = ImageManagement()
        failedimagelist = x.ImportImage(images)
        if failedimagelist:
            for imageerror in failedimagelist:
                print imageerror
            return "Not all images uploaded these images failed '%s'" %(failedimagelist)
        else:    
            return "All images uploaded"

    @cherrypy.expose
    def search(self):
        """
        The webpage that allows a user to enter an image search query.
        :return: HTML for the webpage.
        """
        x = ImageManagement()
        failedimagelist = x.SearchImages( 'q', 'sdfgsdfg sdfgsdfg06/12/1000-12/11/1001 sdfg 06/12/1002-12/11/1003', 'rank')
        
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
        groupHeader = """
        <!DOCTYPE html>
<html>
<head lang="en">
    <meta charset="UTF-8">
    <link type="text/css" rel="stylesheet" href="groupDisplay.css"/>
    <title></title>
</head>
<body>
    <div>
        <h1>
            I CAN'T BELIEVE IT'S NOT IMGUR!
        </h1>
    </div>
    <div>
        <form method="post" action="groupCreation">
            <button type="submit">Create a New Group</button>
        </form>
    </div>
    <div class="groupTable">
        <table>
            <thead>
                <tr>
                    <th colspan="2">My Groups</th>
                </tr>
                <tr style="border-bottom:1px solid black;">
                    <th style="padding: 5px;"><em>Group Name</em></th>
                    <th style="padding: 5px; border-left:1px solid black"><em>Group Members</em></th>
                </tr>
            </thead>
            <tbody>
        """
        groupTableEnd = """
                </tbody>
        </table>
    </div>
        """
        groupFooter = """
</body>
</html>
        """
        groupData = ""
        gm = GroupManagement()
        usersGroups = gm.UsersGroups(cherrypy.session.get("user"))
        print "usersGroups ids", usersGroups.keys()
        for key in usersGroups.keys():
            groupName = usersGroups.get(key)
            groupUsers = gm.GroupMembers(key)
            groupData = groupData + """
                            <tr style="border-bottom:1px solid black;">
                    <td style="padding: 5px;">%s</td>
                    <td style="padding: 5px; border-left: 1px solid black;">%s</td>
                </tr>
            """ %(groupName, "<br>".join(groupUsers))

            groupTableEnd = groupTableEnd + """
                                    <form method="post" action="groupManagement">
                        <input type="hidden" name="groupName" id="groupName" value="%s"/>
                        <input type="hidden" name="groupId" id="groupId" value="%d"/>
                        <button type="submit"> Manage Group %s </button>
                    </form>
            """ %(groupName, key, groupName)
        guestGroupIds = gm.UsersPermissions(cherrypy.session.get("user"))
        print "guestGroupIds ", guestGroupIds
        for id in guestGroupIds:
            if id in usersGroups.keys():
                guestGroupIds.remove(id)
        for groupId in guestGroupIds:
            groupUsers = gm.GroupMembers(groupId)
            groupName = gm.GroupIdToName(groupId)
            groupData = groupData + """
                                        <tr style="border-bottom:1px solid black;">
                    <td style="padding: 5px;">%s</td>
                    <td style="padding: 5px; border-left: 1px solid black;">%s</td>
                    </tr>
            """ %(groupName, "<br>".join(groupUsers))
        return groupHeader + groupData + groupTableEnd + groupFooter

    @cherrypy.expose
    def groupCreation(self):
        """
        The webpage that allows the user to create a new group.
        :return: HTML for the webpage.
        """
        if "user" not in cherrypy.session.keys():
            raise cherrypy.HTTPRedirect("/home")
        return open("static/groupCreation.html")


    @cherrypy.expose
    def groupManagement(self, groupName=None, groupId=None):
        if "user" not in cherrypy.session.keys():
            raise cherrypy.HTTPRedirect("/home")
        print "groupName " + groupName
        print "groupId " + groupId
        groupManagementHTML = open("static/groupManagement.html").read() %(groupId)
        return groupManagementHTML

    @cherrypy.expose
    def addNewGroup(self, groupName=None, groupUsers=None):
        """
        Method called from the groupCreation webpage when we want to add a new group to the database.
        :return: A message detailing whether or not the group was correctly created.
        """
        if(groupName == None or groupUsers == None):
            return "Error, you must provide a group name and a list of users to add."
        gm = GroupManagement()
        usersList = groupUsers.split(", ")
        usersList.append(cherrypy.session.get("user"))
        gm.CreateGroup(cherrypy.session.get("user"), groupName)
        groupId = gm.GroupNameToId(cherrypy.session.get("user"), groupName)
        gm.AddGroupMembers(groupId, usersList)
        return "Group adding successful."

    @cherrypy.expose
    def manageGroup(self, groupId=None, addedUsers=None, removedUsers=None, modifiedNotices=None, deleteGroup=None):
        print "groupId", groupId
        print "addedUsers", addedUsers
        print "removedUsers", removedUsers
        print "modifiedNotices", modifiedNotices
        print "deleteGroup", deleteGroup
        gm = GroupManagement()
        groupName = gm.GroupIdToName((int(groupId)))
        if(deleteGroup == "True"):
            result = gm.RemoveGroup(cherrypy.session.get("user"), groupName)
            if(result):
                return "Group was sucessfully removed."
            else:
                return "Group could not be removed."
        removedUsers = removedUsers.split(", ")
        addedUsers = addedUsers.split(", ")
        results = list()
       # for r, a in removedUsers, addedUsers:
       #     if r == a:
       #         return "Error, cannot both add and remove a user: %s." %(r)
        for r in removedUsers:
            result = gm.RemoveGroupMember(cherrypy.session.get("user"), groupName, r)
            if not result:
                results.append("Error: Could not remove user %s." %(r))
        for a in addedUsers:
            miscList = list()
            miscList.append(a)
            result = gm.AddGroupMembers(groupId, miscList)
            if not result:
                results.append("Error: Could not add user %s." %(a))
        return str(results)

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
