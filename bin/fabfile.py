from fabric.api import run, env
from fabric.decorators import task
from fabric.colors import red, green, yellow

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
Environments
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
        print(config.items(environment))
        _add_properties(config.options(environment))
        return True
    else:
        print(red("Could not find the [" + environment + 
              "] section in '" + filename + "'."))
        return False
    
def _add_properties(properties):
    try:
        env.user = properties["user.username"]
        env.password = properties.get["user.password"]
        env.dbuser = properties.get["database.username"]
        env.dbpassword = properties.get["database.password"]
    except KeyError as ke:
        print("oops: " + str(ke))

def production():
    """
    Work on production environment
    """
    env.settings = 'production'
    env.hosts = ['$(production_domain)']
    env.user = '$(production_user)'
    env.password = '$(production_password)'

def staging():
    """
    Work on staging environment
    """
    env.settings = 'staging'
    env.hosts = ['$(staging_domain)'] 
    env.user = '$(staging_user)'
    env.password = '$(staging_password)'
    
def development():
    """
    Work on local development environment
    """
    env.settings = 'development'
    env.hosts = ['$(development_domain)'] 
    env.user = '$(development_user)'
    env.password = '$(development_password)'
    
"""
Branches
"""
def stable():
    """
    Work on stable branch.
    """
    env.branch = 'stable'

def master():
    """
    Work on development branch.
    """
    env.branch = 'master'

def branch(branch_name):
    """
    Work on any specified branch.
    """
    env.branch = branch_name

"""
Commands - setup
"""
def setup():
    """
    Setup a new website by installing everything we need, and fire up 
    the database.  Does NOT perform the functions of deploy().
    """
    require('settings', provided_by=[production, staging])
    require('branch', provided_by=[stable, master, branch])
    
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

@task()
def create_database():
    """
    Creates the user and database for this project.
    """
    run('echo "CREATE USER %(project_name)s WITH PASSWORD \'%(database_password)s\';" | psql postgres' % env)
    run('createdb -O %(project_name)s %(project_name)s -T template_postgis' % env)

@task()
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
    print("foo")
    _create_environment("foo", "development")
    _create_environment("fabfile.properties", "development")
    