from flask import Flask

app = Flask(__name__)

from server import routes

from server.main.routes import page as main
from server.course.routes import page as course
from server.about.routes import page as about
from server.status.routes import page as status

app.register_blueprint(main)
app.register_blueprint(course, url_prefix='/course')
app.register_blueprint(about, url_prefix='/about')
app.register_blueprint(status, url_prefix='/status')
