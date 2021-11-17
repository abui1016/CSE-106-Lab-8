from flask import Flask, render_template, url_for, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_admin import Admin 
from flask_admin.contrib.sqla import ModelView

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.sqlite3'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'secrettunnel'
db = SQLAlchemy(app)
admin = Admin(app)

# Following Schema from Lab 8.pdf
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    password = db.Column(db.String)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))


class Teacher(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    user = db.relationship('User', backref='teacher', uselist=False)


class Student(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    user = db.relationship('User', backref='student', uselist=False)
    courses = db.relationship('Enrollment', back_populates='student')


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    course_name = db.Column(db.String)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teacher.id'))
    num_enrolled = db.Column(db.Integer)
    capacity = db.Column(db.Integer)
    time = db.Column(db.String)
    teacher = db.relationship('Teacher', backref=db.backref('teachers', lazy=True))
    students = db.relationship('Enrollment', back_populates='course')


class Enrollment(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('student.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    grade = db.Column(db.Integer)
    student = db.relationship('Student', back_populates='courses')
    course = db.relationship('Course', back_populates='students')

db.create_all()

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Teacher, db.session))
admin.add_view(ModelView(Student, db.session))
admin.add_view(ModelView(Course, db.session))
admin.add_view(ModelView(Enrollment, db.session))


@app.route("/", methods=['POST', 'GET'])
def loginView(): 
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        found_user = User.query.filter_by(username=username, password=password).first()
        if found_user.student_id == 0:
            return redirect(url_for('teacherView', name="Ammon Hepworth"))
        if found_user.teacher_id == 0:
            return redirect(url_for('studentView', name="Jose Santos"))
    return render_template('login.html')
    

@app.route("/student/<string:name>", methods=['POST', 'GET'])
def studentView(name):
    if request.method == 'POST':
        return render_template("student.html", name=name)
    return render_template("student.html")

@app.route("/teacher/<string:name>", methods=['POST', 'GET'])
def teacherView(name):
    if request.method == 'POST':
        return render_template("teacher.html", name=name)
    return render_template("teacher.html")

@app.route("/teacher/roster", methods=['POST'])
def rosterView(name):
    if request.method == 'POST':
        return render_template("roster.html")
    return render_template("roster.html")

if __name__ == "__main__":
    app.run()













# jsantE = Enrollment(student_id=1, course_id=1, grade=90)
# bbrowE = Enrollment(student_id=2, course_id=1, grade=90)
# bbrowE2 = Enrollment(student_id=2, course_id=2, grade=90)
# jstuE = Enrollment(student_id=3, course_id=1, grade=90)
# jstuE2 = Enrollment(student_id=3, course_id=2, grade=90)
# jstuE3 = Enrollment(student_id=3, course_id=4, grade=90)
# lichE = Enrollment(student_id=4, course_id=1, grade=90)
# lichE2 = Enrollment(student_id=4, course_id=2, grade=90)
# nlitE = Enrollment(student_id=5, course_id=2, grade=90)
# nlitE2 = Enrollment(student_id=5, course_id=3, grade=90)
# nlitE3 = Enrollment(student_id=5, course_id=4, grade=90)
# mnorE = Enrollment(student_id=6, course_id=2, grade=90)
# mnorE2 = Enrollment(student_id=6, course_id=3, grade=90)
# aranE = Enrollment(student_id=7, course_id=3, grade=90)
# aranE2 = Enrollment(student_id=7, course_id=4, grade=90)
# yiweE = Enrollment(student_id=8, course_id=3, grade=90)
# yiweE2 = Enrollment(student_id=8, course_id=4, grade=90)

# db.session.add(jsantE)
# db.session.add(bbrowE)
# db.session.add(bbrowE2)
# db.session.add(jstuE)
# db.session.add(jstuE2)
# db.session.add(jstuE3)
# db.session.add(lichE)
# db.session.add(lichE2)
# db.session.add(nlitE)
# db.session.add(nlitE2)
# db.session.add(nlitE3)
# db.session.add(mnorE)
# db.session.add(mnorE2)
# db.session.add(aranE)
# db.session.add(aranE2)
# db.session.add(yiweE)
# db.session.add(yiweE2)

# ahep = User(username="ahepworth", password="123123", student_id=0, teacher_id=1)
# swal = User(username="swalker", password="123123", student_id=0, teacher_id=2)
# rjen = User(username="rjenkins", password="123123", student_id=0, teacher_id=3)

# db.session.add(ahep)
# db.session.add(swal)
# db.session.add(rjen)
# db.session.commit()

# ahepT = Teacher(name="Ammon Hepworth")
# swalT = Teacher(name="Susan Walker")
# rjenT = Teacher(name="Ralph Jenkins")

# jsant = User(username="jsantos", password="123123", student_id=1, teacher_id=0)
# bbrow = User(username="bbrown", password="123123", student_id=2, teacher_id=0)
# jstu = User(username="jstuart", password="123123", student_id=3, teacher_id=0)
# lich = User(username="lcheng", password="123123", student_id=4, teacher_id=0)
# nlit = User(username="nlittle", password="123123", student_id=5, teacher_id=0)
# mnor = User(username="mnorris", password="123123", student_id=6, teacher_id=0)
# aran = User(username="aranganath", password="123123", student_id=7, teacher_id=0)
# yiwe = User(username="ychen", password="123123", student_id=8, teacher_id=0)

# jsantS = Student(name="Jose Santos")
# bbrowS = Student(name="Betty Brown")
# jstuS = Student(name="John Stuart")
# lichS = Student(name="Li Cheng")
# nlitS = Student(name="Nancy Little")
# mnorS = Student(name="Mindy Norris")
# aranS = Student(name="Aditya Ranganath")
# yiweS = Student(name="Yi Wen Chen")

# math101 = Course(course_name="Math 101", teacher_id=3, num_enrolled=4, capacity=8, time="MWF 10:00-10:50 AM")
# phys121 = Course(course_name="Physics 121", teacher_id=2, time="TR 11:00-11:50 AM", num_enrolled=4, capacity=10)
# cs106 = Course(course_name="CS 106", teacher_id=1, time="MWF 2:00-2:50 PM", num_enrolled=4, capacity=10)
# cs162 = Course(course_name="CS 162", teacher_id=1, time="TR 3:00-3:50 PM", num_enrolled=4, capacity=4)

# db.session.add(phys121)
# db.session.add(cs106)
# db.session.add(cs162)

# db.session.add(ahepT)
# db.session.add(swalT)
# db.session.add(rjenT)

# db.session.add(jsant)
# db.session.add(bbrow)
# db.session.add(jstu)
# db.session.add(lich)
# db.session.add(nlit)
# db.session.add(mnor)
# db.session.add(aran)
# db.session.add(yiwe)

# db.session.add(jsantS)
# db.session.add(bbrowS)
# db.session.add(jstuS)
# db.session.add(lichS)
# db.session.add(nlitS)
# db.session.add(mnorS)
# db.session.add(aranS)
# db.session.add(yiweS)

# db.session.add(math101)
# db.session.commit()