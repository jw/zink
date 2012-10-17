from fabric.api import run, env
from fabric.decorators import task
from fabric.colors import red, green, yellow
from fabric.operations import require, sudo
from fabric.context_managers import show, settings, cd
from fabric.utils import abort
from fabric.contrib import django

"""
Base configuration
"""
env.project = "elevenbits"
env.repo = "hg.elevenbits.org"
env.path = '/var/www/%(project)s' % env

"""
Some config utility methods
"""
def _create_environment(filename, environment):
    """
        Creates the correct env keys for an environment using a given
        configuration filename.
    """
    from ConfigParser import SafeConfigParser
    from os.path import isfile
    if not isfile(filename):
        print(red("Configuration file '" + filename + "' does not exist."))
        return False
    config = SafeConfigParser()
    config.read(filename)
    if environment in config.sections():
        env.settings = environment
        return _add_properties(config, environment)
    else:
        print(red("Could not find the [" + environment + 
              "] section in '" + filename + "'."))
        return False
    
def _add_properties(config, section):
    from ConfigParser import NoOptionError
    try:
        env.user = config.get(section, "user.username")
        env.password = config.get(section, "user.password")
        env.dbuser = config.get(section, "db.username")
        env.dbpassword = config.get(section, "db.password")
        env.dbname = config.get(section, "db.name")
        env.hosts = [ config.get(section, "host") ]
        return True
    except NoOptionError as noe:
        print(red("Could not find the '" + noe.option + 
              "' key in the '" + noe.section + "' section."))
        return False

"""
The three environments.
"""
@task
def production():
    """
        Build for a Production environment.
    """
    _create_environment("fabfile.properties", "production")

@task
def staging():
    """
        Build for a Staging environment.
    """
    _create_environment("fabfile.properties", "staging")

@task
def development():
    """
        Build for a Development environment.
    """
    _create_environment("fabfile.properties", "development")

"""
Where to get the code.
"""
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

"""
Deploy
"""
@task
def deploy():
    """
        Setup a new website by installing everything we need, and fire up 
        the database.  Then deploys the site.
    """
    
    require('settings', provided_by=[production, staging, development])
    require('branch', provided_by=[tip, revision])

    print(green("Fabricating " + env.branch + " in " + env.settings + " environment..."))

    # when deploying to production, first get the latest 
    # content and store it in the repo
    if (env.branch == "tip" and env.settings == "production"):
        update_fixtures()
    
    setup_directories()    

    if (env.branch == "tip"):
        checkout_latest()
    else:
        checkout_revision(env.branch)

    install_requirements()

    #drop_database()
    create_database()
    populate_database()
    restart_database()
    
    update_webserver()
    restart_webserver()
    
    print(green("Setup complete."))

"""
Tasks to help in deployment
"""

def setup_directories():
    """
        Create directories necessary for deployment.
    """
    sudo("rm -rf %(path)s" % env)
    sudo("mkdir -p %(path)s" % env)
    sudo("chown www-data:www-data %(path)s" % env)
    
def checkout_latest():
    """
        Get latest version from repository.
    """
    sudo('hg clone https://%(user)s:%(password)s@%(repo)s/elevenbits %(path)s' % env, user="www-data")

def checkout_revision(revision):
    """
        Clone a revision.
    """
    sudo('hg clone -r %(branch)s https://%(user)s:%(password)s@%(repo)s/elevenbits %(path)s' % env, user="www-data")

def install_requirements():
    """
        Install the required packages using pip.
    """
    
    sudo('pip install -r %(path)s/requirements.txt' % env)
    print(yellow("Most likely only installed some of the required packages.  You still need to do check this yourself for now..."))

@task
def update_fixtures():
    """
        Dumping the latest content of the portal and adding it to the repo
    """
    with cd(env.path):
        sudo('python manage.py dumpdata --indent 4 static > %(path)s/fixtures/static.json' % env, user="www-data")
        sudo('python manage.py dumpdata --indent 4 treemenus > %(path)s/fixtures/treemenus.json' % env, user="www-data")
        sudo('python manage.py dumpdata --indent 4 blog > %(path)s/fixtures/blog.json' % env, user="www-data")
        sudo('hg commit -m "Automatically committed latest content to repo when deploying"' % env, user="www-data")
        sudo('hg push https://%(user)s:%(password)s@%(repo)s/elevenbits')

def create_database():
    """
        Creates a user and a database.
    """

    # check if user is already there
    print('echo "SELECT 1 FROM pg_roles WHERE rolname=\'%(dbuser)s\';" | psql postgres -tA' % env)
    output = run('echo "SELECT 1 FROM pg_roles WHERE rolname=\'%(dbuser)s\';" | psql postgres -tA' % env)
    print("output: " + output)
    if (output == "1"):
        print(green("Good.  User '%(dbuser)s' exists." % env))
    else:
        # if not, create the user
        print(green("Creating user '%(dbuser)s'." % env))
        output = run('echo "CREATE ROLE %(dbuser)s WITH PASSWORD \'%(dbpassword)s\';" | psql postgres -tA' % env)
        if (output == "CREATE DATABASE" or output == "CREATE ROLE"):
            print(green("Created user successfully."))
        else:
            print(red("Could not create user."))
            abort("User creation error.")

    # check if the database is already there 
    output = run('echo "SELECT 1 from pg_database WHERE datname=\'%(dbname)s\';" | psql postgres -tA' % env)
    if (output == "1"):
        print(green("Good.  Database '%(dbname)s' exists." % env))
    else:
        # if not, create it
        print(green("Creating database '%(dbname)s'..." % env))
        output = run('echo "CREATE DATABASE %(dbname)s OWNER %(dbuser)s;" | psql postgres -tA' % env)
        if (output == "CREATE DATABASE"):
            print(green("Created database successfully."))
        else:
            print(red("Could not create database."))
            abort("Database creation error.")

def drop_database():
    """
        Destroys the user and database for this project.
        Will not cause the fab to fail if they do not exist.
    """
    with settings(warn_only=True):
        run('dropdb %(dbname)s' % env)
        run('dropuser %(dbuser)s' % env)

@task
def update_deployment_time():
    # get date and time
    from datetime import datetime
    now = datetime.now()
    deployment_time = now.strftime("%d.%m.%Y, %H%Mhrs");
    print("Deployment time is " + deployment_time)
    # first get Django access
    from os import environ
    from sys import path
    path.append(env.path)
    environ.setdefault("DJANGO_SETTINGS_MODULE", "elevenbits.settings")
    with cd(env.path):
        # get the version
        from elevenbits.templatetags import revision
        version = revision.get_gh_revision()
        # TODO: get tag
        tag = "n/a"
        # add this development
        from elevenbits.deployment.models import Deployment
        deployment = Deployment(tag=tag, timestamp=now, version=version, deployer='Deployed via Fabric.')
        deployment.save()
        
def populate_database():
    """
        Loads (mostly fixture) data in the database.
    """
    with cd(env.path):
        run('./manage.py syncdb')
        run('./manage.py loaddata static.json')
        run('./manage.py loaddata treemenus.json')
        run('./manage.py loaddata blog.json')
    # update the deployment time
    with cd(env.path + "/bin"):
        run('fab update_deployment_time')

def restart_database():
    sudo("/etc/init.d/postgresql restart")
    
def restart_webserver():
    sudo("/etc/init.d/cherokee restart")
    
def update_webserver():
    """
        TODO: Updates the Cherokee webserver
    """
    print(yellow("Not updating the Cherokee webserver yet.  You still need to do this yourself for now..."))
    
