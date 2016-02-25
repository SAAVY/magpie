import os
from fabric.api import sudo, cd, put, env, settings


def prod():
    env.hosts = os.environ['SERVER_HOST']
    env.user = os.environ['SERVER_USER']
    if os.environ.get('SERVER_PEM'):
        env.key_filename = os.environ['SERVER_PEM']
    if os.environ.get('SERVER_PASSWORD'):
        env.password = os.environ['SERVER_PASSWORD']


def setup_apache():
    sudo('apt-get install libapache2-mod-wsgi')
    sudo('a2enmod wsgi')
    put('deploy/apache/magpie_api.conf', '/etc/apache2/sites-available/magpie_api.conf', use_sudo=True)
    sudo('a2ensite magpie_api.conf')
    sudo('service apache2 reload')
    with settings(warn_only=True):
        sudo('git clone https://github.com/SAAVY/magpie.git /var/www/magpie')
    with cd('/var/www/magpie'):
        sudo('git pull')
        sudo('virtualenv -p /usr/bin/python2.7 venv')


def deploy_apache():
    # and finally touch the .wsgi file so that mod_wsgi triggers
    # a reload of the application
    sudo('cp /var/www/magpie/deploy/apache/magpie.wsgi /var/www/magpie/magpie.wsgi')
    sudo('touch /var/www/magpie/magpie.wsgi')
    sudo('service apache2 reload')


def setup_nginx():
    sudo('apt-get install nginx')
    sudo('sudo /etc/init.d/nginx start')
    put('deploy/nginx/magpie_api.conf', '/etc/nginx/sites-available/magpie_api.conf', use_sudo=True)
    with settings(warn_only=True):
        sudo('cp /etc/nginx/sites-available/magpie_api.conf /etc/nginx/sites-enabled/magpie_api.conf')
        sudo('git clone https://github.com/SAAVY/magpie.git /var/www/magpie')
    with cd('/var/www/magpie'):
        sudo('git pull')
        sudo('virtualenv -p /usr/bin/python2.7 venv')
    sudo('cp /etc/nginx/sites-available/magpie_api.conf /etc/nginx/sites-enabled/magpie_api.conf')


def deploy_nginx():
    with cd('/var/www/magpie'):
        sudo('. venv/bin/activate')
        sudo('gunicorn -w 4 -b 127.0.0.1:8000 \'client.api:start("logs",False)\'')
