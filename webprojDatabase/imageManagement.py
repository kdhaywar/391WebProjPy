
__author__ = 'KyleHayward'

import cx_Oracle
from groupManagement import GroupManagement








class ImageManagement:



    def ImportImage(self, images):
        """
        Inserts projimage object that contains 
        image and image information into the 
        images table of the database
        """
        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        
        ## hacked together... prob should fix that
        photo = images.imageFile
        cur.setinputsizes(photo=cx_Oracle.BLOB)
        
        ##convert privacy label charvar to privacy code
        privacyCode = None
        if images.imagePrivacy == "Private":
            privacyCode = 2
        elif images.imagePrivacy == "Public":
            privacyCode = 1
        elif images.imagePrivacy == "Group":
            x = GroupManagement()
            groupId = x.GroupNameToId(images.imageGroup , images.ownerName)
            if groupId:
                privacyCode = groupId
            else:
                print "group name+username pair does not exist so privacy was defualted to private"
                print images.ownerName
                privacyCode = 2
        else:
            print "ERROR: ProjImage privacy code does not follow protocol"
            privacyCode = 2
        
        insert ="insert into images( photo_id, owner_name, permitted, subject, place, timing, description, thumbnail, photo) values( photo_id_seq.nextval, :owner_name, :privacyCode, :subject, :place,  to_date(:timing,'MM-DD-YYYY'), :description, :thumbnail, :photo)"
        cur.execute(insert, {'owner_name':images.ownerName, 'privacyCode':privacyCode, 'subject':images.imageSubject, 'place':images.imageLocation, 'timing':images.imageDate, 'description':images.imageDesc, 'thumbnail':images.thumbnail, 'photo':images.imageFile})
        connection.commit()      
        cur.close()
        connection.close()         
        

        return True
