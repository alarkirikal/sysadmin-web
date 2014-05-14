from flask import Blueprint, redirect, url_for

from server.status import views

# Blueprint
page = Blueprint('status', __name__, template_folder='../templates/status/')

# Requests for the testserver status index page
@page.route('/', methods=['GET'])
def index():
    return views.index()
