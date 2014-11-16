
__author__ = 'KyleHayward'

import cx_Oracle








class GroupManagement:



    def CreateGroup(self, uname, gname):
        """
        creates new group taking a uname and gname
        must have unique uname+ gname
        returns true on success and false on group creation failure
        """
        #TODO more specific exception handling.  (check for uniqueness of uname and gname exception)

        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()        
        insert ="insert into groups( group_id, user_name, group_name, date_created ) values( group_id_seq.nextval, :user_name, :group_name, sysdate )"
        
        try:
            cur.execute(insert, {'user_name':uname, 'group_name':gname})
            connection.commit() 
            x = GroupManagement()             
            cur.close()
            connection.close()
            return True            

        except Exception as e:
            print("ERROR: while creating group in CreateGroup")
            cur.close()
            connection.close()              
            return False        
    
    
    def AddGroupMembers(self, gid, fids, *args):
        """
        adds new member to existing group taking a group_id, list of friend_id and notice
        must have unique and non null group_id and friend_id. notice can be null
        returns true on success and false on member addition failure
        """ 
        
        if len(args) == 0:
            note = None 
        else:
            note = args[0]
            
        for fid in fids:
            connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
            cur = connection.cursor()
            insert ="insert into group_lists( group_id, friend_id, date_added, notice ) values( :group_id, :friend_id, sysdate, :notice  )"
            try:
                cur.execute(insert, {'group_id':gid, 'friend_id':fid, 'notice':note})
                connection.commit()
            except Exception as e:
                #Better error check and return list of friends that did not add
                print("ERROR: while adding '%s' to group") %(fid) 
        cur.close()
        connection.close()         
        return True
    
    
    
    def RemoveGroup( self,uname, gname):
        """
        takes uname and gname and removes that group
        """
        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        gid = GroupManagement().GroupNameToId(uname , gname)
        if not gid and uname is not 'admin':
            print "%s does not have access to delete group %s" %(uname, gname)
            return False
        #deletes all memebers of the group first  
        for fid in GroupManagement().GroupMembers(GroupManagement().GroupNameToId(uname, gname)):
            GroupManagement().RemoveGroupMember(uname, gname, fid)
        #deletes group
        statement ="DELETE FROM groups WHERE group_id = :gid OR :uname = 'admin'"
        cur.execute(statement, {'gid':gid, 'uname':uname})
        connection.commit()
        cur.close()
        connection.close()           
        return True        
        
        
        
    def RemoveGroupMember( self, uname, gname, fid):
        """
        takes uname gname and friend_id(aka username to be removed from group) and removes said person
        returns true if user removal was successful false if not
        TODO add to take in list of fid?? maybe
        """
        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        gid = GroupManagement().GroupNameToId(uname , gname)
        if not gid and uname is not 'admin':
            print "%s does not have access to remove members from %s" %(uname, gname)
            return False
        
        statement ="DELETE FROM group_lists WHERE (group_id = :gid OR :uname = 'admin') AND friend_id = :fid"
        cur.execute(statement, {'gid':gid, 'fid':fid, 'uname':uname})
        connection.commit()
        cur.close()
        connection.close()           
        return True        
        
        
    
    


    def UsersGroups(self, uname):
        """
        Takes a uname and returns a dict of group_id/group_name pairs belonging to that user
        TODO admin stuff
        """
        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        
        query ="select group_id, group_name FROM groups WHERE user_name = :uname"
        cur.execute(query, {'uname':uname})
        results = cur.fetchall()
        cur.close()
        connection.close()   
        
        return dict(results)
        
        
        
    def GroupMembers(self, gId):
        """
        Takes a Group_id and returns a list of unames belonging to that group
        TODO admin stuff
        """
        results = []
        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        query ="select friend_id FROM group_lists WHERE group_id = :gId"
        cur.execute(query, {'gId':gId})
        for row in cur:
            results.append(row[0])      
        cur.close()
        connection.close() 
        return results
    
    
    def GroupNameToId(self, uname, gname ):
        """
        Takes a gname and uname and returns the group ID or False if gname + uname do not exist
        """
        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()      
        query ="select group_id FROM groups WHERE user_name = :uname and group_name = :gname"
        cur.execute(query, {'uname':uname, 'gname':gname})
        result = cur.fetchall()

        cur.close()
        connection.close() 
        if len(result) > 1:
            print "ERROR: UNIQUE(group_name, user_name) constraint for groups has be violated"
            return False
        elif result:
            return result[0][0]
        else:
            return False
        
        
    def UsersPermissions( self, uname):
        """
        gets passed a uname and returns a list of groups the user has permissions to
        TODO admin stuff
        """
        listofgroups = list()
        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        query ="select DISTINCT group_id FROM group_lists WHERE friend_id = :uname"
        cur.execute(query, {'uname':uname})
        for row in cur:
            listofgroups.append(row[0])              
        cur.close()
        connection.close()   
        return listofgroups
    
    def GroupIdToName( self, gId ):
        """
        Takes a Group_id and returns group name
        """

        connection = cx_Oracle.connect('kdhaywar/kdhaywar2014@crs.cs.ualberta.ca')
        cur = connection.cursor()
        query ="select group_name FROM groups WHERE group_id = :gId"
        cur.execute(query, {'gId':gId})
        result = cur.fetchone()
        cur.close()
        connection.close() 
        return result[0]    
        