from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secrettunnel'
db = SQLAlchemy(app)

# Following Schema from Lab 8.pdf
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    role = db.Column(db.String(100))
    username = db.Column(db.String(100))
    password = db.Column(db.String(100))

# After user presses login button:
    # if role = student -> render_template(student)
    # if role = teacher -> render_template(teacher)

class Classes(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String(100))
    teacher = db.Column(db.String)
    time = db.Column(db.String(100))
    num_enrolled = db.Column(db.Integer)
    capacity = db.Column(db.Integer)

class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    class_id = db.Column(db.Integer, db.ForeignKey('classes.id')) 
    student_id = db.Column(db.Integer, db.ForeignKey('users.id')) 
    grade = db.Column(db.Integer)

db.create_all()

# Inserting into db
# ahep = Users(name="Ammon Hepworth", role="Teacher", username="ahepworth", password="123123")
# swalk = Users(name="Susan Walker", role="Teacher", username="swalker", password="123123")
# rjenk = Users(name="Ralph Jenkins", role="Teacher", username="rjenkins", password="123123")

# jsant = Users(name="Jose Santos", role="Student", username="jsantos", password="123123")
# bbrow = Users(name="Betty Brown", role="Student", username="bbrown", password="123123")
# jstu = Users(name="John Stuart", role="Student", username="jstuart", password="123123")
# lich = Users(name="Li Cheng", role="Student", username="lcheng", password="123123")
# nlit = Users(name="Nancy Little", role="Student", username="nlittle", password="123123")
# mnor = Users(name="Mindy Norris", role="Student", username="mnorris", password="123123")
# aran = Users(name="Aditya Ranganath", role="Student", username="aranganath", password="123123")
# yiwe = Users(name="Yi Wen Chen", role="Student", username="ychen", password="123123")

# math101 = Classes(course_name="Math 101", teacher="Ralph Jenkins", time="MWF 10:00-10:50 AM", num_enrolled=4, capacity=8)
# phys121 = Classes(course_name="Physics 121", teacher="Susan Walker", time="TR 11:00-11:50 AM", num_enrolled=4, capacity=10)
# cs106 = Classes(course_name="CS 106", teacher="Ammon Hepworth", time="MWF 2:00-2:50 PM", num_enrolled=4, capacity=10)
# cs162 = Classes(course_name="CS 162", teacher="Ammon Hepworth", time="TR 3:00-3:50 PM", num_enrolled=4, capacity=4)

# db.session.add(ahep)
# db.session.add(swalk)
# db.session.add(rjenk)

# db.session.add(jsant)
# db.session.add(bbrow)
# db.session.add(jstu)
# db.session.add(lich)
# db.session.add(nlit)
# db.session.add(mnor)
# db.session.add(aran)
# db.session.add(yiwe)

# db.session.add(math101)
# db.session.add(phys121)
# db.session.add(cs106)
# db.session.add(cs162)
# db.session.commit()



@app.route("/", methods=['POST', 'GET'])
def loginView(): 
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        found_user = Users.query.filter_by(username=username, password=password).first()
        if found_user.role == 'Teacher':
            return redirect(url_for('teacherView', name=found_user.name))
        if found_user.role == 'Student':
            return redirect(url_for('studentView', name=found_user.name))
    return render_template('login.html')
    

@app.route("/student/<string:name>", methods=['POST', 'GET'])
def studentView(name):
    if request.method == 'POST':
        return render_template("student.html", name=name)
    return render_template("student.html", name=name)

@app.route("/teacher/<string:name>", methods=['POST', 'GET'])
def teacherView(name):
    if request.method == 'POST':
        return render_template("teacher.html", name=name)
    return render_template("teacher.html", name=name)

@app.route("/teacher/roster")
def rosterView():
    return render_template("roster.html")

if __name__ == "__main__":
    app.run()