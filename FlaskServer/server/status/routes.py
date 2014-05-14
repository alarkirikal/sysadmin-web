from flask import Blueprint, redirect, url_for

from server.status import views

page = Blueprint('status', __name__, template_folder='../templates/status/')

@page.route('/', methods=['GET'])
def index():
    return views.index()
