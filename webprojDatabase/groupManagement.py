
__author__ = 'KyleHayward'

import cx_Oracle








class GroupManagement:



    def CreateGroup(self, groupInfo):

        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        
        insert ="insert into groups( group_id, user_name, group_name, date_created ) values( group_id_seq.nextval, :user_name, :group_name, to_date(sysdate,'MM-DD-YYYY') )"
        cur.execute(insert, {'user_name':groupInfo.user_name, 'group_name':groupInfo.group_name})
        connection.commit()      
        cur.close()
        connection.close()         
        return True
