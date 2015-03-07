from fabric.api import local, task, settings, env, run, cd
from fabtools import deb, require, deb
from fabtools.python import virtualenv, install_requirements
from fabtools.require import postgres
from fabtools import user
from fabric.contrib.files import append, exists
import configuration, os

env.hosts = configuration.HOSTS
env.user = configuration.INITIAL_OPERATING_SYSTEM_USER
                  
@task
def create_virtualenv(virtualenv_path):
    require.python.virtualenv(virtualenv_path, use_sudo=True)

@task
def install_virtualenv_requirements():
    
    with virtualenv(configuration.VIRTUALENV_PATH):
        install_requirements(configuration.REQUIREMENTS_FILE, use_sudo=True)

@task
def install_os_packages(packages):

    with settings():
        deb.install(packages)

@task
def create_project_path():
    env.user = configuration.NEW_OPERATING_SYSTEM_USER
    run('sudo mkdir -p %s' % configuration.PROJECT_PATH)
    run('mkdir -p %s' % configuration.STATIC_FILES_PATH)

@task
def create_backup_path():
    run('mkdir -p %s' % configuration.BACKUP_PATH)

@task
def clone_git_repo():
    run("cd %s && sudo git clone %s ." % (configuration.PROJECT_PATH, configuration.GIT_REPO_URL))

@task
def git_pull():
    with cd(configuration.PROJECT_PATH):
        run("sudo git pull")

@task
def create_nginx_conf():

    sites_available = "/etc/nginx/sites-available/%s" % configuration.PROJECT_NAME
    sites_enabled = "/etc/nginx/sites-enabled/%s" % configuration.PROJECT_NAME

    append(sites_available, configuration.nginx_conf, use_sudo=True)

    run('sudo ln -s %s %s' % (sites_available, sites_enabled))
    
    # This removes the default configuration profile for Nginx
    run('sudo rm -v /etc/nginx/sites-enabled/default')

@task
def create_uwsgi_conf():

    apps_available = "/etc/uwsgi/apps-available/%s.ini" % configuration.PROJECT_NAME
    apps_enabled = "/etc/uwsgi/apps-enabled/%s.ini" % configuration.PROJECT_NAME

    append(apps_available, configuration.uwsgi_conf, use_sudo=True)

    run('sudo ln -s %s %s' % (apps_available, apps_enabled))


@task
def create_wsgi_file():
    
    if not exists(configuration.WSGI_FILE, use_sudo=True):
        append(configuration.WSGI_FILE, configuration.wsgipy, use_sudo=True)

@task
def create_pip_requirements():

    append(configuration.REQUIREMENTS_FILE, configuration.pip_requirements, use_sudo=True)

@task
def restart_nginx_uwsgi():
    
    
    run('sudo service nginx restart')
    run('sudo service uwsgi restart')

@task
def restart_supervisor():
    
    run('sudo service supervisor restart')

@task
def setup_postgres():
    with settings():
        postgres.server()
        postgres.create_user(configuration.DB_USER_NAME, password=configuration.DB_PASSWORD)
    postgres.create_database(configuration.DB_NAME, owner=configuration.DB_USER_NAME)
   
@task
def create_supervisor_celery_conf():
    append('/etc/supervisor/conf.d/celery.conf', configuration.supervisor_celery_conf, use_sudo=True)
    run('touch /home/%s/celerybeat-schedule.db' % configuration.NEW_OPERATING_SYSTEM_USER)
    restart_supervisor()
                    
@task
def create_new_os_user():
    
    user.create(configuration.NEW_OPERATING_SYSTEM_USER, create_home=True, password=configuration.NEW_OPERATING_SYSTEM_USER_PASSWORD)    

@task
def syncdb_collectstatic():
    with cd(configuration.PROJECT_PATH):
        with virtualenv(configuration.VIRTUALENV_PATH):
            run('python manage.py syncdb')
            run('python manage.py collectstatic')

@task
def build():
    run('sudo apt-get update')
    create_new_os_user()
    env.user = configuration.NEW_OPERATING_SYSTEM_USER    
    install_os_packages(configuration.SYSTEM_PACKAGES_NEEDED)    
    create_project_path()
    create_backup_path()
    clone_git_repo()
    create_pip_requirements()
    create_virtualenv(configuration.VIRTUALENV_PATH)
    install_virtualenv_requirements()
    setup_postgres()
    create_nginx_conf()
    create_uwsgi_conf()
    create_wsgi_file()
    syncdb_collectstatic()            
    create_supervisor_celery_conf()    
    restart_nginx_uwsgi()
    restart_supervisor()
    
@task    
def update_from_git_and_migratedb():
    
    git_pull()
    
    with cd(configuration.PROJECT_PATH):
        with virtualenv(configuration.VIRTUALENV_PATH):
            run('python manage.py makemigrations web')
            run('python manage.py migrate')
            run('python manage.py syncdb')
            
    restart_nginx_uwsgi()
    restart_supervisor()

@task    
def update_from_git():
    
    git_pull()
    restart_nginx_uwsgi()
    restart_supervisor()   
