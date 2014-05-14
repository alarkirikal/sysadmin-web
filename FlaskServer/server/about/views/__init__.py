from flask import render_template

# Index page for About Page
def index():
    return render_template('about/index.html')
