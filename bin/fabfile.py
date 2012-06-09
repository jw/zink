from fabric.api import run, env
from fabric.decorators import task
from fabric.colors import red, green, yellow
from fabric.operations import require

"""
Base configuration
"""
#env.project_name = '$(project)'
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
    Work on the tip.
    """
    env.branch = 'tip'

@task
def revision(revision):
    """
    Work on a revision in the hg.
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
    
    """
    setup_directories()
    setup_virtualenv()
    clone_repo()
    checkout_latest()
    destroy_database()
    create_database()
    load_data()
    install_requirements()
    install_apache_conf()
    deploy_requirements_to_s3()
    """
    print("hello!")
    
    
def setup_directories():
    """
    Create directories necessary for deployment.
    """
    run('mkdir -p %(path)s' % env)
    run('mkdir -p %(env_path)s' % env)
    run ('mkdir -p %(log_path)s;' % env)
    sudo('chgrp -R www-data %(log_path)s; chmod -R g+w %(log_path)s;' % env)
    run('ln -s %(log_path)s %(path)s/logs' % env)
    
def setup_virtualenv():
    """
    Setup a fresh virtualenv.
    """
    run('virtualenv -p %(python)s --no-site-packages %(env_path)s;' % env)
    run('source %(env_path)s/bin/activate; easy_install -U setuptools; easy_install pip;' % env)

def clone_repo():
    """
    Do initial clone of the git repository.
    """
    run('git clone git@tribune.unfuddle.com:tribune/%(project_name)s.git %(repo_path)s' % env)

def checkout_latest():
    """
    Pull the latest code on the specified branch.
    """
    run('cd %(repo_path)s; git checkout %(branch)s; git pull origin %(branch)s' % env)

def install_requirements():
    """
    Install the required packages using pip.
    """
    run('source %(env_path)s/bin/activate; pip install -E %(env_path)s -r %(repo_path)s/requirements.txt' % env)

def install_apache_conf():
    """
    Install the apache site config file.
    """
    sudo('cp %(repo_path)s/%(project_name)s/configs/%(settings)s/%(project_name)s %(apache_config_path)s' % env)

def deploy_requirements_to_s3():
    """
    Deploy the latest newsapps and admin media to s3.
    """
    run('s3cmd del --recursive s3://%(s3_bucket)s/%(project_name)s/%(admin_media_prefix)s/' % env)
    run('s3cmd -P --guess-mime-type sync %(env_path)s/src/django/django/contrib/admin/media/ s3://%(s3_bucket)s/%(project_name)s/%(site_media_prefix)s/' % env)
    run('s3cmd del --recursive s3://%(s3_bucket)s/%(project_name)s/%(newsapps_media_prefix)s/' % env)
    run('s3cmd -P --guess-mime-type sync %(env_path)s/src/newsapps/newsapps/na_media/ s3://%(s3_bucket)s/%(project_name)s/%(newsapps_media_prefix)s/' % env)

@task
def create_database():
    """
    Creates the user and database for this project.
    """
    run('echo "CREATE USER %(project_name)s WITH PASSWORD \'%(database_password)s\';" | psql postgres' % env)
    run('createdb -O %(project_name)s %(project_name)s -T template_postgis' % env)

@task
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
    
def pgpool_down():
    """
    Stop pgpool so that it won't prevent the database from being rebuilt.
    """
    sudo('/etc/init.d/pgpool stop')
    
def pgpool_up():
    """
    Start pgpool.
    """
    sudo('/etc/init.d/pgpool start')



def deploy_static():
    with cd(env.project_root):
        run('./manage.py collectstatic -v0 --noinput')
        
def deploy():
    "Deploys the website to elevenbits.org"
    create_database()
    populate_database()
    get_current_trunk_and_tag_it()
    deploy_statics()
    deploy()
    check()
    push_back()

@task()
def foo():
    """start a shell within the current context"""
    #_create_environment("foo", "development")
    _create_environment("fabfile.properties", "development")
    
    