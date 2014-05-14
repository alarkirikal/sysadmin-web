from flask import Blueprint, redirect, url_for
from server.main import views

page = Blueprint('main', __name__, template_folder='../templates/main/')

@page.route('/', methods=['GET'])
def index():
    return views.index()

@page.route('/second', methods=['GET'])
def second():
    return views.second()
