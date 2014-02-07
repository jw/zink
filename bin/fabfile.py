
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

from fabric.api import run, env
from fabric.operations import put
from fabric.decorators import task
from fabric.colors import red, green, yellow
from fabric.operations import require, sudo
from fabric.context_managers import settings, cd
from fabric.utils import abort
from fabric.contrib import django

from os import makedirs
from os.path import join, dirname, realpath, exists, isfile
from ConfigParser import SafeConfigParser, NoOptionError
from string import Template

#
# Defaults
#

CONFIGURATION_FILE = "fabfile.properties"

DEVELOPMENT = "development"
PRODUCTION = "production"
STAGING = "staging"

#
# Base configuration first
#

# repository is https://elevenbits@bitbucket.org/elevenbits/zink
env.name = "zink"
env.repo = "bitbucket.org"
env.account = "elevenbits"

# deployment properties
env.prefix = '/var/www'
env.remote = env.path = "%(prefix)s/%(name)s" % env
env.local = dirname(realpath(join(__file__, "..")))
print("local: %s." % env.local)
print("remote: %s" % env.remote)

# TODO: handle these properly
env.upload = "%(prefix)s/%(name)s/static/upload" % env
env.media = "%(prefix)s/%(name)s/media" % env


#
# First some config utility and property retrieval methods
#


def _create_environment(filename, environment):
    """
    Create the correct env keys for an environment using a given configuration
    filename. Also the properties of the project are retrieved.
    @param filename: the filename to be read as configuration.
    @param environment: the section in the filename to be used as
    configuration file.
    """
    from ConfigParser import SafeConfigParser
    from os.path import isfile
    if not isfile(filename):
        print(red("Configuration file '%s' does not exist." % filename))
        abort("Could not find configuration file %s." % filename)
    config = SafeConfigParser()
    config.read(filename)
    if environment in config.sections():
        env.settings = environment
        _add_environment_properties(config, environment)
        _add_project_properties(env.name)
    else:
        print(red("Could not find the [%s] section in '%s'.") %
              (environment, filename))
        abort("Could not find the [%s] section in '%s'." %
              (environment, filename))


def _add_project_properties(name):
    """
    Read the project.properties file and add the different sections into
    the env.project as a dict. There should be three sections: project, email
    and twitter.
    """
    filename = name + ".properties"
    print("Getting properties of project '%s'..." % filename)
    if not isfile(filename):
        print(red("Configuration file '%s' does not exist." % filename))
        abort("Could not find configuration file %s." % filename)

    # read the file
    config = SafeConfigParser()
    config.read(filename)

    # check the three sections
    if "email" not in config.sections():
        abort("Missing the email section in %s." % filename)
    if "twitter" not in config.sections():
        abort("Missing the twitter section in %s." % filename)
    if "project" not in config.sections():
        abort("Missing the project section in %s." % filename)

    # read and handle them
    env["project"] = {}
    env["project"]["name"] = name
    try:
        env["project"]["key"] = config.get("project", "key")
    except NoOptionError:
        abort("No key entry found in project section in the %s file." %
              filename)
    try:
        _add_email_properties(config)
        _add_twitter_properties(config)
    except NoOptionError as noe:
        abort("Could not find the '" + noe.option +
              "' key in the '" + noe.section + "' section.")


def _add_email_properties(config):
    """
    Add the email properties to the env["project"]["email"] as a dict.
    """
    e = env["project"]["email"] = {}
    e["host"] = config.get("email", "host")
    e["port"] = config.get("email", "port")
    e["user"] = config.get("email", "user")
    e["password"] = config.get("email", "password")
    e["tls"] = config.get("email", "tls")


def _add_twitter_properties(config):
    """
    Add the twitter properties to the env["project"]["twitter"] as a dict.
    """
    t = env["project"]["twitter"] = {}
    t["name"] = config.get("twitter", "name")
    t["consumer.key"] = config.get("twitter", "consumer.key")
    t["consumer.secret"] = config.get("twitter", "consumer.secret")
    t["oauth.token"] = config.get("twitter", "oauth.token")
    t["oauth.token.secret"] = config.get("twitter", "oauth.token.secret")


def _add_environment_properties(config, section):
    """
    Get the database entries of a environment section from a config parser.
    @param config: a ConfigParser.
    @param section: a section in an ini file, e.g. staging, or production.
    """
    from ConfigParser import NoOptionError
    try:
        env.user = config.get(section, "user.username")
        env.password = config.get(section, "user.password")
        env.dbuser = config.get(section, "db.username")
        env.dbpassword = config.get(section, "db.password")
        env.dbname = config.get(section, "db.name")
        env.hosts = [config.get(section, "host")]
        return True
    except NoOptionError as noe:
        print(red("Could not find the '" + noe.option +
              "' key in the '" + noe.section + "' section."))
        abort("Could not find the '" + noe.option +
              "' key in the '" + noe.section + "' section.")


#
# The three environments.
#


@task
def production():
    """
    Build for a Production environment.

    Files will come from the repository.
    Secret environment properties (like email, twitter,...) are
    retrieved from the zink.properties file, then they are inserted
    in the local_settings.py
    """
    _create_environment(CONFIGURATION_FILE, PRODUCTION)


@task
def staging():
    """
    Build for a Staging environment.

    Files will come from the repository.
    Secret environment properties (like email, twitter,...) are
    retrieved from the zink.properties file, then they are inserted
    in the local_settings.py
    """
    _create_environment(CONFIGURATION_FILE, STAGING)


@task
def development():
    """
    Build for a Development environment.

    Files will come from the repository, or (when in tip) from the users
    drive.  When not in tip, the secret environment properties (like email,
    twitter,...) are retrieved from the zink.properties file and
    inserted in the local_settings.py.  When in tip, the current
    local_settings.py is used as is.
    """
    _create_environment(CONFIGURATION_FILE, DEVELOPMENT)


#
# The branch to deploy
#


@task
def tip():
    """
    Deploy the tip.
    """
    env.branch = 'tip'


@task
def revision(revision="tip"):
    """
    Deploy a certain revision.  Default is the tip.
    """
    env.branch = revision


#
# The tasks
#


@task
def check_database():
    # prepare_user
    # prepare_postgres
    pass


@task
def user_ready():
    pass


@task
def deploy():
    """
    Install everything we need, and fire up the database.  Then start the
    server.
    """

    require('settings', provided_by=[production, staging, development])
    require('branch', provided_by=[tip, revision])

    print(green("Fabricating %s in %s environment..." %
                (env.branch, env.settings)))

    remove_previous_releases()
    create_prefix_directory()

    if env.settings == "development" and env.branch == "tip":
        print(green("Deploying hot development trunk..."))
        if database_user_exists() and database_exists():
            copy_current()
        else:
            print(red("Database user or database not available."))
            abort("Database user or database not available.")
    else:
        print(green("Creating..."))
        create_root_directory()

        # TODO: make a backup of the staging|production database environment
        # TODO: create a new revision

        print(green("Getting files from repository..."))
        if env.branch == "tip":
            checkout_latest()
        else:
            checkout_revision(env.branch)

        create_local_settings()

        install_requirements()

        create_user()
        create_database()
        populate_database()
        restart_database()

        add_cronjob()  # checks existence of some core processes

    #create_upload_directory()

    print(green("Checking to see if uwsgi is an upstart job..."))
    handle_uwsgi_upstart()

    print(green("Updating nginx and uwsgi configuration..."))
    update_webserver_and_uwsgi_configuration()

    print(green("Restarting nginx and uwsgi..."))
    restart_webserver()

    print(green("Setup complete."))

#
# Tasks to help in deployment
#


def add_cronjob():
    """
        Add a cronjob which checks for the correct processes to be running.
    """
    sudo("cp %(path)s/conf/processes /etc/cron.d/processes" % env)


def remove_previous_releases():
    sudo("rm -rf %(path)s" % env)


def create_prefix_directory():
    sudo("mkdir -p %(prefix)s" % env)


def create_root_directory():
    """
        Create directories necessary for deployment.
    """
    sudo("mkdir -p %(path)s" % env)
    sudo("chown www-data:www-data %(path)s" % env)


def copy_current():
    sudo('cp -r %(local)s %(prefix)s' % env)
    sudo("chown www-data:www-data --recursive %(path)s" % env)


@task
def create_local_settings():
    d = {}
    # project
    d["project_key"] = env["project"]["key"]
    # database
    d["db_name"] = env.dbname
    d["db_username"] = env.dbuser
    d["db_password"] = env.dbpassword
    # email
    d["email_host"] = env["project"]["email"]["host"]
    d["email_port"] = env["project"]["email"]["port"]
    d["email_user"] = env["project"]["email"]["user"]
    d["email_password"] = env["project"]["email"]["password"]
    d["email_tls"] = env["project"]["email"]["tls"]
    # twitter
    t = env["project"]["twitter"]
    d["twitter_name"] = t["name"]
    d["twitter_consumer_key"] = t["consumer.key"]
    d["twitter_consumer_secret"] = t["consumer.secret"]
    d["twitter_oauth_token"] = t["oauth.token"]
    d["twitter_oauth_token_secret"] = t["oauth.token.secret"]
    # get the template...
    with open("template.py") as f:
        s = Template(f.read())
    # ...substitute the values...
    reply = s.substitute(d)
    # ...and save it
    with open("/tmp/foobar.py", "w") as f:
        f.write(reply)
    sudo("mkdir -p %(remote)s/elevenbits/" % env, user="www-data")
    put("/tmp/foobar.py",
        "%(remote)s/elevenbits/local_settings.py" % env,
        use_sudo=True)
    sudo("chown www-data:www-data %(remote)s/elevenbits/local_settings.py" %
         env)


# TODO: check this - this seems wrong
def create_upload_directory():
    """Allow write access by group on upload directory"""
    sudo("mkdir -p %(upload)s" % env)
    sudo("chown www-data:www-data --recursive %(upload)s" % env)
    sudo("chmod 777 %(upload)s" % env)
    sudo("ls -al %(upload)s" % env)


def checkout_latest():
    """Get latest version from repository."""
    sudo('hg clone '
         'https://%(account)s@%(repo)s/%(account)s/%(name)s '
         '%(path)s' % env, user="www-data")


def checkout_revision(revision):
    """Clone a revision."""
    sudo('hg clone -r %(branch)s '
         'https://%(account)s@%(repo)s/$(account)s/%(name)s '
         '%(path)s' % env, user="www-data")


def install_requirements():
    """
        Install the required packages using pip.
    """
    sudo('pip install -r %(path)s/requirements.txt' % env)
    print(green("Some required packages are installed."))
    print(yellow("Some packages might be missing."))
    print(yellow("You still need to do check this yourself for now..."))


@task
def backup():
    """
    Dump the latest content of the portal and add it to the repository.
    """
    with cd(env.path):
        print(env.local)
        sudo('python manage.py dumpdata --indent 4 static > '
             '%(local)s/fixtures/static.json' % env)
        sudo('python manage.py dumpdata --indent 4 treemenus > '
             '%(local)s/fixtures/treemenus.json' % env)
        sudo('python manage.py dumpdata --indent 4 blog > '
             '%(local)s/fixtures/blog.json' % env)
        sudo('python manage.py dumpdata --indent 4 index > '
             '%(local)s/fixtures/index.json' % env)
        sudo('python manage.py dumpdata --indent 4 services > '
             '%(local)s/fixtures/services.json' % env)
        # TODO: save these to the repo?


#
# Database handling
#


# check user and database

def database_user_exists():
    """
    Check if the database user exists.
    """
    output = run('echo "SELECT 1'
                 '      FROM pg_roles'
                 '      WHERE rolname=\'%(dbuser)s\' and'
                 '            rolcreatedb is true and'
                 '            rolcanlogin is true;"'
                 ' | psql postgres -tA' % env)
    if "1" in output:
        print(green("Good.  User '%(dbuser)s' exists." % env))
        return True
    else:
        return False


def database_exists():
    """
    Check if the database exists.
    """
    output = run('echo "SELECT 1 '
                 '      FROM pg_database '
                 '      WHERE datname=\'%(dbname)s\'; "'
                 '| psql postgres -tA' % env)
    if "1" in output:
        print(green("Good.  Database '%(dbname)s' exists." % env))
        return True
    else:
        return False


# create user and database

def create_user():
    """
    Create a database user.
    """
    if not database_user_exists():
        print(green("Creating user '%(dbuser)s'." % env))
        output = run('echo "CREATE ROLE %(dbuser)s'
                     '      WITH PASSWORD \'%(dbpassword)s\''
                     '      CREATEDB LOGIN;"'
                     ' | psql postgres -tA' % env)
        print(yellow("The current output: %s." % output))
        if "CREATE ROLE" in output:
            print(green("Created user successfully."))
        else:
            print(red("Could not create user."))
            abort("User creation error.")


def create_database():
    if not database_exists():
        print(green("Creating database '%(dbname)s'..." % env))
        output = run('echo "CREATE DATABASE %(dbname)s OWNER %(dbuser)s;" '
                     '| psql postgres -tA' % env)
        if output == "CREATE DATABASE":
            print(green("Created database successfully."))
        else:
            print(red("Could not create database."))
            abort("Database creation error.")


# drop and populate database

@task
def drop_database():
    """Destroys the database for this project."""
    with settings(warn_only=True):
        run('dropdb %(dbname)s' % env)


@task
def drop_user():
    """Destroys the database for this project."""
    with settings(warn_only=True):
        run('dropuser %(dbuser)s' % env)


@task
def populate_database():
    """
        Loads (mostly fixture) data in the database.
    """
    with cd(env.path):
        run('./manage.py syncdb')
        run('./manage.py migrate')
        run('./manage.py loaddata static.json')
        run('./manage.py loaddata treemenus.json')
        run('./manage.py loaddata menu_extras.json')
        run('./manage.py loaddata blog.json')
    # update the deployment time
    with cd(env.path + "/bin"):
        run('fab update_deployment_time')


@task
def update_deployment_time():
    """
    Updates the deployment time on the machine where the website is being
    deployed.
    """
    # get date and time
    from datetime import datetime
    now = datetime.now()
    deployment_time = now.strftime("%d.%m.%Y, %H%Mhrs")
    print(green("Deployment time is " + deployment_time + "."))
    # first get Django access
    from sys import path
    path.append(env.path)
    django.settings_module('elevenbits.settings')
    with cd(env.path):
        # get the version
        from elevenbits.templatetags import revision
        version = revision.get_hg_revision()
        # TODO: get tag
        tag = "n/a"
        # add this development
        from elevenbits.deployment.models import Deployment
        deployment = Deployment(tag=tag, timestamp=now, version=version,
                                deployer='Deployed via Fabric.')
        deployment.save()


#
# Manage database and webserver runtime
#

def restart_database():
    sudo("service postgresql restart")


def restart_webserver():
    sudo("service nginx restart")
    sudo("service uwsgi restart")


def update_webserver_and_uwsgi_configuration():
    # remove default first if it is there
    if exists("/etc/nginx/sites-enabled/default"):
        with settings(warn_only=True):
            sudo("rm /etc/nginx/sites-enabled/default")
    # update nginx
    sudo("mkdir -p /etc/nginx/sites-available" % env)
    sudo("cp %(path)s/conf/%(host)s.conf /etc/nginx/sites-available" % env)
    sudo("ln -sf %(path)s/conf/%(host)s.conf "
         "/etc/nginx/sites-enabled/%(host)s.conf" % env)
    # update uwsgi
    sudo("mkdir -p /etc/uwsgi/apps-available" % env)
    sudo("mkdir -p /etc/uwsgi/apps-enabled" % env)
    sudo("cp %(path)s/conf/django.ini /etc/uwsgi/apps-available" % env)
    sudo("ln -sf %(path)s/conf/django.ini "
         "/etc/uwsgi/apps-enabled/django.ini" % env)


def uwsgi_is_upstart_job():
    if exists("/etc/init/uwsgi.conf"):
        output = run("initctl list", quiet=True)
        if "uwsgi" in output:
            return True
        else:
            return False
    else:
        return False


def handle_uwsgi_upstart():
    """Make sure that uwsgi is an upstart job."""
    if uwsgi_is_upstart_job():
        print("uwsgi seems to be an upstart job. Leaving as is.")
    else:
        print("Forcing uwsgi to be an upstart job...")
        sudo("cp %(path)s/conf/uwsgi.conf /etc/init" % env)
        sudo("initctl reload uwsgi")
        if uwsgi_is_upstart_job():
            print(green("Good. uwsgi is now an upstart job."))
        else:
            print(red("Could not make uwsgi an upstart job. Please check."))
