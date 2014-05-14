from flask import render_template, url_for

def index():
    """ Function to render the testserver status index page """
    return render_template('status/index.html')
