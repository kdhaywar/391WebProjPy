
__author__ = 'KyleHayward'

import cx_Oracle
from webprojDatabase.accountdbmanagement import AccountDbManagement

__author__ = 'KyleHayward'





class ImageManagement:



    def ImportImage(self, images):

        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        
        insert = """insert into images( photo_id, owner_name, permitted, subject, place, timing, description, thumbnail, photo) values( :photo_id, :owner_name, :permitted, :subject, :place, to_date(:timing,'MM-DD-YYYY'), :description, :thumbnail, :photo)"""
        curs.execute(insert, { 'photo_id': images.imageId, 'owner_name': images.ownerName, 'permitted': images.imagePrivacy, 'subject': images.imageSubject, 'place': images.imageLocation, 'timing': images.imageDate, 'description': images.imageDesc, 'thumbnail': images.thumbnail, 'photo': images.imageFile})
        connection.commit() 
        
        
        cur.close()
        connection.close()         
        

        return True
