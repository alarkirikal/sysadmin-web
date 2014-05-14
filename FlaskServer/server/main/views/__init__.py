from flask import render_template, request, url_for


def index():
    """ Function to render template for the main index page """
    return render_template('main/index.html')
