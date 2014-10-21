from webprojDatabase.accountdbmanagement import AccountDbManagement

__author__ = 'KyleHayward'



class AccountManagement(object):
    """
    Interface object overtop of our database. Used to coordinate between our
    application and our internal database.
    """

    def UserLogin(self, uname, password):
        """
        Checks to see if the provided username and password match up with the database.
        :param uname: The user provided username.
        :param password: The user provided password.
        :return: Boolean value based on whether or not the username and password match up.
        """
        x = AccountDbManagement()
        if x.CheckLogin(uname, password):
            return True
        else:
            return False


    def CreateUserAccount(self, fname, lname, address, email, phonenum, uname, password, passconf):

        ###todo###
        ## check user input contraints
        ##check if password is null
        x = AccountDbManagement()
        if x.CheckIfUsernameExists(uname):
        ###username already exists
            return False
        elif x.CheckIfEmailExists(email):
        ##email already exists
            return False
        elif password != passconf or password == True:
            ##password and passconf do not match
            return False
        else:
            x.CreateUserAccount(fname, lname, address, email, phonenum, uname, password)
            
        return True