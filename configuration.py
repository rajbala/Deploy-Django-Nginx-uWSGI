SYSTEM_PACKAGES_NEEDED = 'git vim uwsgi-plugin-python python-pip supervisor redis-server python-dev libxml2-dev libxslt-dev libpq-dev nginx uwsgi postgresql-client postgresql postgresql-contrib nginx uwsgi'


# Required
HOSTS = ["IP_ADDRESS_OF_DEPLOYMENT_TARGET"]
INITIAL_OPERATING_SYSTEM_USER = 'root'
#

# Optional
# If you're using SSH keys to access servers remotely  Example:

# You should change these when you're building for production, but it's fine to leave them to test the deployment script on a new server
# For production and actual Django app the project_name and app_name must match the actual
NEW_OPERATING_SYSTEM_USER = "django"
NEW_OPERATING_SYSTEM_USER_PASSWORD = "setarealpassword"
PROJECT_NAME = "project_name"
APP_NAME = "app_name"

GIT_USER_NAME = "git_user"
GIT_PASSWORD = "git_password"
GIT_EMAIL = "git_email"
GIT_USER = "git user"

# Ex. https://user:password@github.com/username/repo.git
#GIT_REPO_URL = "https://%s:%s@github.com/username/repo.git" % (GIT_USER_NAME, GIT_PASSWORD)
GIT_REPO_URL = "https://github.com/rajbala/django-project.git"

REQUIREMENTS_FILE = "/tmp/requirements.txt"
DB_NAME = "database_name"
DB_USER_NAME = "postgres_user"
DB_PASSWORD = "postgres_user_password"
APPS_ROOT = "/var/www/apps/"
PROJECT_PATH = "%s%s" % (APPS_ROOT, PROJECT_NAME)
DOMAIN_NAME = "domain_name"
VIRTUALENV_PATH = "/var/www/virtualenv/%s" % DOMAIN_NAME
STATIC_FILES_PATH = "/home/%s/apps/static/" % NEW_OPERATING_SYSTEM_USER
BACKUP_PATH = "/home/%s/backups/" % NEW_OPERATING_SYSTEM_USER
WSGI_FILE = "%s/%s/wsgi.py" % (PROJECT_PATH, APP_NAME)
VISUDO_PATH = "/tmp/visudo.sh"

pip_requirements = '''
django
celery
django-celery
South
redis
psycopg2 '''

visudo = '''
#!/bin/sh
if [ -z "$1" ]; then
  echo "Starting up visudo with this script as first parameter"
  export EDITOR=$0 && sudo -E visudo
else
  echo "Changing sudoers"
  echo "%s ALL=(ALL:ALL) ALL" >> $1
fi ''' % (NEW_OPERATING_SYSTEM_USER)

nginx_conf = '''
# the upstream component nginx needs to connect to
upstream django {
    server unix:/tmp/%s.sock;
}

# configuration of the server
server {
    listen      80;
    server_name %s;
    charset     utf-8;

    # max upload size
    client_max_body_size 75M;   # adjust to taste

    # Django media
    location /media  {
        alias /var/www/apps/%s/%s/media;  # your Django project's media files - amend as required
    }

    location /static {
        alias /home/%s/apps/static; # your Django project's static files - amend as required
    }

    # Finally, send all non-media requests to the Django server.
    location / {
        uwsgi_pass  django;
        include uwsgi_params;
        uwsgi_param UWSGI_SCHEME $scheme;
        uwsgi_param UWSGI_PYHOME %s;
        uwsgi_param UWSGI_CHDIR %s;
        uwsgi_param UWSGI_MODULE app;
        uwsgi_param UWSGI_CALLABLE app;
        error_page 404 /404.html;
        }
}''' % (DOMAIN_NAME, PROJECT_NAME, PROJECT_NAME, APP_NAME, NEW_OPERATING_SYSTEM_USER, VIRTUALENV_PATH, PROJECT_PATH)


uwsgi_conf = '''
[uwsgi]
chdir           = %s
module          = %s.wsgi:application
home            = %s
master          = True
processes       = 4
socket          = /tmp/%s.sock
daemonize       = /var/log/uwsgi/%s.log
plugins         = python
env             = DJANGO_CONFIGURATION=Prod
uid             = 33
gid             = 33''' % (PROJECT_PATH, APP_NAME, VIRTUALENV_PATH, DOMAIN_NAME, PROJECT_NAME)


wsgipy = '''
import os
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "%s.settings")

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application() ''' % (PROJECT_NAME)


supervisor_celery_conf = '''
[program:celeryd]
command=%s/bin/celery -A %s.celery worker -B --schedule /home/%s/celerybeat-schedule.db --loglevel=info
directory=%s
environment=PATH="%s"
stdout_logfile=/var/log/celeryd.log
stderr_logfile=/var/log/celeryd.log
autostart=true
autorestart=true
user=%s
startsecs=10
stopwaitsecs=600 ''' % (VIRTUALENV_PATH, APP_NAME, NEW_OPERATING_SYSTEM_USER, PROJECT_PATH, PROJECT_PATH, NEW_OPERATING_SYSTEM_USER)
