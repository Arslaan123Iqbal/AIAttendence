from os import name

from flask.helpers import url_for
from recognizer import recognizer
from flask import Flask, render_template, request, redirect,Response, sessions,session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from camera import Video
from camera2 import Video2
import sqlite3
from face import captureImage
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///staff.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'AI'
app.config['SESSION_TYPE'] = 'filesystem'
db = SQLAlchemy(app)

class Staff(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    register = db.Column(db.String(500), nullable=False)
    email = db.Column(db.String(200), nullable=False)
    department = db.Column(db.String(200), nullable=False)
    phone = db.Column(db.String(200), nullable=False)

    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.sno} - {self.title}"

@app.route('/cam1')
def index():
    return render_template("index.html")

def gen1(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n\r\n')

@app.route("/video")
def video():
    return Response(gen1(Video()),
    mimetype ='multipart/x-mixed-replace; boundary=frame')

@app.route('/cam2')
def index1():
    return render_template("video2.html")

def gen2(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
        b'Content-Type: image/jpeg\r\n\r\n'+frame+b'\r\n\r\n')

@app.route("/video2")
def video2():
    return Response(gen2(Video2()),
    mimetype ='multipart/x-mixed-replace; boundary=frame')
    

@app.route('/add', methods=['GET', 'POST'])
def hello_world():
    if request.method=='POST':
        name = request.form['name']
        register = request.form['register']
        email = request.form['email']
        department = request.form['department']
        phone = request.form['phone']
        staff_memeber = Staff(name=name,register=register,email=email,department=department,phone=phone)
        db.session.add(staff_memeber)
        db.session.flush()
        db.session.commit()
        getid = staff_memeber.id
        print(getid)
        captureImage(getid)
        recognizer()
        
    allstaff = Staff.query.all() 
    return render_template('add.html',redirect="add.html", allstaff=allstaff)

@app.route("/signup", methods =["GET","POST"])
def signUp():
    if(request.method=="POST"):
        if(request.form["username"]!="" and request.form["password"]!=""):
            username = request.form["username"]
            password= request.form["password"]
            conn = sqlite3.connect("staff.db")
            c= conn.cursor()
            c.execute("INSERT INTO signup VALUES('"+ username+"','"+ password+"')")
            msg ="Your account created"
            conn.commit()
            conn.close()
        
    return render_template("signup.html")

@app.route("/", methods =["GET","POST"])
def login():
    r=""
    msg = ""
    if(request.method=="POST"):
        username = request.form["username"]
        password = request.form["password"]
        conn = sqlite3.connect("staff.db")
        c= conn.cursor()
        c.execute("SELECT* FROM signup WHERE username='"+ username+"' and password ='" + password+"' ")
        r= c.fetchall()
        for i in r :
            if(username== i[0] and password== i[1]):
                session["logedin"]= True
                session["username"]= username
                return redirect(url_for("home"))
            else:
                msg="Username and password is wrong"


    
            
    return render_template("login.html",msg=msg)
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("login"))
@app.route("/supervisor")
def super():
    return render_template("supervisor.html")

@app.route("/home", methods =["GET","POST"])
def home():
    return render_template("home.html")

@app.route('/attendencein')
def list():
   con = sqlite3.connect("staff.db")
   con.row_factory = sqlite3.Row
   
   cur = con.cursor()
   cur.execute("select * from attendence")
   
   rows = cur.fetchall(); 
   return render_template("attendence_in.html",rows = rows)

@app.route('/attendenceout')
def list2():
   con = sqlite3.connect("staff.db")
   con.row_factory = sqlite3.Row
   
   cur = con.cursor()
   cur.execute("select * from attendence_out")
   
   rows = cur.fetchall(); 
   return render_template("attendence_out.html",rows = rows)






@app.route('/manage')
def staffdata():
    data = Staff.query.all()
 
    return render_template("manage.html",data=data)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method=='POST':
        name = request.form['name']
        register = request.form['register']
        email = request.form['email']
        department = request.form['department']
        phone = request.form['phone']
        todo = Staff.query.filter_by(id=id).first()
        todo.name = name
        todo.register = register
        todo.email = email
        todo.department = department
        todo.phone = phone
        db.session.add(todo)
        db.session.commit()
        return redirect("/manage")
        
    staff = Staff.query.filter_by(id=id).first()
    return render_template('update.html', staff=staff)

@app.route('/delete/<int:id>')
def delete(id):
    todo = Staff.query.filter_by(id=id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/manage")

if __name__ == "__main__":
    app.run(host='0.0.0.0')