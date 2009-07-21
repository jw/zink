#!/usr/bin/python

class Source:
    '''
        A Subversion source.  This is where the project to be deployed lives.
    '''
    
    def __init__(self, request):
        '''
           Parses a source request.  This is a Subversion location.  Currently
           the 'head' is always selected.
                      
           The request string will be parsed as 
           <schema>[username[|password]@][host:]path where
           protocol: can be http, https, file, svn or svn+ssh all followed by a '://'
           username: the name of the user
           password: the password to be used to log in
           host: the host to be used
           path: the path to be used
        '''
        self.schema = None
        self.username = None
        self.password = None
        self.host = None
        self.path = None
        # schema
        if (request.find("://") != -1):
            self.schema = request[0:request.index(":")]
            request = request[request.find("://")+3:len(request)]
        # username and password
        if (request.find("|") != -1 and request.find("@") != -1):
            self.password = request[request.index("|")+1:request.index("@")]
            self.username = request[0:request.index("|")]
            request = request[request.find("@")+1:len(request)]
        # only username - no password
        if (request.find("@") != -1 and request.find("|") < 0):
            self.username = request[0:request.index("@")]
            request = request[request.find("@")+1:len(request)]
        # host
        if (request.find(":") != -1):
            self.host = request[0:request.find(":")]
            request = request[request.find(":")+1:len(request)]
        # at last - the required path
        self.path = request

    def __str__(self):
        string = "["
        if (self.schema is not None):
            string = string + "schema=" + str(self.schema) + "; "
        if (self.username is not None):
            string = string + "username=" + str(self.username) + "; "
        if (self.password is not None):
            string = string + "password=" + str(self.password) + "; "
        if (self.path is not None):
            string = string + "host=" + str(self.host) + "; "
        string = string + "location=" + str(self.path) + "]"
        return string

    def __repr__(self):
        return self.__str__()

class Destination:
    '''
        A destination where the project will be deployed to.  This looks much
        like a scp destination.
    '''

    def __init__(self, request):
        '''
           Parses a destination request.  The request string will be parsed as 
           [username[|password]@][host:]path where
           username: the name of the user
           password: the password to be used to log in
           host: the host to be used
           path: the path to be used
        '''
        self.username = None
        self.password = None
        self.host = None
        self.path = None
        # username and password
        if (request.find("|") != -1 and request.find("@") != -1):
            self.password = request[request.index("|")+1:request.index("@")]
            self.username = request[0:request.index("|")]
            request = request[request.find("@")+1:len(request)]
        # only username - no password
        if (request.find("@") != -1 and request.find("|") < 0):
            self.username = request[0:request.index("@")]
            request = request[request.find("@")+1:len(request)]
        # host
        if (request.find(":") != -1):
            self.host = request[0:request.find(":")]
            request = request[request.find(":")+1:len(request)]
        # at last - the required path
        self.path = request

    def __str__(self):
        string = "["
        if (self.username is not None):
            string = string + "username=" + str(self.username) + "; "
        if (self.password is not None):
            string = string + "password=" + str(self.password) + "; "
        if (self.path is not None):
            string = string + "host=" + str(self.host) + "; "
        string = string + "location=" + str(self.path) + "]"
        return string

    def __repr__(self):
        return self.__str__()


        
