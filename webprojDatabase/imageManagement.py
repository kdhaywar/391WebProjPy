
__author__ = 'KyleHayward'

import cx_Oracle
import imghdr
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
            if errormessage:
                failedimages.append([image , errormessage] )

        
        connection.commit()             
        cur.close()
        connection.close()         
        return failedimages



    def UsersImages(self, uname):
        """
        WIP
        takes user_name and returns a list of Photo_ids owned by the user
        """

        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        pIdList = list()
        
        query ="select photo_id FROM images WHERE owner_name = :uname"
        cur.execute(query, {'uname':uname})
        for row in cur:
            pIdList.append(row[0])       

        cur.close()
        connection.close()   
        return pIdList       
        
        
        
        
    def GetImages(self, Pid):
        """
        WIP
        takes list of Photo_id and returns a list of projimage Objects
        """
        listofimages = list()
        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        Pidstring = ','.join(str(i) for i in Pid)

        #TODO BIND VAR
        query ="select * FROM images WHERE photo_id IN (%s)" %(Pidstring)
        
        #this is mixing up the PID so its fucking with the search order
        cur.execute(query)
        for image in cur:
            newImage = ProjImage()
            newImage.imageId = image[0]
            newImage.ownerName = image[1]
            newImage.imagePrivacy = image[2]
            newImage.imageSubject = image[3]
            newImage.imageLocation = image[4]
            newImage.imageDate = image[5]
            newImage.imageDesc = image[6]
            newImage.thumbnail = image[7]
            newImage.imageFile = image[8].read()
            listofimages.append(newImage)
        cur.close()
        connection.close()   
        
        return listofimages       
        
        
        
    def SearchImages( self , searchquery, uname):
        """
        takes a string and username and performs a search based on the string  
        returns list of photo_ids that the specific user is permitted to view
        WIP
        """
        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        pIdList = list()
        
        # 6*frequency(subject) + 3*frequency(place) + frequency(description)
        
        query ="SELECT score(1), score(2), score(3), photo_id FROM images WHERE contains(place, 'internet', 1) + contains(subject, 'dickbutt', 2) + contains(description, 'internet', 3) > 0 order by (score(1)*3)+(score(2)*6)+(score(3)) desc"
        cur.execute(query)
        for row in cur:
            pIdList.append(row[3])
            print row
            print "asdfasdf"
        print pIdList
        x = ImageManagement()
        failedimagelist = x.GetImages(pIdList)
        for d in failedimagelist:
            print d.imageSubject
            print d.imageLocation
            print d.imageId
            print "\n"
        cur.close()
        connection.close()   
        return pIdList         
        
        
        