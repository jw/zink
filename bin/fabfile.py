from fabric.api import run, env
from fabric.decorators import task
from fabric.colors import red, green, yellow
from fabric.operations import require, sudo
from fabric.context_managers import show

"""
Base configuration
"""
env.project = "elevenbits"
env.repo = "https://hg.elevenbits.org"
env.path = '/var/www/%(project)s' % env

#
# old stuff
#

#env.database_password = '$(db_password)'
#env.site_media_prefix = "site_media"
#env.admin_media_prefix = "admin_media"
#env.newsapps_media_prefix = "na_media"
#env.path = '/home/newsapps/sites/%(project_name)s' % env
#env.log_path = '/home/newsapps/logs/%(project_name)s' % env
#env.env_path = '%(path)s/env' % env
#env.repo_path = '%(path)s/repository' % env
#env.apache_config_path = '/home/newsapps/sites/apache/%(project_name)s' % env
#env.python = 'python2.6'

"""
Some config stuff.
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
Where the source code is.
"""
@task
def tip():
    """
    Delpoy the tip.
    """
    env.branch = 'tip'

@task
def revision(revision="tip"):
    """
    Deploy a certain revision.  Default is the tip.
    """
    env.branch = revision

"""
Commands - setup
"""
@task
def setup():
    """
        Setup a new website by installing everything we need, and fire up 
        the database.  Does NOT perform the functions of deploy().
    """
    
    require('settings', provided_by=[production, staging, development])
    require('branch', provided_by=[tip, revision])

    print(green("Fabricating " + env.branch + " in " + env.settings + " environment..."))
    
    setup_directories()    
    if (env.branch == "tip"):
        checkout_latest()
    else:
        checkout_revision(env.branch)
    install_requirements()
    update_database()

    print(green("Setup complete."))
    
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
    sudo('hg clone %(repo)s/elevenbits %(path)s' % env, user="www-data")

def checkout_revision(revision):
    """
        Clone a revision.
    """
    sudo('hg clone -r %(branch)s %(repo)s/elevenbits %(path)s' % env, user="www-data")

def install_requirements():
    """
        Todo: install the required packages using pip.
    """
    print(orange("Not installing requirements yet.  Need to do this yourself for now..."))
    #run('source %(env_path)s/bin/activate; pip install -E %(env_path)s -r %(repo_path)s/requirements.txt' % env)

def update_database():
    """
        Creates a user and a database.
    """

    # check if user is already there
    output = run('echo "SELECT 1 FROM pg_roles WHERE rolname=\'%(dbuser)s\';" | psql postgres -tA' % env)
    if (output == "1"):
        print(green("Good.  User '%(dbuser)s' exists." % env))
    else:
        # if not, create it
        print(green("Creating user '%(dbuser)s'." % env))
        output = run('echo "CREATE USER %(dbuser)s WITH PASSWORD \'%(dbpassword)s\';" | psql postgres -tA' % env)
        if (output == "CREATE DATABASE"):
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

def destroy_database():
    """
        Destroys the user and database for this project.
        Will not cause the fab to fail if they do not exist.
    """
    with settings(warn_only=True):
        run('dropdb %(project_name)s' % env)
        run('dropuser %(project_name)s' % env)
        
def load_data():
    """
        Loads data from the repository into PostgreSQL.
    """
    run('psql -q %(project_name)s < %(path)s/repository/data/psql/dump.sql' % env)
    run('psql -q %(project_name)s < %(path)s/repository/data/psql/finish_init.sql' % env)
    
def deploy_static():
    with cd(env.project_root):
        run('./manage.py collectstatic -v0 --noinput')
        
def deploy():
    """
        Deploys the website
    """
    create_database()
    populate_database()
    get_current_trunk_and_tag_it()
    deploy_statics()
    deploy()
    check()
    push_back()
    