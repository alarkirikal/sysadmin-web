from flask import Blueprint, redirect, url_for

from server.course import views


# Blueprint
page = Blueprint('course', __name__, template_folder='../templates/course/')

# Requests for students page
@page.route('/overview', methods=['GET', 'POST'])
@page.route('/overview/<course_time>', methods=['GET', 'POST'])
def students(course_time = ""):
    return views.students(course_time)

# Requests for initializing course
@page.route('/initcourse', methods=['GET', 'POST'])
def init_course():
    return views.init_course()

# Requests for ajax file upload check
@page.route('/initcourse_ajax', methods=['POST'])
def init_course_ajax():
    return views.init_course_ajax()

# Requests for ajax file upload + database save
@page.route('/initcourse_final', methods=['POST'])
def init_course_final():
    return views.init_course_final()

# Requests for certsign page
@page.route('/certsign', methods=['GET', 'POST'])
@page.route('/certsign/<course_time>', methods=['GET', 'POST'])
def cert_sign(course_time = ""):
    return views.cert_sign(course_time)
