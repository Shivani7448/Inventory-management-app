from flask import Flask, render_template,redirect,request
from flask import current_app as app
from .models import *

# @app.route
# 1. from models import * >will look for this file in root directory
# 2. from .models import * >will look for this file in current directory(application folder)
# 3. from application.models import * > controllers.py will think that there is one more application folder in the root directory(application folder) with respect to controllers.py
