#!/usr/bin/python

import logging
import logging.config

import ConfigParser

import paramiko
from paramiko import SSHClient

from os import listdir, makedirs
from os.path import exists, join, basename, walk, isfile

from optparse import OptionParser

import sys
import shutil
from stat import S_ISDIR

import util

import tempfile

from arguments import Destination
from arguments import Source

from svn import core 

# are these needed?
import socket
import pysvn
import datetime

class Deployer:
    """
        Deploys a Django system from a Subversion source to a remote 
        location after updating the required files with the proper values. 
    """
    
    def __init__(self, ):

        logging.config.fileConfig("./logging.config", None)

        # argument and options handler
        usage = "usage: %prog source destination [options]\n" \
                "\n"\
                " source: <schema>[username[|password]@][host:]path\n" \
                " destination: [username[|password]@][host:]path"
        parser = OptionParser(usage=usage)
        parser.add_option("--verbose", action="store_true", default=False, 
                          help="Make lots of noise.")
        parser.add_option("--version", type="string", default="1.0.0", 
                          help="Set the version of the deployed system [default: %default].")
        parser.add_option("--tag", action="store_true", default=False, 
                          help="Tag the Subversion tree.")
        parser.add_option("--port", type="int", default="22",
                          help="The SSH port on the destination host [default: %default].")
        (options, args) = parser.parse_args()

        # arguments check
        if len(args) == 2:
            self.source=Source(args[0])
            self.destination=Destination(args[1])
        else:
            print "Sorry - two arguments are required.\n"
            parser.print_help()
            sys.exit()

        # options check
        self.verbose = options.verbose
        self.tag = options.tag
        self.version = options.version
        self.port = options.port
        
        logging.debug("Derived arguments and options: ")
        logging.debug(" source: " + str(self.source))
        logging.debug(" destination: " + str(self.destination))
        logging.debug(" o verbose: " + str(self.verbose))
        logging.debug(" o tag: " + str(self.tag))
        logging.debug(" o version: " + self.version)
        logging.debug(" o port: " + str(self.port))

        # connect to the remote location
        if self.verbose:
            print "Creating connection to " + self.destination.host + "..."
        self.connect()
        
        # prepare the svn client a.k.a. the source side
        def get_login(realm, username, may_save):
            return True, self.source.username, self.source.password, True
        self.client = pysvn.Client()
        self.client.callback_get_login = get_login
        self.client.exception_style = 1

        # get the different svn error codes
        global __svn_errors 
        __svn_errors = util.get_svn_errors()

    def connect(self):
        """
            Opens an SFTP connection to the destination host.
        """
        try:
            self.sftp = None
            transport = None
            transport = paramiko.Transport((self.destination.host, self.port))
            transport.connect(username = self.destination.username, password = self.destination.password)
            self.sftp = paramiko.SFTPClient.from_transport(transport)
        except socket.gaierror, (errno, strerror):
            logging.warn("Oops (%s): %s" % (errno, strerror))
            return False
        except socket.error, (errno, strerror):
            logging.warn("Oops (%s): %s" % (errno, strerror))
            return False
        except IOError, (errno, strerror):
            logging.warn("Oops (%s): %s" % (errno, strerror))
            return False       
        except paramiko.AuthenticationException, (strerror):
            logging.warn("Oops (-3): %s" % (strerror))
            return False
        except paramiko.SSHException, (strerror):
            logging.warn("Oops (-4): %s" % (strerror))
            return False

    def disconnect(self):
        """
            Closes the SFTP connection.
        """
        if (self.sftp != None):
            channel = self.sftp.get_channel()
            if (channel != None):
                transport =  channel.get_transport()
                if (transport != None):
                    transport.close()
                channel.close()
            self.sftp.close()

    def __str__(self):
        return "Deployer" 

    def is_proper_svn(self):
        """
            Is the given source a proper svn?  Is it a Subversion url?  
            And, does it contain the 'branches', 'tags' and 'trunk' 
            directories?  If so, it is; otherwise False is returned. 
        """
        url = self.source.schema + "://" + self.source.host + self.source.path
        if self.client.is_url(url):
            try:
                entries_list = self.client.ls(url)
                files = []
                for tuple in entries_list:
                    files.append(basename(tuple.name))
                if (files.__contains__("branches") and 
                    files.__contains__("trunk") and
                    files.__contains__("tags")):
                    if (self.verbose):
                        print "Good.  The specified source " + url + " is a valid Subversion project."
                    return True
            except pysvn.ClientError as (e):
                for message, code in e.args[1]:
                    logging.warn(str(message) + " [" + str(code) + ":" + __svn_errors[code] + "] ")
        print "Sorry, " +  url + " can not be deployed.  See the log file for more info."
        return False;

    def export_source_to_temp(self):
        """
            Exports the 'trunk' directory from the Subversion source to
            a temporary directory.  
        """
        url = self.source.schema + "://" + self.source.host + self.source.path
        trunk = join(url, "trunk")
        logging.debug("Exporting " + trunk + "...")
        try:
            self.dir = tempfile.mkdtemp(suffix=".deploy", prefix="svn.")
            self.client.export(trunk, join(self.dir, "trunk"))
        except pysvn.ClientError as (e):
            for message, code in e.args[1]:
                logging.warn(str(message) + " [" + str(code) + ":" + __svn_errors[code] + "] ")
            return False            
        logging.debug("Exported the system successfully.")
        if self.verbose:
            print "Exported " + trunk + " to this machine successfully."
        return True
    
    def update_export(self):
        """
            Updates the exported source file.
        """
        wsgi = join(self.dir, "trunk", "django.wsgi")
        if (exists(wsgi)):
            # find sys.path.append('<something>') and replace it with
            # sys.path.append('<self.destination.path>').
            good = "sys.path.append('" + self.destination.path + "')\n"
            input = open(wsgi)
            # make temporary directory
            temp_directory = join(self.dir, "temp")
            makedirs(temp_directory)
            # make temporary django.wsgi
            temp_file = join(self.dir, "temp", "django.wsgi")
            output = open(temp_file, 'w') 
            # update the python path 
            for s in input:
                if (s.startswith("sys.path.append")):
                    output.write(good)
                elif (s.startswith("append")):
                    output.write(good)
                else:
                    output.write(s)
            # close
            output.close()
            input.close()
            # copy the updated file over the original file
            shutil.copy(temp_file, wsgi)
            if self.verbose:
                print "Updated the " + wsgi + "." 
            return True
        else:
            logging.warn("Oops: django.wsgi does not exist!")
        print "warning: could not properly update the django.wsgi.  Trying to continue..."
        return False

    def exists_remotely(self, name):
        """
            Check whether name (file name or directory name) exists on 
            the destination.
        """
        try:
            stat = self.sftp.stat(name)
            return True
        except IOError:
            return False
        else:
            raise RuntimeError, "Error checking file status for %s on remote host" % (name)
        
    def empty_remote(self, remote_path):
        """
            Empties the remote path.
        """
        logging.debug("Removing " + remote_path)
        if self.exists_remotely(remote_path):
            logging.debug("Preparing to remove: " + str(self.sftp.listdir(remote_path)))
            list = self.sftp.listdir(remote_path)
            for file in list:
                full = join(remote_path, file)
                remote_stat = self.sftp.stat(full)                
                if (S_ISDIR(remote_stat.st_mode)):
                    logging.debug("Removing files in " + full + "...")
                    self.empty_remote(full)
                    logging.debug("Removing dir...")
                    self.sftp.rmdir(full)
                else:
                    logging.debug("Removing file...")
                    self.sftp.remove(full)

    def send_temp_to_destination(self):
        
        if self.exists_remotely(self.destination.path):
            
            # prepare the root
            self.sftp.chdir(self.destination.path)
            root = join(self.dir, "trunk")

            self.empty_remote(self.destination.path)
            if self.verbose:
                print "Emptied the remote deploy location."
            
            # get all the files and directories
            def send(args, dirname, filenames):
                logging.info("dir: " + dirname)
                path = self.destination.path
                if (dirname != root and dirname.startswith(root)):
                    path = join(self.destination.path, dirname[len(root)+1:len(dirname)])
                    logging.info("Creating directory " + path + " on remote host...")
                    try:
                        self.sftp.mkdir(path)
                    except IOError, e:
                        print "warning: could not create " + path + " on the destination.  Trying to continue."
                    self.sftp.chdir(path)
                    logging.info("Changing to that directory on remote host...")
                else:
                    logging.info(dirname + " == " + root + " - leaving as is.")
                for file in filenames:
                    if isfile(join(dirname, file)):
                        logging.info("file: " + file + " - sending it over")
                        source = join(dirname, file)
                        destination = join(self.destination.path, file)
                        logging.info("  from " + join(dirname, file))
                        logging.info("  to " + join(path, file))
                        if self.verbose:
                            print "Sending " + join(dirname, file) + " to " + join(path, file) + "..."
                        self.sftp.put(source, join(path, file), None)
                    else:
                        logging.warn("Oops: " + join(dirname, file) + " is not a file - discarding")
            
            # walk over the full tree
            walk(root, send, None)
        
        return True
        
    def is_proper_destination(self):
        # TODO: implement this!
        return True
    
    def cleanup(self):
        """
            All the files that are still open ar closed.
            And all the temporary directories are removed.
        """
        self.disconnect()
        return True
        
    def deploy(self):
        """
            Deploys source to destination while addressing the given properties. 
        """
                
        try:

            if self.is_proper_svn():
                logging.debug(str(self.source) + " can be deployed to " + str(self.destination))
            else:
                logging.warn(str(self.source) + " can not be used as deployment basis.")
                
            if self.export_source_to_temp():
                logging.debug("Exported system successfully.")
            else:
                logging.warn("Could not export the system.")
                
            if self.update_export():
                logging.debug("Updated the source successfully.")
            else:
                logging.warn("Could not update the source properly.")
    
            if self.send_temp_to_destination():
                logging.debug("Sent the updated source to the destination successfully.")
            else:
                logging.warn("Could send the updated source the system.")
                
            # TODO: tag the Subversion repository
            # TODO: add the release to the tag of specified

        finally:
            self.cleanup()
            
        print "Deployed the project to " + self.destination.host + self.destination.path + " successfully." 
                
if __name__ == "__main__":
    deployer = Deployer() 
    deployer.deploy()
    