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

**Step 5:  CD into the repo you just cloned.  Build and deploy.**
```shell
fab build
```

When you run ```fab build``` it calls the build() function in fabfile.py which in turn calls a number of other functions to install system packages, creates a user, installs virtualenv, etc.


