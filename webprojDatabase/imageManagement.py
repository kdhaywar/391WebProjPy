
__author__ = 'KyleHayward'

import cx_Oracle
import imghdr
import re
from datetime import datetime
import datetime
from groupManagement import GroupManagement
from util.ProjImage import ProjImage









class ImageManagement:



    def ImportImage(self, images):
        """
        Inserts projimage object into images table of database
        takes a list of projimages and returns a list(image,list of errormessages) for images that failed to insert,
        if no errors then returns an empty list.
        Checks if image is an image,  date formatting is correct, and if the group name is owner exist/owned by owner  
        """
        failedimages = list()

        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        
        for image in images:

            ## hacked together... prob should fix that
            photo = image.imageFile
            cur.setinputsizes(photo=cx_Oracle.BLOB)            
            errormessage = list()
            privacyCode = 2
            #convert privacy label charvar to privacy code
            #TODO if we arn't allowing the user to import multiple batches move this outside for loop
            if image.imagePrivacy == "Private":
                privacyCode = 2
            elif image.imagePrivacy == "Public":
                privacyCode = 1
            elif image.imagePrivacy == "Group":
                x = GroupManagement()
                groupId = x.GroupNameToId(image.imageGroup , image.ownerName)
                if groupId:
                    privacyCode = groupId
                else:
                    errormessage.append("No %s's %s group in DB set to 'PRIVATE'" %(image.ownerName, image.imageGroup))
                    
            #if image not an image then adds the error to failimages list if it is an image it attempts to insert new image to DB
            if not imghdr.what(None, image.imageFile):
                errormessage.append("Not a recognized image")
            else:

                try:
                    insert ="insert into images( photo_id, owner_name, permitted, subject, place, timing, description, thumbnail, photo) values( photo_id_seq.nextval, :owner_name, :privacyCode, :subject, :place,  to_date(:timing,'MM-DD-YYYY'), :description, :thumbnail, :photo)"
                    cur.execute(insert, {'owner_name':image.ownerName, 'privacyCode':privacyCode, 'subject':image.imageSubject, 'place':image.imageLocation, 'timing':image.imageDate, 'description':image.imageDesc, 'thumbnail':image.thumbnail, 'photo':image.imageFile})
                except cx_Oracle.DatabaseError as e:
                    error, = e.args
                    if(error.code == 1858):
                        errormessage.append("Improper Date formatting" )
                    else:
                        errormessage.append("Unknown database error when inserting image")
                        print("Database Error Occured on image '%s'") %(error.code)
                        print("Database Error Occured on image '%s'") %(error.message)
                        print(e)
            if errormessage:
                failedimages.append([image , errormessage])

        
        connection.commit()             
        cur.close()
        connection.close()         
        return failedimages



    def GetUsersImages(self, uname, **kwargs):
        """
        takes user_name and returns a list of projimage objects owned by the user
        TODO add ability to only get certian image fields
        TODO add admin privledge
        """

        listofimages = list()
        
        
        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        pIdList = list()

        query ="select * FROM images WHERE owner_name = :uname"
        cur.execute(query, {'uname':uname})
        for row in cur:
            newImage = ProjImage()
            newImage.imageId = row[0]
            newImage.ownerName = row[1]
            newImage.imagePrivacy = row[2]
            newImage.imageSubject = row[3]
            newImage.imageLocation = row[4]
            newImage.imageDate = row[5]
            newImage.imageDesc = row[6]
            newImage.thumbnail = row[7]
            newImage.imageFile = row[8].read()
            listofimages.append(newImage)      
        cur.close()
        connection.close()   
        return listofimages      
        
        
        
        
      
        
        
        
    def SearchImages( self , uname, searchquery, orderby):
        """
        takes a username, string for search query, and the type of ranking ( "rank" or "recentfirst" or "recentlast" and performs a search based on the string  
        returns list of projimage objects
        TODO add ability to only get certian image fields
        TODO date search
        
        """
        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        listofimages = list()
        
        
        period =""

        periodregex = re.compile('\d{2}[/]\d{2}[/]\d{4}-\d{2}[/]\d{2}[/]\d{4}')
        periodlist=periodregex.findall(searchquery)
        
        # iterates the matching list and prints all the matches
        # TODO add sql injection protection
        for match in periodlist:
            dateregex = re.compile('\d{2}[/]\d{2}[/]\d{4}')
            periodlist=dateregex.findall(searchquery)
            period = period + " AND (timing BETWEEN to_date('"+ periodlist[0] + "','MM-DD-YYYY') AND to_date('"+ periodlist[1] + "','MM-DD-YYYY'))"
            print "asdfkjasdflkjhsadlfkjhasldkfhalksjdf"
            

    
                
        
        #cleans user input to just alphanumeric
        rx = re.compile('\W+')
        cleansearchquery = rx.sub(' ', searchquery).strip()
     
        
        
        
        #gets a list of group_ids the uname is a member of and converts it into a string for query condition statement
        x = GroupManagement()
        listofgroups = x.UsersPermissions(uname)
        stringofgroups = ','.join(map(str, listofgroups)) 

        #TODO PARSE INPUT REMOVING COMMAS AND SUCH must not have query operators
        #tokenizes searchquery and transforms it to various oracle recognized expressions for a better search 
        progrelaxml = """'<query>
            <textquery lang="ENGLISH" grammar="CONTEXT"> """+ cleansearchquery +"""
            <progression>
            <seq><rewrite>transform((TOKENS, "{", "}", " "))</rewrite></seq>
            <seq><rewrite>transform((TOKENS, "{", "}", " ; "))</rewrite></seq>
            <seq><rewrite>transform((TOKENS, "{", "}", " AND "))</rewrite></seq>
            <seq><rewrite>transform((TOKENS, "{", "}", " ACCUM "))</rewrite></seq>
            </progression>
            </textquery>
            <score datatype="INTEGER" algorithm="COUNT"/>
            </query>'"""
        

        ranktype = None
        if orderby is 'rank':
            ranktype = "(score(1)*3)+(score(2)*6)+(score(3)) desc"    
        elif orderby is 'recentfirst':
            ranktype = "timing desc"
        elif orderby is 'recentlast':
            ranktype = "timing asc"
        else:
            print "Not recognized orderby parameter"
            return False
        
        period = "AND 1 "
        query ="""SELECT * FROM images WHERE (contains(place, :progrelaxml , 1) + contains(subject,  :progrelaxml , 2) + contains(description, :progrelaxml, 3) > 0)
            AND (owner_name = :uname OR permitted IN (%s) OR :uname = 'admin') :period order by :ranktype""" %(stringofgroups)

        cur.execute(query, {'progrelaxml':progrelaxml , 'uname':uname , 'period':period , 'ranktype':ranktype }) 
        for row in cur:
            newImage = ProjImage()
            newImage.imageId = row[0]
            newImage.ownerName = row[1]
            newImage.imagePrivacy = row[2]
            newImage.imageSubject = row[3]
            newImage.imageLocation = row[4]
            newImage.imageDate = row[5]
            newImage.imageDesc = row[6]
            newImage.thumbnail = row[7]
            newImage.imageFile = row[8].read()
            listofimages.append(newImage)         

           
        cur.close()
        connection.close()   
        return listofimages        
        
        
        
        
        
        
    def ModifyImageData( self, uname, pid, **kwargs):
        """
        takes a pid and a key word pairs of column names:new data to be changed and what they are being changed to.
        Note keys must match the columns in the images table
        example ModifyImageData(uname, photo_id, subject ='new subject' , place = 'new location') 
        do not modify pid
        """
        
        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        # creates a sql statement using the keys passed.  the nested join statement creates ' key= :key '
        # while the other join statement combines ' key= :key ' strings so they are seperated by commas
        insert ="UPDATE images SET "+ ", ".join(["= :".join([key, key]) for key, value in kwargs.items()]) +" WHERE photo_id = :pid AND (owner_name = :uname OR :uname = 'admin')"
        #adds the pid and uname to the kwargs so sql can properly bind all the nessesary varibles when executed
        kwargs.update({'pid':pid , 'uname':uname})
        cur.execute(insert, kwargs ) 
        connection.commit() 
        cur.close()
        connection.close()   
        return True  
        
        