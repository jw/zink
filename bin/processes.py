#!/usr/bin/env python

#
# Copyright (C) 2013-2014 Jan Willems (ElevenBits)
#
# This file is part of Zink.
#
# Zink is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Zink is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with Zink.  If not, see <http://www.gnu.org/licenses/>.
#

"""
    Checks existence of some processes, when a process does not exist,
    a mail is sent.

    The ``processes.properties`` file contains the processes and the mail
    properties.  This properties file must look like:

    [processes]
    names = nginx, uwsgi, postgres, django

    [mail]
    host = <host>
    port = <port>
    username = <username>
    password = <password>
"""

#
# This is a Python 3 based class, with some changes to make it Python 2.7
# compliant.
#

from subprocess import Popen, PIPE
from re import split
try:
    from configparser import ConfigParser
except ImportError:
    # python 2.7
    from ConfigParser import SafeConfigParser as ConfigParser
from os.path import exists


class Properties():
    """The properties file contents."""

    def __init__(self, filename):
        parser = ConfigParser()
        parser.read(filename)
        self.host = parser.get('mail', 'host')
        self.port = parser.get('mail', 'port')
        self.username = parser.get('mail', 'username')
        self.password = parser.get('mail', 'password')
        self.processes = parser.get('processes', 'names').split()
        print(self.processes)


# FIXME: this is a bad class
class Process(object):
    """
        Data structure for a process.
    """

    def __init__(self, proc_info):
        self.user = proc_info[0]
        self.pid = proc_info[1]
        self.cpu = proc_info[2]
        self.mem = proc_info[3]
        self.vsz = proc_info[4]
        self.rss = proc_info[5]
        self.tty = proc_info[6]
        self.stat = proc_info[7]
        self.start = proc_info[8]
        self.time = proc_info[9]
        self.cmd = proc_info[10]

    def to_str(self):
        """
            Returns a string containing minimalistic info
            about the process: user, pid, and command
        """
        return '%s %s %s' % (self.user, self.pid, self.cmd)


def get_proc_list():
    """
        Retrieves a list [] of Process objects representing the active
        process list.
    """

    proc_list = []
    sub_proc = Popen(['ps', 'aux'], shell=False, stdout=PIPE)
    sub_proc.stdout.readline()
    for line in sub_proc.stdout:
        # the separator for splitting is a 'variable number of spaces'
        proc_info = split(" *", line.strip())
        proc_list.append(Process(proc_info))
    return proc_list


def missing_processes(properties):
    """
        Returns missing processes.
    """

    process_list = get_proc_list()

    valid = set([])

    for process in process_list:
        for check in properties.processes:
            if check in process.cmd:
                valid.add(check)

    return properties.processes - valid


def send_mail(host, port, username, password, subject, missing):
    """
        Send a mail informing the receiver a set of processes are missing.
    """

    import smtplib
    import string

    FROM = username
    TO = username

    SUBJECT = subject

    if len(missing) is 1:
        message = "The " + missing.pop() + " process is missing...\n"
    else:
        message = "Missing these processes:\n"
        for process in missing:
            message += " - " + process + "\n"

    BODY = (
        "Hello,\n" + "\n" + message + "\n",
        "Please investigate,\n" + "Your machine"
    )

    body = string.join((
        "From: %s" % FROM,
        "To: %s" % TO,
        "Subject: %s" % SUBJECT,
        "",
        BODY), "\r\n")

    server = smtplib.SMTP(host, port)
    #server.set_debuglevel(2)
    server.ehlo()
    server.starttls()
    server.ehlo()
    server.login(username, password)
    server.sendmail(FROM, [TO], body)
    server.quit()


if __name__ == "__main__":

    import argparse
    parser = argparse.ArgumentParser(version="1.0")
    parser.add_argument("--properties", required=True, dest="file",
                        help="properties file location is required")
    results = parser.parse_args()
    if not exists(results.file):
        print("Given file does not exist: %s - bailing out." % results.file)
    else:
        properties = Properties(results.file)
        missing = missing_processes(properties)
        if not missing:
            print("No issues. Good!")
        else:
            print("Missing process(es), sending a mail...")
            send_mail(properties.host,
                      properties.port,
                      properties.username,
                      properties.password,
                      "Website offline!",
                      missing)
