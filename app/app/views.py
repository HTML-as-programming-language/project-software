from flask import render_template
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_appbuilder import BaseView

from app import appbuilder, db
from .models import *


@appbuilder.app.errorhandler(404)
def page_not_found(e):
    """ Application wide 404 error handler """
    return render_template('404.html', base_template=appbuilder.base_template, appbuilder=appbuilder), 404


db.create_all()

    # >>> import requests
    # >>> r = requests.post("http://bugs.python.org", data={'number': 12524, 'type': 'issue', 'action': 'show'})
    # >>> print(r.status_code, r.reason)
    # 200 OK
    # >>> print(r.text[:300] + '...')