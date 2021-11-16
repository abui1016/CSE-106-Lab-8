from flask import Flask, render_template, url_for, request

app = Flask(__name__)

@app.route("/")
def loginView(): 
    return render_template("login.html")

@app.route("/student", methods=['POST'])
def studentView():
    return render_template("student.html")

@app.route("/teacher", methods=['POST'])
def teacherView():
    return render_template("teacher.html")

@app.route("/teacher/roster")
def rosterView():
    return render_template("roster.html")