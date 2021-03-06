from flask import render_template, url_for, request, redirect
from werkzeug import secure_filename
from datetime import date

from server.system.db import Postgres

import helpers
import os
import csv
import json


## Local helper methods ##

def get_future_courses():
    """ This function looks, which courses aren't inited yet in this and next year.

    Returns:
        tuple. Available course times

    """

    # Init db
    db = Postgres()
    db.connect()
    
    # SQL
    sql = """
        SELECT DISTINCT
            course_time
        FROM
            Students;
    """
    
    data = db.execute(sql)
    current_courses = []
    for element in data:
        current_courses.append(element[0])
    
    # Get current year
    years_to_show = (date.today().year, date.today().year + 1)
    
    courses = []
    for year in years_to_show:
        courses.append(str(year) + "_spr")
        courses.append(str(year) + "_aut")
    
    # Get the unique list of courses
    unique_courses = list(set(courses) - set(current_courses))
    retval = []
    for element in unique_courses:
        retval.append({"name" : element.replace("_", " ") \
                      .replace("spr", "Spring") \
                      .replace("aut", "Autumn"),
                      "val"  : element})
    
    return tuple(retval)

def generate_uid(study_nr, course_time):
    """ This function generates an uid for a student

    Args:
        study_nr (str): Study number of the student
        course_time (str): Time of the course the student is registered to

    Returns:
        str. The generated uid
        
    """

    splitter = "_"
    if " " in course_time:
        splitter = " "
    
    course_year = course_time.split(splitter)[0]
    course_time = course_time.split(splitter)[1].replace("Spring", "spr").replace("Autumn", "aut")
    return study_nr + "_" + course_year[2:] + course_time

def update_data_if_changed(current_student, student_id, db, course_time):
    """ This function updates the data in the database in case it is different from the original
        .csv file the students data was taken from

    Args:
        current_student (list): the data of the studend loaded in the new .csv
        student_id (str): the ID of the student
        db (Postgres): database connection object
        course_time (str): time of the course the student is registered to

    """
    
    # Get student with the given id and during that course time
    data = db.execute("""
        SELECT
            id, study_nr, name, lastname, faculty, year, study_degree, study_curriculum, group_nr, email_ut, email_ext
        FROM
            Students
        WHERE
            study_nr LIKE %s
        AND
            course_time LIKE %s
        """, (student_id, course_time))[0]
    
    
    if tuple(current_student) != tuple(data):
        # Values differ - overwrite the database values
        db.execute("""
            UPDATE
                Students
            SET
                id = %s
                ,study_nr = %s
                ,name = %s
                ,lastname = %s
                ,faculty = %s
                ,year = %s
                ,study_degree = %s
                ,study_curriculum = %s
                ,group_nr = %s
                ,email_ut = %s
                ,email_ext = %s
            WHERE
                study_nr LIKE %s
            AND
                course_time LIKE %s
            """, tuple(current_student + [student_id, course_time]))

def check_and_deactivate_nonexistent(student_ids, db, course_time):
    """ This function sets the students inactive, who are not found in the new .csv file

    Args:
        student_ids (list): list of student ids in the new .csv file
        db (Postgres): database connection object
        course_time (str): time of the course the students are registered to

    """


    # Get student IDs from DB
    db_ids_temp = db.execute("""
        SELECT
            study_nr
        FROM
            Students
        WHERE
            course_time LIKE %s
        """, (course_time,))
    
    db_ids = []
    for element in db_ids_temp:
        db_ids.append(element[0])
    
    if student_ids == db_ids:
        pass
    elif len(student_ids) < len(db_ids):
        # Less ID's in the .csv than in db - deactivate
        ids_to_deactivate = list(set(db_ids) - set(student_ids))
        
        for id in ids_to_deactivate:
            # Deactivate this ID
            db.execute("""
                UPDATE
                    Students
                SET
                    course_status = 'deactive'
                WHERE
                    study_nr LIKE %s
                AND
                    course_time LIKE %s
                """, (id, course_time))


def get_students(course_time):
    """ This function gets all the students for the given course time

    Args:
        course_time (str): the course time of the students to return

    Returns:
        tuple. All the students who are registered in that course

    """
    
    # Open database for query
    db = Postgres()
    db.connect()
    
    # SQL Query
    sql = """
        SELECT
            course_status, id, name, lastname, group_nr, study_curriculum, email_ut, email_ext
        FROM
            Students
        """
    
    # Check if course time is valid
    if course_time and \
        helpers.is_valid_year(course_time.split("_")[0]):
        sql += " WHERE course_time LIKE '" + course_time + "'"
    
    # Get data
    data = db.execute(sql)
    students = []
    for row in data:
        student = {"status" : row[0]
            ,"sid" : row[1]
            ,"name" : row[2].decode('utf8')
            ,"lastname" : row[3].decode('utf8')
            ,"group" : row[4].decode('utf8')
            ,"curriculum" : row[5]
            ,"utemail" : row[6]
            ,"extemail" : row[7]}
        
        students.append(student)
    
    return tuple(students)


def get_courses():
    """ Function to get all the current courses
    
    Returns:
        tuple. course times, that exist in the database

    """

    # Init db
    db = Postgres()
    db.connect()
    
    # SQL
    sql = """
        SELECT DISTINCT
            course_time
        FROM
            Students
        """
    
    # Generate tuple of dictionaries
    times_temp = db.execute(sql)
    times = []
    for element in times_temp:
        time = element[0]
        times.append({ "name"   : time.replace("_", " ") \
                     .replace("spr", "Spring") \
                     .replace("aut", "Autumn"),
                     "val"    : time})
    
    return tuple(times)


def get_latest_course():
    """ Function to get the latest current course
    
    Returns:
        str. Latest current course
        None. In case no courses are inited
    """

    # Init DB
    db = Postgres()
    db.connect()
    
    # SQL
    sql = """
        SELECT DISTINCT
            course_time
        FROM
            Students
        """
    
    data = db.execute(sql)
    
    # Compare to 1970_spr
    latest_course = "1970_spr"
    for time in data:
        current_course = time[0].split("_")
        if int(current_course[0]) > int(latest_course.split("_")[0]):
            latest_course = "_".join(current_course)
        elif int(current_course[0]) == int(latest_course.split("_")[0]):
            if "aut" in current_course:
                latest_course = "_".join(current_course)
    
    # Return None if the str has not been updated
    if latest_course == "1970_spr":
        return None
    
    return latest_course



## GET/POST methods for ../views.py ##

def cert_sign(course_time = ""):
    """ Function to get data and send it to jinja2 via render_template """

    if request.method == "GET":
        # Check for necessity of redirection before going for any data
        if course_time == "":
            latest_course = get_latest_course()
            if latest_course == None:
                return render_template("course/cert_sign.html", students=[], menu_items=[])
            return redirect(url_for("course.cert_sign") + "/" + latest_course)
        
        # Continue in case no redirection needed
        
        # Get student data from DB
        db = Postgres()
        db.connect()
        
        sql = """
            SELECT
                name, lastname, username, student_uid, status_mail, status_smime, status_csr, status_certsent
            FROM
                Students
            WHERE
                course_time LIKE %s
            """
        
        rows = db.execute(sql, (course_time,))

        # Generate tuple of student dictionaries
        students = []
        for row in rows:
            student = {
                "name"          : row[0].decode('utf8'),
                "lastname"      : row[1].decode('utf8'),
                "login"         : row[2].decode('utf8'),
                "uid"           : row[3].decode('utf8'),
                "mail_status"   : row[4],
                "smime_status"  : row[5],
                "csr_status"    : row[6],
                "certsent_status": row[7]
            }
            students.append(student)
        
        return render_template('course/cert_sign.html', students=students, menu_items=get_courses())


def init_course():
    """ Function to get data and send it to jinja2 via render_template """
    if request.method == "GET":
        return render_template('course/init_course.html', courses=get_future_courses())


def students(course_time = ""):
    """ Function to get data and send it to jinja2 via render_template """
    if request.method == "GET":
        if course_time == "":
            if get_latest_course() == None:
                # If there are no courses inited
                return render_template('course/students.html', students=[], menu_items=get_courses())
            # If there are courses, but the request was made for none of them
            return redirect(url_for('course.students') + "/" + get_latest_course())
        # Normal GET request
        return render_template('course/students.html', students=get_students(course_time), menu_items=get_courses())
    else:
        message = None
        
        # POST - Uploaded CSV file to update students
        file = request.files['ois_file']
        if file:
            if helpers.allowed_file(file.filename):
                
                # Open file and read csv
                if not file.closed:
                    csvreader = csv.reader(file, delimiter=',')
                    rows = []
                    student_ids = []
                    for row in csvreader:
                        current_row = []
                        
                        # First column from OIS file
                        for element in row[0].split(";"):
                            current_row.append(element)
                        
                        # Second column from OIS file
                        current_row.append(row[1])
                        
                        # Third column from OIS file
                        for element in row[2].split(";"):
                            current_row.append(element)
                        
                        # Student id
                        student_ids.append(row[0].split(";")[1])
                        
                        rows.append(current_row)
                    
                    db = Postgres()
                    db.connect()
                    
                    # Look for the student ID's in the db
                    counter = 0
                    for student_id in student_ids:
                        count = db.execute("""
                            SELECT
                            count(study_nr)
                            FROM
                            Students
                            WHERE
                            study_nr LIKE %s
                            AND
                            course_time LIKE %s
                            """, (student_id,course_time))
                        
                        count_nr = count[0][0]
                        current_student = rows[counter]
                        
                        counter += 1
                        
                        if count_nr == 0:
                            # No such ID in the db - add it to db
                            db.execute("""
                                INSERT INTO
                                    Students
                                VALUES
                                    (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 'NOK', 'NOK', 'NOK', 'NOK');
                                """, tuple(current_student + ["active", course_time, generate_uid(current_student[1], course_time)]))
                        elif count_nr == 1:
                            # Such ID already in db
                            update_data_if_changed(current_student, student_id, db, course_time)
                    
                    # Check for students to set as inactive 
                    check_and_deactivate_nonexistent(student_ids, db, course_time)
            
            else:
                message = "File upload unsuccessful - wrong format"
        else:
            message = "File upload unsuccessful"
        
        return render_template('course/students.html', students=get_students(course_time), message=message, menu_items=get_courses())



## AJAX Methods ##


def init_course_final():
    """ Ajax function to upload a new .csv file to the database """

    if request.method == "POST":
        response = {}
        
        # File checks for the form file
        file = request.files['ois_file']
        if file and helpers.allowed_file(file.filename):
                
            if not file.closed:
                csvreader = csv.reader(file, delimiter=',')
                rows = []
                for row in csvreader:
                    current_row = []
                        
                    # First column from OIS file
                    for element in row[0].split(";"):
                        current_row.append(element.decode('utf8'))
                        
                    # Second column from OIS file
                    current_row.append(row[1][1:])
                        
                    # Third column from OIS file
                    for element in row[2].split(";"):
                        current_row.append(element.decode('utf8'))
                        
                    rows.append(current_row)
                    
                db = Postgres()
                db.connect()
                    
                for current_student in rows:
                        
                    #Generate course time
                    course_time = request.form['course_time'] \
                                    .replace(" ", "_") \
                                    .replace("Spring", "spr") \
                                    .replace("Autumn", "aut")
                        
                    # Generate username
                    username = (current_student[2][:1] + current_student[3]).lower()
                        
                    # TODO: Check if username is unique
                        
                    # Generate tuple
                    tuple_to_add = tuple(current_student + [
                        "active",           # course_status
                        course_time,        # course_time
                        generate_uid(current_student[1], request.form['course_time']), # student_uid
                        "NOK",              # status_mail
                        "NOK",              # status_smime
                        "NOK",              # status_csr
                        "NOK",              # status_certsent
                        username])
                    
                    db.execute("""
                        INSERT INTO
                            Students
                        VALUES
                            (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                    """, tuple_to_add)
                
                response['status'] = 'success'
                return json.dumps(response)
            else:
                response['error_msg'] = "Wrong file format"
        
        else:
            response['error_msg'] = "File not found"
        response['status'] = 'failure'
        return json.dumps(response)


def init_course_ajax():
    """ Function to check the .csv file if it can be opened """
    
    if request.method == "POST":
        # Init response
        response = {}
        
        # Check for correctness of file
        if len(request.files) == 1:
            file = request.files['ois_file']
            if file and helpers.allowed_file(file.filename):
                response['status'] = "success"
                
                # Get nr of students in file
                response['filename'] = file.filename
                response['students_count'] = len(file.readlines())
            else:
                response['status'] = "failure"
                response['error_msg'] = "Bad file format"
        else:
            response['status'] = "failure"
            response['error_msg'] = "Missing file"
        
        # Return response dict
        return json.dumps(response)

