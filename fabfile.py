from fabric.api import *

"""
Base configuration
"""
env.project_name = 'alltoez'
env.python = 'python2.7'
env.repository_url = 'https://github.com/devangmundhra/alltoez.git'

"""
Environments
"""
def production():
    """
    Work on production environment
    """
    env.settings = 'production'
    env.user = 'root'
    env.hosts = ['alltoez.com']
    env.path = '/home/django/sites/%(project_name)s' % env
    env.env_path = '%(path)s/env' % env
    env.repo_path = '%(path)s/repository' % env
    env.site_packages_path = '%(env_path)s/lib/python2.7/site-packages' % env

def staging():
    """
    Work on staging environment
    """
    env.settings = 'staging'
    env.user = 'alltoez'
    env.hosts = ['staging.alltoez.com']
    env.path = '/home/alltoez/sites/%(project_name)s' % env
    env.env_path = '%(path)s/env' % env
    env.repo_path = '%(path)s/repository' % env
    env.site_packages_path = '%(env_path)s/lib/python2.7/site-packages' % env

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
    Setup a fresh virtualenv, install everything we need

    Does NOT perform the functions of deploy().
    """
    require('settings', provided_by=[production, staging])
    require('branch', provided_by=[stable, master, branch])

    setup_directories()
    setup_virtualenv()
    clone_repo()
    checkout_latest()

    install_requirements()
    install_supervisor_conf()
    install_nginx_conf()
    reload_webserver()
    create_empty_db()

def refresh_configs():
    install_supervisor_conf()
    install_nginx_conf()

def refresh_requirements():
    """
    Refreshes the items in the requirements list, in case you have added additional dependences
    after having already run the main setup process
    """
    require('settings', provided_by=[production, staging])
    require('branch', provided_by=[stable, master, branch])

    checkout_latest()
    install_requirements()
    setup_symlinks()

def setup_directories():
    """
    Create directories necessary for deployment.
    """
    run('mkdir -p %(path)s' % env)
    run('mkdir -p %(env_path)s' % env)
    run('mkdir -p /home/%(user)s/logs/' % env)
    sudo('chown -R %(user)s:%(user)s ~/logs' % env)
    run('mkdir -p /home/celery/' % env)
    sudo('chown -R celery:celery /home/celery' % env)

def setup_virtualenv():
    """
    Setup a fresh virtualenv.
    """
    run('virtualenv -p %(python)s --no-site-packages %(env_path)s;' % env)
    with prefix('source %(env_path)s/bin/activate' % env):
        run('easy_install -U setuptools; easy_install pip;' % env)

def clone_repo():
    """
    Do initial clone of the git repository.
    """
    run('git clone --recursive %(repository_url)s %(repo_path)s' % env)

def checkout_latest():
    """
    Pull the latest code on the specified branch.
    """
    run('cd %(repo_path)s; git pull origin %(branch)s' % env)
    run('cd %(repo_path)s; git submodule init' % env)
    run('cd %(repo_path)s; git submodule update' % env)

def install_requirements():
    """
    Install the required packages using pip.
    """
    with prefix('source %(env_path)s/bin/activate' % env):
        run('pip install -r %(repo_path)s/requirements.txt' % env)
        run('npm install --prefix %(repo_path)s less' % env)
        run('npm install --prefix %(repo_path)s yuglify' % env)
        run('npm install --prefix %(repo_path)s coffee-script' % env)

def install_supervisor_conf():
    """
    Install the supervisor/gunicorn site config file.
    """
    sudo('rm -fr /etc/supervisor/conf.d/%(project_name)s.conf' % env)
    sudo('ln -s %(repo_path)s/%(project_name)s/configs/%(settings)s/supervisor.conf /etc/supervisor/conf.d/%(project_name)s.conf' % env)
    sudo('chmod a+x %(repo_path)s/%(project_name)s/configs/%(settings)s/server.sh' % env)
    sudo('chmod a+x %(repo_path)s/%(project_name)s/configs/%(settings)s/celery.sh' % env)
    sudo('chmod a+x %(repo_path)s/%(project_name)s/configs/%(settings)s/celerybeat.sh' % env)
    sudo('sudo supervisorctl reread')
    sudo('sudo supervisorctl update')

def install_nginx_conf():
    """
    Install the nginx site config file.
    """
    sudo('rm -fr /etc/nginx/sites-enabled/%(project_name)s.conf' % env)
    sudo('rm -fr /etc/nginx/sites-available/%(project_name)s.conf' % env)
    sudo('ln -s %(repo_path)s/%(project_name)s/configs/%(settings)s/nginx.conf /etc/nginx/sites-available/%(project_name)s.conf' % env)
    sudo('ln -s /etc/nginx/sites-available/%(project_name)s.conf /etc/nginx/sites-enabled/%(project_name)s.conf' % env)

def setup_symlinks():
    with prefix('source %(env_path)s/bin/activate' % env):
        run('python %(repo_path)s/%(project_name)s/configs/%(settings)s/manage.py collectstatic --noinput;' % env)

def create_empty_db():
    sudo('psql -U postgres -c "CREATE DATABASE %(project_name)s WITH TEMPLATE=template0 OWNER=postgres ENCODING=\'UTF8\'"' % env)
    with prefix('source %(env_path)s/bin/activate' % env):
        run('python %(repo_path)s/%(project_name)s/configs/%(settings)s/manage.py syncdb --noinput;' % env)
        run('python %(repo_path)s/%(project_name)s/configs/%(settings)s/manage.py migrate;' % env)

"""
Commands - deployment
"""

def deploy():
    """
    Deploy the latest version of the site to the server and restart gunicorn.

    Does not perform the functions of load_new_data().
    """
    require('settings', provided_by=[production, staging])
    require('branch', provided_by=[stable, master, branch])

    checkout_latest()
    setup_symlinks()

    # Run any migrations
    with prefix('source %(env_path)s/bin/activate' % env):
        run('python %(repo_path)s/%(project_name)s/configs/%(settings)s/manage.py migrate;' % env)

    sudo('supervisorctl restart %(project_name)s' % env)
    sudo('supervisorctl restart celery' % env)
    sudo('supervisorctl restart celerybeat' % env)

def reload_webserver():
    """
    Restart the web servers.
    """
    try:
        sudo('/etc/init.d/nginx restart')
    except:
        pass
    try:
        sudo('/etc/init.d/supervisor restart')
    except:
        pass
    #sudo('pkill supervisord')
    #sudo('supervisord')
    try:
        sudo('supervisorctl stop %(project_name)s' % env)
    except:
        pass
    sudo('supervisorctl start %(project_name)s' % env)

def reload_modwsgi():
    run('touch %(repo_path)s/%(project_name)s/configs/%(settings)s/%(settings)s.wsgi;' % env)

"""
Commands - rollback
"""
def rollback(commit_id):
    """
    Rolls back to specified git commit hash or tag.

    There is NO guarantee we have committed a valid dataset for an arbitrary
    commit hash.
    """
    require('settings', provided_by=[production, staging])
    require('branch', provided_by=[stable, master, branch])

    checkout_latest()
    git_reset(commit_id)

    reload_modwsgi()

def git_reset(commit_id):
    """
    Reset the git repository to an arbitrary commit hash or tag.
    """
    env.commit_id = commit_id
    run("cd %(repo_path)s; git reset --hard %(commit_id)s" % env)


"""
Commands - miscellaneous
"""

def clear_cache():
    """
    Restart memcache, wiping the current cache.
    """
    run('/etc/init.d/memcached restart')

def echo_host():
    """
    Echo the current host to the command line.
    """
    run('echo %(settings)s; echo %(hosts)s' % env)

def manage_command(command):
    """
    Execute management commands
    """
    env.command = command
    require('settings', provided_by=[production, staging])
    require('branch', provided_by=[stable, master, branch])
    with prefix('source %(env_path)s/bin/activate' % env):
        run('python %(repo_path)s/%(project_name)s/configs/%(settings)s/manage.py %(command)s;' % env)

def rebuild_index():
    """
    Rebuild haystack indexes
    """
    with prefix('source %(env_path)s/bin/activate' % env):
        run('python %(repo_path)s/%(project_name)s/configs/%(settings)s/manage.py rebuild_index;' % env)


def heroku_deploy():
    """
    Deploy to Heroku
    :return:
    """
    local('pip freeze > requirements.txt')
    local('python manage.py collectstatic --noinput')
    local('git add .')
    print("enter your git commit comment: ")
    comment = raw_input()
    local('git commit -m "%s"' % comment)
    local('git push -u origin master')
    local('heroku maintenance:on')
    local('git push heroku master')
    local('heroku run python manage.py migrate')
    local('heroku maintenance:off')