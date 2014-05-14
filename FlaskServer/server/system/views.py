from flask import render_template

from server import app

@app.errorhandler(404)
def error_notfound(e):
    return render_template('404.html'), 404
