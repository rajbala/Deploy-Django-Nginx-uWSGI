# Deploy Django with Nginx, uWSGI, Celery, and Supervisor

This is Fabric script to automatically deploy a Django app with uWSGI and Nginx. It also installs Supervisor and Celery, but feel free to comment those portions out if you're not using them.  

I wrote this on Ubuntu 14.04, but *should* work on Red Hat and its variants with minimal changes.  

**Step 1:  Install Fabric on your local machine**
```shell
pip install fabric
```

**Step 2:  Install Fabtools on your local machine**
```shell
pip install fabtools
```

**Step 3:  Clone this git repo**
```shell
git clone https://github.com/rajbala/Deploy-Django-Nginx-uWSGI.git
```

**Step 4:  SSH into your server and run this script.  It adds a user called django to sudoers**
https://github.com/rajbala/Deploy-Django-Nginx-uWSGI/blob/master/visudo.sh

**Step 6:  Setup a few paramters in configuration.py with the location of your server, etc.**
Minimally, you'll need to set the HOSTS constant with location of your deployment target which could be your local machine.  You can use your own Django app, but you may need to change the paths if you already have a WSGI file, etc.  

**Step 5:  CD into the directory of the repo you just cloned where fabfile.py is located.  Build and deploy.**
```shell
fab build
```
The script assumes that you're logging in as the root user intially to get started, but certainly change that if your user is some other user with root privileges.

You'll be prompted a few times for the password of the newly created operating system user. The default password, which is set in configuration.py, is setarealpassword.  As the password implies you should really consider setting a real password.  

When you run ```fab build``` it calls the build() function in fabfile.py which in turn calls a number of other functions to install system packages, creates a user, installs virtualenv, etc.

The majority of your changes should be in configuration.py unless you're deploying on something other than Ubuntu/Debian or perhaps you don't want to install and configure a specific component such as Celery or Supervisor.

