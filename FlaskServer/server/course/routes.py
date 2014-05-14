from flask import Blueprint, redirect, url_for

from server.course import views

page = Blueprint('course', __name__, template_folder='../templates/course/')

@page.route('/overview', methods=['GET', 'POST'])
@page.route('/overview/<course_time>', methods=['GET', 'POST'])
def students(course_time = ""):
    return views.students(course_time)

@page.route('/initcourse', methods=['GET', 'POST'])
def init_course():
    return views.init_course()

@page.route('/initcourse_ajax', methods=['POST'])
def init_course_ajax():
    return views.init_course_ajax()

@page.route('/initcourse_final', methods=['POST'])
def init_course_final():
    return views.init_course_final()

@page.route('/certsign', methods=['GET', 'POST'])
@page.route('/certsign/<course_time>', methods=['GET', 'POST'])
def cert_sign(course_time = ""):
    return views.cert_sign(course_time)
