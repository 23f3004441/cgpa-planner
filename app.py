import os
from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from dotenv import load_dotenv

load_dotenv()  # reads your .env file

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "fallback-dev-key-change-this")

app.config["SQLALCHEMY_DATABASE_URI"] = os.environ.get("DATABASE_URL", "sqlite:///courses.db")
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)


# --------------------
# MODELS
# --------------------

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), unique=True)
    email = db.Column(db.String(200))
    password = db.Column(db.String(200))


class Course(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    code = db.Column(db.String(50))
    credits = db.Column(db.Integer)
    level = db.Column(db.String(50))


class UserGrade(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer)
    course_id = db.Column(db.Integer)
    grade = db.Column(db.String(2))


# --------------------
# GRADE POINTS
# --------------------

grade_points = {
    "S":10,"A":9,"B":8,"C":7,"D":6,"E":4,"U":0
}


# --------------------
# SEED COURSES
# --------------------

def seed_courses():

    expected = 57

    if Course.query.count() >= expected:
        return

    Course.query.delete()
    db.session.commit()

    courses = [

        # FOUNDATION
        Course(name="Mathematics for Data Science I", code="BSMA1001", credits=4, level="foundation"),
        Course(name="Statistics for Data Science I", code="BSMA1002", credits=4, level="foundation"),
        Course(name="Computational Thinking", code="BSCS1001", credits=4, level="foundation"),
        Course(name="English I", code="BSHS1001", credits=4, level="foundation"),
        Course(name="Mathematics for Data Science II", code="BSMA1003", credits=4, level="foundation"),
        Course(name="Statistics for Data Science II", code="BSMA1004", credits=4, level="foundation"),
        Course(name="Programming in Python", code="BSCS1002", credits=4, level="foundation"),
        Course(name="English II", code="BSHS1002", credits=4, level="foundation"),

        # DIPLOMA PROGRAMMING
        Course(name="Database Management Systems", code="BSCS2001", credits=4, level="diploma_prog"),
        Course(name="Programming Data Structures and Algorithms using Python", code="BSCS2002", credits=4, level="diploma_prog"),
        Course(name="Modern Application Development I", code="BSCS2003", credits=4, level="diploma_prog"),
        Course(name="Modern Application Development I Project", code="BSCS2003P", credits=2, level="diploma_prog"),
        Course(name="Programming Concepts using Java", code="BSCS2005", credits=4, level="diploma_prog"),
        Course(name="Modern Application Development II", code="BSCS2006", credits=4, level="diploma_prog"),
        Course(name="Modern Application Development II Project", code="BSCS2006P", credits=2, level="diploma_prog"),
        Course(name="System Commands", code="BSSE2001", credits=3, level="diploma_prog"),

        # DIPLOMA DATA SCIENCE
        Course(name="Machine Learning Foundations", code="BSCS2004", credits=4, level="diploma_ds"),
        Course(name="Business Data Management", code="BSMS2001", credits=4, level="diploma_ds"),
        Course(name="Machine Learning Techniques", code="BSCS2007", credits=4, level="diploma_ds"),
        Course(name="Machine Learning Practice", code="BSCS2008", credits=4, level="diploma_ds"),
        Course(name="Machine Learning Practice Project", code="BSCS2008P", credits=2, level="diploma_ds"),
        Course(name="Tools in Data Science", code="BSSE2002", credits=3, level="diploma_ds"),
        Course(name="Business Data Management Project", code="BSMS2001P", credits=2, level="diploma_ds"),
        Course(name="Business Analytics", code="BSMS2002", credits=4, level="diploma_ds"),
        Course(name="Introduction to Deep Learning and Generative AI", code="BSDA2001", credits=4, level="diploma_ds"),
        Course(name="Deep Learning and Generative AI Project", code="BSDA2001P", credits=2, level="diploma_ds"),

        # DEGREE
        Course(name="Software Engineering", code="BSCS3001", credits=4, level="degree"),
        Course(name="Software Testing", code="BSCS3002", credits=4, level="degree"),
        Course(name="AI: Search Methods for Problem Solving", code="BSCS3003", credits=4, level="degree"),
        Course(name="Deep Learning", code="BSCS3004", credits=4, level="degree"),
        Course(name="Strategies for Professional Growth", code="BSGN3001", credits=4, level="degree"),
        Course(name="Algorithmic Thinking in Bioinformatics", code="BSBT4001", credits=4, level="degree"),
        Course(name="Big Data and Biological Networks", code="BSBT4002", credits=4, level="degree"),
        Course(name="Data Visualization Design", code="BSCS4001", credits=4, level="degree"),
        Course(name="Special Topics in Machine Learning (Reinforcement Learning)", code="BSDA5007", credits=4, level="degree"),
        Course(name="Speech Technology", code="BSEE4001", credits=4, level="degree"),
        Course(name="Design Thinking for Data-Driven App Development", code="BSMS4002", credits=4, level="degree"),
        Course(name="Industry 4.0", code="BSMS4001", credits=4, level="degree"),
        Course(name="Sequential Decision Making", code="BSDA5007", credits=4, level="degree"),
        Course(name="Market Research", code="BSMS3002", credits=4, level="degree"),
        Course(name="Privacy & Security in Online Social Media", code="BSCS4003", credits=4, level="degree"),
        Course(name="Introduction to Big Data", code="BSDA5001", credits=4, level="degree"),
        Course(name="Financial Forensics", code="BSMS4003", credits=4, level="degree"),
        Course(name="Linear Statistical Models", code="BSMA3012", credits=4, level="degree"),
        Course(name="Advanced Algorithms", code="BSCS4021", credits=4, level="degree"),
        Course(name="Statistical Computing", code="BSMA3014", credits=4, level="degree"),
        Course(name="Computer Systems Design", code="BSCS3031", credits=4, level="degree"),
        Course(name="Programming in C", code="BSCS3005", credits=4, level="degree"),
        Course(name="Mathematical Thinking", code="BSMA2001", credits=4, level="degree"),
        Course(name="Large Language Models", code="BSDA5004", credits=4, level="degree"),
        Course(name="Introduction to Natural Language Processing (i-NLP)", code="BSDA5005", credits=4, level="degree"),
        Course(name="Deep Learning for Computer Vision", code="BSDA5006", credits=4, level="degree"),
        Course(name="Managerial Economics", code="BSMS3033", credits=4, level="degree"),
        Course(name="Game Theory and Strategy", code="BSMS4023", credits=4, level="degree"),
        Course(name="Corporate Finance", code="BSMS3034", credits=4, level="degree"),
        Course(name="Deep Learning Practice", code="BSDA5013", credits=4, level="degree"),
        Course(name="Operating Systems", code="BSCS4022", credits=4, level="degree"),
        Course(name="Mathematical Foundations of Generative AI", code="BSDA5002", credits=4, level="degree"),
        Course(name="Algorithms for Data Science", code="BSDA5003", credits=4, level="degree"),
        Course(name="Machine Learning Operations (MLOps)", code="BSDA5014", credits=4, level="degree"),
        Course(name="Data Science and AI Lab", code="BSDA4001", credits=4, level="degree"),
        Course(name="App Dev Lab", code="BSCS4010", credits=4, level="degree"),
        Course(name="Computer Networks", code="BSCS4024", credits=4, level="degree"),
        Course(name="Theory of Computation", code="BSCS3021", credits=4, level="degree"),
    ]

    db.session.add_all(courses)
    db.session.commit()


# --------------------
# ROUTES
# --------------------

@app.route("/")
def index():
    return render_template("index.html")


@app.route("/register", methods=["GET","POST"])
def register():
    if request.method == "POST":
        user = User(
            username=request.form["username"],
            email=request.form["email"],
            password=generate_password_hash(request.form["password"])
        )
        db.session.add(user)
        db.session.commit()
        return redirect("/login")
    return render_template("register.html")


@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form["username"]).first()
        if user and check_password_hash(user.password, request.form["password"]):
            session["user_id"] = user.id
            return redirect("/dashboard")
    return render_template("login.html")


@app.route("/dashboard")
def dashboard():
    if "user_id" not in session:
        return redirect("/login")

    user = db.session.get(User, session["user_id"])
    saved = UserGrade.query.filter_by(user_id=session["user_id"]).all()
    saved_grades = {g.course_id: g.grade for g in saved}

    return render_template(
        "dashboard.html",
        foundation_courses=Course.query.filter_by(level="foundation").all(),
        diploma_prog_courses=Course.query.filter_by(level="diploma_prog").all(),
        diploma_ds_courses=Course.query.filter_by(level="diploma_ds").all(),
        degree_courses=Course.query.filter_by(level="degree").all(),
        saved_grades=saved_grades,
        username=user.username,
        cgpa=None
    )


@app.route("/calculate", methods=["POST"])
def calculate():
    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]
    user = db.session.get(User, session["user_id"])
    courses = Course.query.all()

    total_points = 0
    total_credits = 0

    for course in courses:
        grade = request.form.get(f"course_{course.id}")
        if grade:
            existing = UserGrade.query.filter_by(user_id=user_id, course_id=course.id).first()
            if existing:
                existing.grade = grade
            else:
                db.session.add(UserGrade(user_id=user_id, course_id=course.id, grade=grade))
            if grade in grade_points:
                total_points += grade_points[grade] * course.credits
                total_credits += course.credits

    db.session.commit()

    cgpa = round(total_points / total_credits, 2) if total_credits else None
    saved = UserGrade.query.filter_by(user_id=user_id).all()
    saved_grades = {g.course_id: g.grade for g in saved}

    return render_template(
        "dashboard.html",
        foundation_courses=Course.query.filter_by(level="foundation").all(),
        diploma_prog_courses=Course.query.filter_by(level="diploma_prog").all(),
        diploma_ds_courses=Course.query.filter_by(level="diploma_ds").all(),
        degree_courses=Course.query.filter_by(level="degree").all(),
        saved_grades=saved_grades,
        username=user.username,
        cgpa=cgpa
    )


@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")


# --------------------
# START APP
# --------------------

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
        seed_courses()
    app.run(debug=True)