
import os
import time
import random
from contextlib import contextmanager

from fabric.context_managers import prefix, settings
from fabric.api import cd, env, run, task

env.user = 'ubuntu'
env.hosts = ['177.71.186.49']

WORKON = 'source /usr/local/bin/virtualenvwrapper.sh; workon pegapega'

@task
def deploy():
    with prefix(WORKON), cd('src/pegapega/'):
        # Get newest code
        run('git checkout -f')
        run('git pull origin master -v')

        # Clean pyc files
        run('find . -iname "*.pyc" -exec rm {} \;')

        # Run DB routines
        run('./manage.py syncdb --noinput')
        run('./manage.py migrate --noinput')

    with settings(user='root'):
        pass
        # Restart gunicorn process using supervisor
        #run('supervisorctl restart pegapega')
