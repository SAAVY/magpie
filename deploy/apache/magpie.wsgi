#!/usr/bin/python
import sys
import logging
from client.api import app as application
logging.basicConfig(stream=sys.stderr)
sys.path.insert(0, "/var/www/magpie/")


activate_this = '/var/www/magpie/venv/bin/activate_this.py'
execfile(activate_this, dict(__file__=activate_this))
application.secret_key = 'Add your secret key'
