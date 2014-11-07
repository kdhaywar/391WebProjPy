
__author__ = 'KyleHayward'

import cx_Oracle








class GroupManagement:



    def CreateGroup(self, uname, gname):
        """
        creates new group taking a uname and gname
        must have unique uname and gname
        returns true on success and false on group creation failure
        """

        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        #TODO exeption handler and return false on failed group creation
        insert ="insert into groups( group_id, user_name, group_name, date_created ) values( group_id_seq.nextval, :user_name, :group_name, sysdate )"
        cur.execute(insert, {'user_name':uname, 'group_name':gname})
        connection.commit()      
        cur.close()
        connection.close()         
        return True
    
    
    def AddGroupMembers(self, gid, fids, note):
        """
        adds new member to existing group taking a group_id, list of friend_id and notice
        must have unique and non null group_id and friend_id. notice can be null
        returns true on success and false on group creation failure
        """ 
        for fid in fids:
            connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
            cur = connection.cursor()
            #TODO exeption handler and return false on failed member addition
            insert ="insert into group_lists( group_id, friend_id, date_added, notice ) values( :group_id, :friend_id, sysdate, :notice  )"
            cur.execute(insert, {'group_id':gid, 'friend_id':fid, 'notice':note})
            connection.commit()
        
        cur.close()
        connection.close()         
        return True


    def UsersGroups(self, uname):
        """
        Takes a uname and returns a list of group_id/group_name pairs belonging to that user
        """
        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        
        query ="select group_id, group_name FROM groups WHERE user_name = :uname"
        cur.execute(query, {'uname':uname})
        results = cur.fetchall()
        
        cur.close()
        connection.close()   
        
        return results
        
        
        
    def GroupMembers(self, gname):
        """
        WIP
        Takes a gname and returns a list of unames belonging to that group
        """
        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        
        query ="select friend_id FROM group_lists WHERE user_name = :uname"
        cur.execute(query, {'uname':uname})
        results = cur.fetchall()
        
        cur.close()
        connection.close()   
        
        return results
        