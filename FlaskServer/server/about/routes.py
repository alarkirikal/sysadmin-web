from flask import Blueprint, redirect, url_for
from server.about import views

# Blueprint for /about
page = Blueprint('about', __name__, template_folder='../templates/about/')

@page.route('/', methods=['GET'])
def index():
    return views.index()
