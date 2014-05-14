from flask import render_template, request, url_for

def index():
    return render_template('main/index.html')


def second():
    return render_template('main/second.html')
