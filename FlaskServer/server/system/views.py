from flask import render_template

from server import app

# 404 Error handler page
@app.errorhandler(404)
def error_notfound(e):
    return render_template('404.html'), 404
