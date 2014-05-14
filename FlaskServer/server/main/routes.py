from flask import Blueprint
from server.main import views

# Blueprint
page = Blueprint('main', __name__, template_folder='../templates/main/')

# Requests for main index
@page.route('/', methods=['GET'])
def index():
    return views.index()
